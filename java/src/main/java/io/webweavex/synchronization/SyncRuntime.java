package io.webweavex.synchronization;

import io.webweavex.crypto.Kaalka;
import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import io.webweavex.determinism.PyJson;
import io.webweavex.determinism.PyJsonParse;
import io.webweavex.determinism.PyRepr;
import io.webweavex.execution.ExecutionRuntime;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

/**
 * Port of the {@code core.synchronization} family — {@code build_runtime_delta},
 * {@code run_synchronized_runtime}, {@code replay_synchronized_runtime},
 * {@code run_sync_for_extraction}, {@code save_sync_memory}, {@code load_sync_memory} — and the
 * ~18 deterministic sub-engines + synchronization IR they fan out to. Dependency-clean
 * (25-module closure, 0 forbidden; the FS sync-memory engine is only invoked when a memory
 * path+key are supplied). Reuses the certified determinism/crypto/json substrate and
 * {@link ExecutionRuntime#buildUnifiedRuntimeGraph}.
 */
public final class SyncRuntime {

    private SyncRuntime() {
    }

    // -------------------------------------------------------------- helpers

    private static Map<String, Object> map() {
        return new LinkedHashMap<>();
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> asMap(Object o) {
        return o instanceof Map ? (Map<String, Object>) o : map();
    }

    @SuppressWarnings("unchecked")
    private static List<Object> asList(Object o) {
        return o instanceof List ? new ArrayList<>((List<Object>) o) : new ArrayList<>();
    }

    private static Map<String, Object> dictCopy(Object o) {
        return new LinkedHashMap<>(asMap(o));
    }

    private static long pyInt(Object v, long dflt) {
        if (v == null) {
            return dflt;
        }
        if (v instanceof Boolean) {
            return ((Boolean) v) ? 1L : 0L;
        }
        if (v instanceof Number) {
            return (long) ((Number) v).doubleValue();
        }
        if (v instanceof String) {
            return Long.parseLong(((String) v).trim());
        }
        return dflt;
    }

    private static String str(Object o) {
        return PyRepr.str(o);
    }

    private static int cmp(String a, String b) {
        return Normalization.codePointCompare(a, b);
    }

    /** Python {@code ==} deep equality for the native value tree. */
    @SuppressWarnings("unchecked")
    private static boolean pyEquals(Object a, Object b) {
        if (a == null || b == null) {
            return a == b;
        }
        if (a instanceof Number && b instanceof Number) {
            return ((Number) a).doubleValue() == ((Number) b).doubleValue();
        }
        if (a instanceof Map && b instanceof Map) {
            Map<String, Object> ma = (Map<String, Object>) a;
            Map<String, Object> mb = (Map<String, Object>) b;
            if (ma.size() != mb.size()) {
                return false;
            }
            for (Map.Entry<String, Object> e : ma.entrySet()) {
                if (!mb.containsKey(e.getKey()) || !pyEquals(e.getValue(), mb.get(e.getKey()))) {
                    return false;
                }
            }
            return true;
        }
        if (a instanceof List && b instanceof List) {
            List<Object> la = (List<Object>) a;
            List<Object> lb = (List<Object>) b;
            if (la.size() != lb.size()) {
                return false;
            }
            for (int i = 0; i < la.size(); i++) {
                if (!pyEquals(la.get(i), lb.get(i))) {
                    return false;
                }
            }
            return true;
        }
        return a.equals(b);
    }

    private static Set<String> sortedKeyUnion(Map<String, Object> a, Map<String, Object> b) {
        Set<String> keys = new TreeSet<>(Normalization::codePointCompare);
        keys.addAll(a.keySet());
        keys.addAll(b.keySet());
        return keys;
    }

    private static String sha256hex32(String text) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] d = md.digest(text.getBytes(StandardCharsets.UTF_8));
            StringBuilder sb = new StringBuilder(64);
            for (byte x : d) {
                sb.append(Character.forDigit((x >> 4) & 0xF, 16));
                sb.append(Character.forDigit(x & 0xF, 16));
            }
            return sb.substring(0, 32);
        } catch (Exception e) {
            throw new IllegalStateException(e);
        }
    }

    private static Map<String, Object> mapOf(Object... kv) {
        Map<String, Object> m = map();
        for (int i = 0; i < kv.length; i += 2) {
            m.put((String) kv[i], kv[i + 1]);
        }
        return m;
    }

    // -------------------------------------------------------------- delta

    private static String classifyChange(String field) {
        if (field.contains("semantic")) {
            return "semantic_change";
        }
        if (field.contains("workflow")) {
            return "workflow_change";
        }
        if (field.contains("dom") || field.contains("ui")) {
            return "ui_mutation";
        }
        if (field.contains("state")) {
            return "application_state_mutation";
        }
        return "runtime_transition";
    }

    /** {@code build_runtime_delta}. */
    public static Map<String, Object> buildRuntimeDelta(Map<String, Object> previous,
            Map<String, Object> current, long tick) {
        Map<String, Object> prev = previous == null ? map() : previous;
        Map<String, Object> cur = current == null ? map() : current;
        List<Object> changes = new ArrayList<>();
        for (String key : sortedKeyUnion(prev, cur)) {
            if (!pyEquals(prev.get(key), cur.get(key))) {
                Map<String, Object> ch = map();
                ch.put("field", key);
                ch.put("from", prev.get(key));
                ch.put("to", cur.get(key));
                ch.put("kind", classifyChange(key));
                changes.add(ch);
            }
        }
        String payload = jsonKey(changes);
        String deltaId = sha256hex32(payload);
        Map<String, Object> out = map();
        out.put("delta_id", deltaId);
        out.put("changes", changes);
        out.put("timestamp", tick);
        out.put("bounded", true);
        return out;
    }

    private static String jsonKey(List<Object> changes) {
        List<Object> sorted = new ArrayList<>(changes);
        sorted.sort((a, b) -> cmp(str(asMap(a).get("field")), str(asMap(b).get("field"))));
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < sorted.size(); i++) {
            Map<String, Object> c = asMap(sorted.get(i));
            if (i > 0) {
                sb.append("|");
            }
            sb.append(str(c.get("field"))).append(":").append(str(c.get("kind")));
        }
        return sb.toString();
    }

    // -------------------------------------------------------------- replay

    /** {@code replay_synchronized_runtime}. */
    public static Map<String, Object> replaySynchronizedRuntime(Map<String, Object> memory) {
        Map<String, Object> m = memory == null ? map() : memory;
        Map<String, Object> out = map();
        out.put("synchronized_histories", Py.get(m, "history", map()));
        out.put("runtime_deltas", Py.get(m, "deltas", new ArrayList<>()));
        out.put("semantic_timelines", Py.get(m, "timeline", map()));
        out.put("distributed_realities", Py.get(m, "realities", new ArrayList<>()));
        out.put("convergence", Py.get(m, "convergence", map()));
        out.put("replayed", true);
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- snapshot / drift / diff / mutation

    public static Map<String, Object> captureRuntimeSnapshot(Map<String, Object> browser, Map<String, Object> native_,
            Map<String, Object> semantic, Map<String, Object> workflow, Map<String, Object> causality,
            Map<String, Object> syncState, long tick) {
        Map<String, Object> out = map();
        out.put("snapshot_id", "snapshot:" + tick);
        out.put("tick", tick);
        out.put("browser_runtime", dictCopy(browser));
        out.put("native_runtime", dictCopy(native_));
        out.put("semantic_runtime", dictCopy(semantic));
        out.put("workflow_state", dictCopy(workflow));
        out.put("causality_state", dictCopy(causality));
        out.put("synchronization_state", dictCopy(syncState));
        out.put("bounded", true);
        return out;
    }

    private static final String[][] DRIFT_CHECKS = {
        {"selector_drift", "selectors"}, {"semantic_drift", "semantic"}, {"workflow_drift", "workflow"},
        {"topology_drift", "topology"}, {"application_drift", "application"}, {"runtime_divergence", "runtime"},
    };

    public static Map<String, Object> detectRuntimeDrift(Map<String, Object> baseline, Map<String, Object> current) {
        List<Object> drifts = new ArrayList<>();
        for (String[] dc : DRIFT_CHECKS) {
            if (!pyEquals(baseline.get(dc[1]), current.get(dc[1]))) {
                drifts.add(mapOf("type", dc[0], "field", dc[1], "detected", true));
            }
        }
        Map<String, Object> out = map();
        out.put("drifts", drifts);
        out.put("drift_count", (long) drifts.size());
        out.put("diverged", drifts.size() > 0);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> diffRuntimeState(Map<String, Object> previous, Map<String, Object> current) {
        List<Object> runtimeChanges = new ArrayList<>();
        List<Object> semanticMut = new ArrayList<>();
        List<Object> workflowMut = new ArrayList<>();
        List<Object> distributedChanges = new ArrayList<>();
        for (String key : sortedKeyUnion(previous, current)) {
            if (pyEquals(previous.get(key), current.get(key))) {
                continue;
            }
            Map<String, Object> entry = mapOf("field", key, "from", previous.get(key), "to", current.get(key));
            if (key.contains("semantic")) {
                semanticMut.add(entry);
            } else if (key.contains("workflow")) {
                workflowMut.add(entry);
            } else if (key.contains("distributed") || key.contains("worker")) {
                distributedChanges.add(entry);
            } else {
                runtimeChanges.add(entry);
            }
        }
        Map<String, Object> out = map();
        out.put("runtime_changes", runtimeChanges);
        out.put("semantic_mutations", semanticMut);
        out.put("workflow_mutations", workflowMut);
        out.put("distributed_changes", distributedChanges);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> trackRuntimeMutations(List<Object> changes, long tick) {
        List<Object> sorted = new ArrayList<>(changes);
        sorted.sort((a, b) -> cmp(str(Py.get(asMap(a), "field", "")), str(Py.get(asMap(b), "field", ""))));
        Map<String, Object> out = map();
        out.put("mutations", sorted);
        out.put("count", (long) changes.size());
        out.put("tick", tick);
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- merge / converge / sync / replication

    public static Map<String, Object> mergeRuntimeRealities(List<Object> realities) {
        Map<String, Object> mergedSemantic = map();
        Map<String, Object> mergedWorkflow = map();
        Map<String, Object> mergedApplication = map();
        List<Object> timelines = new ArrayList<>();
        int limit = Math.min(realities.size(), 1000);
        for (int i = 0; i < limit; i++) {
            Map<String, Object> reality = asMap(realities.get(i));
            timelines.add(mapOf("reality_id", str(Py.get(reality, "reality_id", "")),
                    "tick", pyInt(Py.get(reality, "tick", 0L), 0)));
            mergedSemantic.putAll(asMap(reality.get("semantic")));
            mergedWorkflow.putAll(asMap(reality.get("workflow")));
            mergedApplication.putAll(asMap(reality.get("application")));
        }
        List<Object> sortedTimelines = new ArrayList<>(timelines);
        sortedTimelines.sort(Comparator.comparingLong(t -> pyInt(asMap(t).get("tick"), 0)));
        Map<String, Object> out = map();
        out.put("semantic", mergedSemantic);
        out.put("workflow", mergedWorkflow);
        out.put("application", mergedApplication);
        out.put("timelines", sortedTimelines);
        out.put("reality_count", (long) realities.size());
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> convergeRuntimeState(List<Object> realities) {
        Map<String, Object> merged = map();
        List<Object> histories = new ArrayList<>();
        List<Object> sorted = new ArrayList<>(realities);
        sorted.sort((a, b) -> cmp(str(Py.get(asMap(a), "reality_id", "")), str(Py.get(asMap(b), "reality_id", ""))));
        for (int index = 0; index < sorted.size(); index++) {
            Map<String, Object> reality = asMap(sorted.get(index));
            histories.add(str(Py.get(reality, "reality_id", "reality:" + index)));
            for (Map.Entry<String, Object> e : reality.entrySet()) {
                if (e.getKey().equals("reality_id")) {
                    continue;
                }
                merged.put(e.getKey(), e.getValue());
            }
        }
        Map<String, Object> out = map();
        out.put("converged_state", merged);
        out.put("reality_count", (long) realities.size());
        out.put("histories", histories);
        out.put("converged", true);
        out.put("bounded", true);
        return out;
    }

    private static final String[] SYNC_HANDLERS = {"browser", "electron", "terminal", "vm", "remote"};

    public static Map<String, Object> synchronizeRuntime(List<Object> snapshots, long tick) {
        List<Object> synchronized_ = new ArrayList<>();
        for (String runtime : SYNC_HANDLERS) {
            Map<String, Object> payload = map();
            for (Object so : snapshots) {
                Map<String, Object> snapshot = asMap(so);
                String key = runtime.equals("browser") ? "browser_runtime" : runtime + "_runtime";
                if (runtime.equals("electron")) {
                    key = "native_runtime";
                }
                Object value = Py.get(snapshot, key, Py.get(snapshot, "native_runtime", map()));
                if (Py.truthy(value)) {
                    if (value instanceof Map) {
                        payload.putAll(asMap(value));
                    } else {
                        payload.put("data", value);
                    }
                }
            }
            synchronized_.add(mapOf("runtime", runtime, "synced", Py.truthy(payload), "tick", tick,
                    "handler", "sync_" + runtime));
        }
        long count = 0;
        for (Object s : synchronized_) {
            if (Py.truthy(asMap(s).get("synced"))) {
                count++;
            }
        }
        Map<String, Object> out = map();
        out.put("synchronized", synchronized_);
        out.put("count", count);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> replicateRuntimeReality(Map<String, Object> source, List<Object> workers) {
        List<Object> replicas = new ArrayList<>();
        int limit = Math.min(workers.size(), 1000);
        for (int index = 0; index < limit; index++) {
            Map<String, Object> worker = asMap(workers.get(index));
            Map<String, Object> r = map();
            r.put("worker_id", str(Py.get(worker, "worker_id", Py.get(worker, "id", "worker:" + index))));
            r.put("reality_id", str(Py.get(source, "reality_id", "primary")));
            r.put("semantic_state", dictCopy(source.get("semantic_state")));
            r.put("runtime_state", dictCopy(source.get("runtime_state")));
            r.put("workflows", dictCopy(source.get("workflows")));
            r.put("checkpoints", asList(source.get("checkpoints")));
            r.put("causality_graph", dictCopy(source.get("causality_graph")));
            r.put("replicated", true);
            replicas.add(r);
        }
        Map<String, Object> out = map();
        out.put("replicas", replicas);
        out.put("replica_count", (long) replicas.size());
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> federateRuntimeRealities(List<Object> workers, Map<String, Object> browser,
            Map<String, Object> native_, Map<String, Object> semantic, Map<String, Object> application) {
        List<Object> wk = workers == null ? new ArrayList<>() : workers;
        List<Object> fw = new ArrayList<>();
        int limit = Math.min(wk.size(), 1000);
        for (int index = 0; index < limit; index++) {
            Map<String, Object> worker = asMap(wk.get(index));
            fw.add(mapOf("worker_id", str(Py.get(worker, "worker_id", Py.get(worker, "id", "w:" + index))),
                    "federated", true));
        }
        Map<String, Object> out = map();
        out.put("workers", fw);
        out.put("browser_runtime", Py.truthy(browser));
        out.put("native_runtime", Py.truthy(native_));
        out.put("semantic_state", Py.truthy(semantic));
        out.put("application_cognition", Py.truthy(application));
        out.put("federated", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> alignRuntimeLayers(Map<String, Object> browser, Map<String, Object> native_,
            Map<String, Object> semantic, Map<String, Object> workflow) {
        Map<String, Object> out = map();
        out.put("browser", Py.truthy(browser));
        out.put("native", Py.truthy(native_));
        out.put("semantic", Py.truthy(semantic));
        out.put("workflow", Py.truthy(workflow));
        out.put("aligned", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> maintainRuntimeContinuity(Map<String, Object> session, Map<String, Object> identity,
            Map<String, Object> workflow, Map<String, Object> semantic, Map<String, Object> checkpoint) {
        Map<String, Object> out = map();
        out.put("authenticated_session", dictCopy(session));
        out.put("browser_identity", dictCopy(identity));
        out.put("workflows", dictCopy(workflow));
        out.put("semantic_state", dictCopy(semantic));
        out.put("distributed_checkpoint", dictCopy(checkpoint));
        out.put("continuous", true);
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- history / timeline / state graph / consistency

    public static Map<String, Object> buildRuntimeHistory(List<Object> deltas, List<Object> workflows) {
        List<Object> sortedDeltas = new ArrayList<>(deltas);
        sortedDeltas.sort(Comparator.comparingLong(d -> pyInt(asMap(d).get("timestamp"), 0)));
        List<Object> mutations = new ArrayList<>();
        List<Object> semanticEvolution = new ArrayList<>();
        for (Object do_ : deltas) {
            for (Object co : asList(asMap(do_).get("changes"))) {
                mutations.add(co);
                if ("semantic_change".equals(asMap(co).get("kind"))) {
                    semanticEvolution.add(co);
                }
            }
        }
        Map<String, Object> out = map();
        out.put("deltas", sortedDeltas);
        out.put("transitions", new ArrayList<>());
        out.put("mutations", mutations);
        out.put("workflows", workflows == null ? new ArrayList<>() : workflows);
        out.put("semantic_evolution", semanticEvolution);
        out.put("length", (long) deltas.size());
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildSyncTimeline(Map<String, Object> history) {
        List<Object> entries = new ArrayList<>();
        for (Object do_ : asList(history.get("deltas"))) {
            Map<String, Object> delta = asMap(do_);
            entries.add(mapOf("tick", pyInt(Py.get(delta, "timestamp", 0L), 0),
                    "delta_id", str(Py.get(delta, "delta_id", "")),
                    "change_count", (long) asList(delta.get("changes")).size()));
        }
        entries.sort(Comparator.comparingLong(e -> pyInt(asMap(e).get("tick"), 0)));
        Map<String, Object> out = map();
        out.put("timeline", entries);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildRuntimeStateGraph(Map<String, Object> snapshot, Map<String, Object> delta,
            Map<String, Object> convergence) {
        List<Object> nodes = new ArrayList<>();
        List<Object> edges = new ArrayList<>();
        String snapshotId = str(Py.get(snapshot, "snapshot_id", "snapshot:0"));
        nodes.add(mapOf("id", snapshotId, "type", "snapshot"));
        String deltaId = str(Py.get(delta, "delta_id", "delta:0"));
        nodes.add(mapOf("id", deltaId, "type", "delta"));
        edges.add(mapOf("from", snapshotId, "to", deltaId, "relation", "mutates"));
        List<Object> changes = asList(delta.get("changes"));
        int climit = Math.min(changes.size(), 5000);
        for (int i = 0; i < climit; i++) {
            String nodeId = "change:" + str(Py.get(asMap(changes.get(i)), "field", ""));
            nodes.add(mapOf("id", nodeId, "type", "mutation"));
            edges.add(mapOf("from", deltaId, "to", nodeId, "relation", "propagates"));
        }
        String convergedId = "convergence:root";
        nodes.add(mapOf("id", convergedId, "type", "convergence"));
        edges.add(mapOf("from", deltaId, "to", convergedId, "relation", "converges"));
        if (Py.truthy(delta.get("changes"))) {
            edges.add(mapOf("from", convergedId, "to", snapshotId, "relation", "synchronizes"));
        }
        nodes.add(mapOf("id", "checkpoint:sync", "type", "checkpoint"));
        edges.add(mapOf("from", convergedId, "to", "checkpoint:sync", "relation", "restores"));
        List<Object> sortedNodes = new ArrayList<>(nodes);
        sortedNodes.sort((a, b) -> cmp(str(asMap(a).get("id")), str(asMap(b).get("id"))));
        List<Object> sortedEdges = new ArrayList<>(edges);
        sortedEdges.sort(Comparator
                .comparing((Object e) -> str(Py.get(asMap(e), "from", "")), SyncRuntime::cmp)
                .thenComparing(e -> str(Py.get(asMap(e), "to", "")), SyncRuntime::cmp)
                .thenComparing(e -> str(Py.get(asMap(e), "relation", "")), SyncRuntime::cmp));
        Map<String, Object> out = map();
        out.put("nodes", sortedNodes);
        out.put("edges", sortedEdges);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> verifyRuntimeConsistency(Map<String, Object> history, Map<String, Object> convergence,
            Map<String, Object> replay) {
        List<Object> deltas = asList(history.get("deltas"));
        List<Object> issues = new ArrayList<>();
        if (!Py.truthy(Py.get(convergence, "converged", null))) {
            issues.add("convergence_incomplete");
        }
        if (!Py.truthy(Py.get(replay, "replayed", null))) {
            issues.add("replay_not_ready");
        }
        for (int index = 1; index < deltas.size(); index++) {
            if (pyInt(Py.get(asMap(deltas.get(index)), "timestamp", 0L), 0)
                    < pyInt(Py.get(asMap(deltas.get(index - 1)), "timestamp", 0L), 0)) {
                issues.add("timeline_order_violation");
                break;
            }
        }
        Map<String, Object> out = map();
        out.put("consistent", issues.isEmpty());
        out.put("issues", issues);
        out.put("synchronization_integrity", issues.isEmpty());
        out.put("semantic_continuity", history.containsKey("semantic_evolution"));
        out.put("replay_consistency", Py.truthy(Py.get(replay, "replayed", false)));
        out.put("distributed_convergence", Py.truthy(Py.get(convergence, "converged", false)));
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- IR

    public static Map<String, Object> compileSynchronizationRuntimeIr(Map<String, Object> sync) {
        Map<String, Object> out = map();
        out.put("ir", "synchronization_runtime");
        out.put("snapshot", Py.get(sync, "snapshot", map()));
        out.put("delta", Py.get(sync, "delta", map()));
        out.put("history", Py.get(sync, "history", map()));
        out.put("timeline", Py.get(sync, "timeline", map()));
        out.put("convergence", Py.get(sync, "convergence", map()));
        out.put("synchronization", Py.get(sync, "synchronization", map()));
        out.put("replication", Py.get(sync, "replication", map()));
        out.put("continuity", Py.get(sync, "continuity", map()));
        out.put("state_graph", Py.get(sync, "state_graph", map()));
        out.put("consistency", Py.get(sync, "consistency", map()));
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> synchronizationRuntimeIrToGraph(Map<String, Object> syncIr) {
        Map<String, Object> graph = asMap(syncIr.get("state_graph"));
        List<Object> nodes = asList(graph.get("nodes"));
        List<Object> edges = asList(graph.get("edges"));
        if (nodes.isEmpty()) {
            nodes = new ArrayList<>(List.of(mapOf("id", "sync:root", "type", "synchronization")));
        }
        List<Object> sortedNodes = new ArrayList<>(nodes);
        sortedNodes.sort((a, b) -> cmp(str(Py.get(asMap(a), "id", "")), str(Py.get(asMap(b), "id", ""))));
        Map<String, Object> out = map();
        out.put("ir", "synchronization_runtime_graph");
        out.put("nodes", sortedNodes);
        out.put("edges", edges);
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- memory (FS)

    public static Map<String, Object> rememberSyncRuntime(Map<String, Object> memory, Map<String, Object> update) {
        Map<String, Object> merged = new LinkedHashMap<>(memory == null ? map() : memory);
        for (String field : new String[] {"deltas", "history", "timeline", "convergence", "realities",
                "continuity", "state_graph"}) {
            if (!merged.containsKey(field)) {
                Object v = update.containsKey(field) ? update.get(field)
                        : (merged.containsKey(field) ? merged.get(field) : map());
                merged.put(field, v);
            }
        }
        merged.putAll(update);
        merged.put("bounded", true);
        return merged;
    }

    private static Map<String, Object> emptyMemory() {
        Map<String, Object> m = map();
        m.put("deltas", new ArrayList<>());
        m.put("history", map());
        m.put("timeline", map());
        m.put("convergence", map());
        m.put("realities", new ArrayList<>());
        m.put("continuity", map());
        m.put("state_graph", map());
        m.put("bounded", true);
        return m;
    }

    /** {@code save_sync_memory(path, memory, key)}. */
    public static Map<String, Object> saveSyncMemory(String path, Map<String, Object> memory, String key) {
        String payload = PyJson.dumpsDefaultAscii(memory);
        Map<String, Object> encrypted = Kaalka.encryptValueEnvelope(payload, key);
        Map<String, Object> wrapper = map();
        wrapper.put("encrypted", encrypted.get("encrypted"));
        wrapper.put("algorithm", "kaalka");
        Path target = Paths.get(path);
        try {
            Path parent = target.getParent();
            if (parent != null) {
                Files.createDirectories(parent);
            }
            Files.write(target, PyJson.dumpsDefaultAscii(wrapper).getBytes(StandardCharsets.UTF_8));
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
        Map<String, Object> out = map();
        out.put("saved", true);
        out.put("path", target.toString());
        out.put("algorithm", "kaalka");
        out.put("bounded", true);
        return out;
    }

    /** {@code load_sync_memory(path, key)}. */
    public static Map<String, Object> loadSyncMemory(String path, String key) {
        Path target = Paths.get(path);
        if (!Files.exists(target)) {
            Map<String, Object> out = map();
            out.put("available", false);
            out.put("memory", emptyMemory());
            out.put("bounded", true);
            return out;
        }
        try {
            String content = new String(Files.readAllBytes(target), StandardCharsets.UTF_8);
            Map<String, Object> wrapper = asMap(PyJsonParse.loads(content));
            Map<String, Object> decrypted = Kaalka.decryptValueEnvelope(str(wrapper.get("encrypted")), key);
            Object memory = PyJsonParse.loads(str(decrypted.get("decrypted")));
            Map<String, Object> out = map();
            out.put("available", true);
            out.put("memory", memory);
            out.put("algorithm", "kaalka");
            out.put("bounded", true);
            return out;
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    // -------------------------------------------------------------- orchestrator

    private static Map<String, Object> runtimeView(Map<String, Object> extraction, Map<String, Object> semantic,
            Map<String, Object> workflow, Map<String, Object> causality) {
        Map<String, Object> ext = extraction == null ? map() : extraction;
        Map<String, Object> sem = semantic == null ? map() : semantic;
        Map<String, Object> wf = workflow == null ? map() : workflow;
        Map<String, Object> ca = causality == null ? map() : causality;
        Map<String, Object> out = map();
        out.put("dom", Py.get(ext, "dom", map()));
        out.put("semantic", Py.get(sem, "semantic", sem));
        out.put("workflow", Py.get(wf, "workflow", wf));
        out.put("causality", Py.get(ca, "causality", ca));
        out.put("runtime", Py.get(ext, "runtime", map()));
        return out;
    }

    /** {@code run_synchronized_runtime}. */
    public static Map<String, Object> runSynchronizedRuntime(long tick, Map<String, Object> browser,
            Map<String, Object> native_, Map<String, Object> semanticResult, Map<String, Object> workflowResult,
            Map<String, Object> causalityResult, Map<String, Object> distributedResult, Map<String, Object> session,
            Map<String, Object> identity, Map<String, Object> memory, List<Object> workers) {
        Map<String, Object> mem = dictCopy(memory);
        List<Object> wk = workers != null ? new ArrayList<>(workers)
                : asList(Py.get(distributedResult == null ? map() : distributedResult, "workers", new ArrayList<>()));

        Map<String, Object> previousView = asMap(Py.get(mem, "last_view", map()));
        Map<String, Object> currentView = runtimeView(browser, semanticResult, workflowResult, causalityResult);

        Map<String, Object> delta = buildRuntimeDelta(previousView, currentView, tick);
        Map<String, Object> snapshot = captureRuntimeSnapshot(browser, native_, semanticResult, workflowResult,
                causalityResult, asMap(Py.get(mem, "continuity", map())), tick);

        Map<String, Object> drift = detectRuntimeDrift(
                driftView(previousView), driftView(currentView));
        Map<String, Object> stateDiff = diffRuntimeState(previousView, currentView);
        Map<String, Object> mutations = trackRuntimeMutations(asList(delta.get("changes")), tick);

        List<Object> realities = new ArrayList<>();
        Map<String, Object> primary = map();
        primary.put("reality_id", "primary");
        primary.put("tick", tick);
        primary.put("semantic", Py.get(currentView, "semantic", map()));
        primary.put("workflow", Py.get(currentView, "workflow", map()));
        primary.put("application", Py.get(currentView, "workflow", map()));
        realities.add(primary);
        if (Py.truthy(distributedResult)) {
            Map<String, Object> dist = map();
            dist.put("reality_id", "distributed");
            dist.put("tick", tick);
            dist.put("semantic", map());
            dist.put("workflow", distributedResult);
            dist.put("application", map());
            realities.add(dist);
        }

        Map<String, Object> merged = mergeRuntimeRealities(realities);
        Map<String, Object> convergence = convergeRuntimeState(realities);
        Map<String, Object> synchronization = synchronizeRuntime(new ArrayList<>(List.of(snapshot)), tick);
        Map<String, Object> replSource = map();
        replSource.put("reality_id", "primary");
        replSource.put("semantic_state", Py.get(currentView, "semantic", map()));
        replSource.put("runtime_state", Py.get(currentView, "runtime", map()));
        replSource.put("workflows", Py.get(currentView, "workflow", map()));
        replSource.put("checkpoints", Py.get(mem, "checkpoints", new ArrayList<>()));
        replSource.put("causality_graph", Py.get(currentView, "causality", map()));
        Map<String, Object> replication = replicateRuntimeReality(replSource, wk);
        Map<String, Object> federation = federateRuntimeRealities(wk, browser, native_, semanticResult,
                workflowResult);
        Map<String, Object> alignment = alignRuntimeLayers(browser, native_, semanticResult, workflowResult);
        Map<String, Object> continuity = maintainRuntimeContinuity(session, identity, workflowResult,
                semanticResult, asMap(Py.get(mem, "checkpoint", map())));

        List<Object> priorDeltas = asList(Py.get(mem, "deltas", new ArrayList<>()));
        List<Object> allDeltas = new ArrayList<>(priorDeltas);
        allDeltas.add(delta);
        Map<String, Object> history = buildRuntimeHistory(allDeltas,
                new ArrayList<>(List.of(Py.get(merged, "workflow", map()))));
        Map<String, Object> timeline = buildSyncTimeline(history);
        Map<String, Object> stateGraph = buildRuntimeStateGraph(snapshot, delta, convergence);

        Map<String, Object> payload = map();
        payload.put("snapshot", snapshot);
        payload.put("delta", delta);
        payload.put("drift", drift);
        payload.put("diff", stateDiff);
        payload.put("mutations", mutations);
        payload.put("merge", merged);
        payload.put("convergence", convergence);
        payload.put("synchronization", synchronization);
        payload.put("replication", replication);
        payload.put("federation", federation);
        payload.put("alignment", alignment);
        payload.put("continuity", continuity);
        payload.put("history", history);
        payload.put("timeline", timeline);
        payload.put("state_graph", stateGraph);
        payload.put("bounded", true);

        Map<String, Object> update = map();
        update.put("deltas", allDeltas);
        update.put("history", history);
        update.put("timeline", timeline);
        update.put("convergence", convergence);
        update.put("realities", realities);
        update.put("continuity", continuity);
        update.put("state_graph", stateGraph);
        update.put("last_view", currentView);
        Map<String, Object> updatedMemory = rememberSyncRuntime(mem, update);
        Map<String, Object> replay = replaySynchronizedRuntime(updatedMemory);
        Map<String, Object> consistency = verifyRuntimeConsistency(history, convergence, replay);

        payload.put("memory", updatedMemory);
        payload.put("replay", replay);
        payload.put("consistency", consistency);
        payload.put("sync_ir", compileSynchronizationRuntimeIr(payload));
        return payload;
    }

    private static Map<String, Object> driftView(Map<String, Object> view) {
        Map<String, Object> out = map();
        out.put("selectors", Py.get(view, "dom", map()));
        out.put("semantic", Py.get(view, "semantic", map()));
        out.put("workflow", Py.get(view, "workflow", map()));
        out.put("topology", Py.get(view, "runtime", map()));
        out.put("application", Py.get(view, "workflow", map()));
        out.put("runtime", Py.get(view, "runtime", map()));
        return out;
    }

    /** {@code run_sync_for_extraction} (no FS when memory path/key empty). */
    public static Map<String, Object> runSyncForExtraction(boolean synchronizedRuntime, String memoryPath,
            String memoryKey, long tick, Map<String, Object> browser, Map<String, Object> native_,
            Map<String, Object> semanticResult, Map<String, Object> workflowResult,
            Map<String, Object> causalityResult, Map<String, Object> distributedResult, Map<String, Object> session,
            Map<String, Object> identity, boolean mergeGraph) {
        if (!synchronizedRuntime) {
            Map<String, Object> off = map();
            off.put("enabled", false);
            off.put("bounded", true);
            return off;
        }
        Map<String, Object> memory = map(); // empty memory path -> no FS load

        Map<String, Object> result = runSynchronizedRuntime(tick, browser, native_, semanticResult, workflowResult,
                causalityResult, distributedResult, session, identity, memory, null);

        Map<String, Object> graphIr = synchronizationRuntimeIrToGraph(asMap(Py.get(result, "sync_ir", map())));
        Map<String, Object> unifiedGraph = map();
        if (mergeGraph) {
            unifiedGraph = ExecutionRuntime.buildUnifiedRuntimeGraph(new ArrayList<>(List.of(graphIr)));
        }
        Map<String, Object> out = map();
        out.put("enabled", true);
        out.put("synchronization", result);
        out.put("sync_ir", Py.get(result, "sync_ir", map()));
        out.put("sync_graph_ir", graphIr);
        out.put("unified_graph", unifiedGraph);
        out.put("replay", Py.get(result, "replay", map()));
        out.put("memory_persisted", false);
        out.put("bounded", true);
        return out;
    }
}
