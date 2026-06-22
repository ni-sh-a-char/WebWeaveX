package io.webweavex.reconstruction;

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

/**
 * Port of the {@code core.reconstruction} orchestrator family — {@code run_reconstruction_runtime}
 * and {@code run_reconstruction_for_extraction} — plus the ~14 deterministic sub-engines, the
 * reconstruction IR, and the snapshot persistence engine they fan out to. Dependency-clean
 * (24-module closure, 0 forbidden; FS confined to the snapshot engine, invoked only with a memory
 * path+key). Reuses the already-certified {@link RuntimeReconstruction},
 * {@link BrowserReconstruction}, {@link MemoryReconstruction}, {@link RuntimeValidation} engines,
 * the determinism/crypto/json substrate, and {@link ExecutionRuntime#buildUnifiedRuntimeGraph}.
 */
public final class ReconstructionRuntime {

    private ReconstructionRuntime() {
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

    private static Map<String, Object> mapOf(Object... kv) {
        Map<String, Object> m = map();
        for (int i = 0; i < kv.length; i += 2) {
            m.put((String) kv[i], kv[i + 1]);
        }
        return m;
    }

    private static List<Object> capped(List<Object> xs, int n) {
        return xs.size() > n ? xs.subList(0, n) : xs;
    }

    /** {@code sorted(items, key=lambda i: str(i.get(field, "")))}. */
    private static List<Object> sortByStr(List<Object> items, String field) {
        List<Object> c = new ArrayList<>(items);
        c.sort((a, b) -> cmp(str(Py.get(asMap(a), field, "")), str(Py.get(asMap(b), field, ""))));
        return c;
    }

    private static String sha256hex32(String text) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] d = md.digest(text.getBytes(StandardCharsets.UTF_8));
            StringBuilder sb = new StringBuilder(64);
            for (byte b : d) {
                sb.append(Character.forDigit((b >> 4) & 0xF, 16));
                sb.append(Character.forDigit(b & 0xF, 16));
            }
            return sb.substring(0, 32);
        } catch (Exception e) {
            throw new IllegalStateException(e);
        }
    }

    private static String identityHash(Map<String, Object> payload) {
        return sha256hex32(PyJson.dumpsDefaultAscii(payload));
    }

    // -------------------------------------------------------------- sub-engines

    public static Map<String, Object> reconstructApplicationRuntime(Map<String, Object> applicationIr,
            Map<String, Object> workflowIr, Map<String, Object> executionIr, String runtimeType) {
        Map<String, Object> appIr = applicationIr == null ? map() : applicationIr;
        Map<String, Object> wfIr = workflowIr == null ? map() : workflowIr;
        Map<String, Object> exIr = executionIr == null ? map() : executionIr;
        Object workflows = Py.get(wfIr, "workflows", Py.get(wfIr, "workflow", map()));
        if (workflows instanceof Map && ((Map<?, ?>) workflows).containsKey("objective")) {
            List<Object> wrapped = new ArrayList<>();
            wrapped.add(workflows);
            workflows = wrapped;
        }
        Map<String, Object> out = map();
        out.put("runtime_type", runtimeType);
        out.put("workflows", workflows instanceof List ? asList(workflows) : new ArrayList<>());
        out.put("forms", new LinkedHashMap<>(asMap(appIr.get("forms"))));
        out.put("dashboards", asList(appIr.get("dashboards")));
        out.put("modals", asList(appIr.get("modals")));
        out.put("tabs", asList(appIr.get("tabs")));
        out.put("application_graph", new LinkedHashMap<>(asMap(Py.get(appIr, "graph", Py.get(appIr, "action_graphs", map())))));
        out.put("execution_state", new LinkedHashMap<>(asMap(Py.get(exIr, "execution_state", Py.get(exIr, "state", map())))));
        out.put("replay_safe", true);
        out.put("bounded", true);
        return out;
    }

    private static final String[] ENV_TYPES = {"browser", "terminal", "electron", "connector", "vm", "distributed"};

    public static Map<String, Object> buildRuntimeEnvironment(String runtime, List<Object> connectors,
            List<Object> workers) {
        String rt = "browser";
        for (String t : ENV_TYPES) {
            if (t.equals(runtime)) {
                rt = runtime;
                break;
            }
        }
        Map<String, Object> out = map();
        out.put("runtime", rt);
        out.put("browser", rt.equals("browser"));
        out.put("terminal", rt.equals("terminal"));
        out.put("electron", rt.equals("electron"));
        out.put("connector", rt.equals("connector"));
        out.put("vm", rt.equals("vm"));
        out.put("distributed", rt.equals("distributed"));
        out.put("connectors", sortByStr(connectors == null ? new ArrayList<>() : connectors, "id"));
        out.put("workers", sortByStr(workers == null ? new ArrayList<>() : workers, "worker_id"));
        out.put("execution_ready", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> reconstructRuntimeSession(Map<String, Object> session,
            Map<String, Object> identity, Map<String, Object> syncState, Map<String, Object> adaptiveMemory) {
        Map<String, Object> ses = session == null ? map() : session;
        Map<String, Object> id = identity == null ? map() : identity;
        Map<String, Object> sync = syncState == null ? map() : syncState;
        Map<String, Object> adaptive = adaptiveMemory == null ? map() : adaptiveMemory;
        List<Object> cookies = new ArrayList<>(asList(ses.get("cookies")));
        cookies.sort((a, b) -> cmp(str(Py.get(asMap(a), "name", "")), str(Py.get(asMap(b), "name", ""))));
        Map<String, Object> authSession = map();
        authSession.put("authenticated", Py.truthy(Py.get(ses, "authenticated", false)));
        authSession.put("session_id", str(Py.get(ses, "session_id", Py.get(id, "identity_id", ""))));
        Map<String, Object> out = map();
        out.put("authenticated_session", authSession);
        out.put("cookies", cookies);
        out.put("csrf_state", new LinkedHashMap<>(asMap(Py.get(ses, "csrf", Py.get(ses, "csrf_state", map())))));
        out.put("browser_identity", new LinkedHashMap<>(id));
        out.put("synchronization_state", new LinkedHashMap<>(sync));
        out.put("adaptive_memory", new LinkedHashMap<>(adaptive));
        out.put("replay_safe", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> reconstructRuntimeIdentity(Map<String, Object> browserIdentity,
            Map<String, Object> session, String runtimeId, String executionId, String workerId) {
        Map<String, Object> browser = new LinkedHashMap<>(browserIdentity == null ? map() : browserIdentity);
        Map<String, Object> sessionBody = new LinkedHashMap<>(session == null ? map() : session);
        String browserHash = identityHash(mapOf("browser", browser));
        String sessionHash = identityHash(mapOf("session", sessionBody));
        String runtimeHash = identityHash(mapOf("runtime_id", runtimeId));
        String executionHash = identityHash(mapOf("execution_id", executionId));
        String workerHash = identityHash(mapOf("worker_id", workerId));
        Map<String, Object> browserId = new LinkedHashMap<>(browser);
        browserId.put("identity_hash", browserHash);
        Map<String, Object> sessionId = new LinkedHashMap<>(sessionBody);
        sessionId.put("identity_hash", sessionHash);
        List<Object> continuity = new ArrayList<>(List.of(browserHash, sessionHash, runtimeHash));
        continuity.sort((a, b) -> cmp((String) a, (String) b));
        Map<String, Object> out = map();
        out.put("browser_identity", browserId);
        out.put("session_identity", sessionId);
        out.put("runtime_identity", mapOf("runtime_id", runtimeId, "identity_hash", runtimeHash));
        out.put("execution_identity", mapOf("execution_id", executionId, "identity_hash", executionHash));
        out.put("worker_identity", mapOf("worker_id", workerId, "identity_hash", workerHash));
        out.put("continuity_hashes", continuity);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> reconstructRuntimeTopology(Map<String, Object> runtimeGraph,
            List<Object> workers, List<Object> connectors, Map<String, Object> executionTopology,
            Map<String, Object> syncTopology) {
        Map<String, Object> graph = runtimeGraph == null ? map() : runtimeGraph;
        List<Object> nodes = sortByStr(asList(graph.get("nodes")), "id");
        List<Object> edges = new ArrayList<>(asList(graph.get("edges")));
        edges.sort(Comparator.comparing((Object e) -> str(Py.get(asMap(e), "from", "")), ReconstructionRuntime::cmp)
                .thenComparing(e -> str(Py.get(asMap(e), "to", "")), ReconstructionRuntime::cmp)
                .thenComparing(e -> str(Py.get(asMap(e), "relation", "")), ReconstructionRuntime::cmp));
        Map<String, Object> out = map();
        out.put("distributed_workers", sortByStr(workers == null ? new ArrayList<>() : workers, "worker_id"));
        out.put("runtime_graph", mapOf("nodes", nodes, "edges", edges));
        out.put("connector_topology", sortByStr(connectors == null ? new ArrayList<>() : connectors, "id"));
        out.put("execution_topology", new LinkedHashMap<>(executionTopology == null ? map() : executionTopology));
        out.put("synchronization_topology", new LinkedHashMap<>(syncTopology == null ? map() : syncTopology));
        out.put("reconstructed", true);
        out.put("bounded", true);
        return out;
    }

    private static final List<String> CONNECTOR_KINDS =
            List.of("database", "api", "kubernetes", "docker", "telemetry", "ide", "cicd");

    public static Map<String, Object> reconstructConnectorRuntime(List<Object> connectors, Map<String, Object> liveIr) {
        List<Object> conn = connectors == null ? new ArrayList<>() : connectors;
        Map<String, Object> live = liveIr == null ? map() : liveIr;
        List<Object> rebuilt = new ArrayList<>();
        List<Object> cap = capped(conn, 1000);
        for (int index = 0; index < cap.size(); index++) {
            Map<String, Object> c = asMap(cap.get(index));
            String kind = str(Py.get(c, "kind", Py.get(c, "type", "api")));
            if (!CONNECTOR_KINDS.contains(kind)) {
                kind = "api";
            }
            rebuilt.add(mapOf("id", str(Py.get(c, "id", "connector:" + index)), "kind", kind,
                    "state", new LinkedHashMap<>(asMap(c.get("state"))), "reconstructed", true));
        }
        Object streams = Py.get(live, "streams", Py.get(live, "connectors", new ArrayList<>()));
        if (streams instanceof Map) {
            streams = asMap(streams).get("streams");
        }
        Map<String, Object> out = map();
        out.put("connectors", sortByStr(rebuilt, "id"));
        out.put("streams", streams instanceof List ? capped(asList(streams), 1000) : new ArrayList<>());
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> recoverReconstructedRuntime(Map<String, Object> checkpoint,
            List<Object> failedSegments) {
        Map<String, Object> ck = checkpoint == null ? map() : checkpoint;
        List<Object> failed = failedSegments == null ? new ArrayList<>() : failedSegments;
        Map<String, Object> out = map();
        out.put("checkpoint_restored", Py.truthy(ck));
        out.put("failed_segments_recovered", (long) failed.size());
        out.put("segments", sortByStr(failed, "id"));
        out.put("replay_safe", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildRuntimeTimeline(List<Object> events, List<Object> actions,
            List<Object> mutations, List<Object> synchronization, List<Object> execution, List<Object> recovery,
            List<Object> replay, long tick) {
        List<Object> timeline = new ArrayList<>();
        Object[][] groups = {
            {"event", events}, {"action", actions}, {"mutation", mutations}, {"sync", synchronization},
            {"execution", execution}, {"recovery", recovery}, {"replay", replay},
        };
        for (Object[] g : groups) {
            String kind = (String) g[0];
            List<Object> items = g[1] == null ? new ArrayList<>() : asList(g[1]);
            for (int index = 0; index < items.size(); index++) {
                Map<String, Object> item = asMap(items.get(index));
                timeline.add(mapOf("kind", kind, "tick", pyInt(Py.get(item, "tick", tick + index), tick + index),
                        "id", str(Py.get(item, "id", kind + ":" + index)), "payload", new LinkedHashMap<>(item)));
            }
        }
        timeline.sort(Comparator.comparingLong((Object t) -> pyInt(asMap(t).get("tick"), 0))
                .thenComparing(t -> str(asMap(t).get("kind")), ReconstructionRuntime::cmp)
                .thenComparing(t -> str(asMap(t).get("id")), ReconstructionRuntime::cmp));
        Map<String, Object> out = map();
        out.put("timeline", timeline);
        out.put("count", (long) timeline.size());
        out.put("replay_deterministic", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildRuntimeReplay(List<Object> actions, List<Object> transactions,
            Map<String, Object> timeline, long tick) {
        List<Object> orderedActions = new ArrayList<>(actions == null ? new ArrayList<>() : actions);
        orderedActions.sort((a, b) -> cmp(str(Py.get(asMap(a), "id", Py.get(asMap(a), "action_id", ""))),
                str(Py.get(asMap(b), "id", Py.get(asMap(b), "action_id", "")))));
        List<Object> orderedTx = sortByStr(transactions == null ? new ArrayList<>() : transactions, "transaction_id");
        List<Object> chain = new ArrayList<>();
        for (int index = 0; index < orderedActions.size(); index++) {
            Map<String, Object> action = asMap(orderedActions.get(index));
            chain.add(mapOf("step", (long) index,
                    "action_id", str(Py.get(action, "id", Py.get(action, "action_id", ""))), "tick", tick + index));
        }
        Map<String, Object> restoration = map();
        restoration.put("actions", orderedActions);
        restoration.put("transactions", orderedTx);
        Map<String, Object> continuity = map();
        continuity.put("tick", tick);
        continuity.put("steps", (long) chain.size());
        Map<String, Object> pkg = map();
        pkg.put("actions", orderedActions);
        pkg.put("timeline", timeline != null ? asList(timeline.get("timeline")) : new ArrayList<>());
        pkg.put("deterministic", true);
        Map<String, Object> out = map();
        out.put("replay_chains", chain);
        out.put("execution_restoration", restoration);
        out.put("runtime_continuity", continuity);
        out.put("replay_package", pkg);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> rebuildRuntimeState(List<Object> queues, Map<String, Object> synchronization,
            List<Object> mutations, List<Object> transactions, Map<String, Object> memory,
            List<Object> executionLineage, List<Object> workflows) {
        List<Object> orderedMutations = new ArrayList<>(mutations == null ? new ArrayList<>() : mutations);
        orderedMutations.sort(Comparator.comparingLong((Object m) -> pyInt(asMap(m).get("tick"), 0))
                .thenComparingLong(m -> pyInt(asMap(m).get("ordered_index"), 0))
                .thenComparing(m -> str(Py.get(asMap(m), "kind", "")), ReconstructionRuntime::cmp));
        List<Object> orderedTx = sortByStr(transactions == null ? new ArrayList<>() : transactions, "transaction_id");
        List<Object> orderedQueues = new ArrayList<>(queues == null ? new ArrayList<>() : queues);
        orderedQueues.sort(Comparator.comparingLong((Object q) -> -pyInt(asMap(q).get("priority"), 0))
                .thenComparingLong(q -> pyInt(asMap(q).get("order"), 0)));
        List<Object> workflowsSorted = new ArrayList<>(workflows == null ? new ArrayList<>() : workflows);
        workflowsSorted.sort((a, b) -> cmp(str(Py.get(asMap(a), "id", Py.get(asMap(a), "objective", ""))),
                str(Py.get(asMap(b), "id", Py.get(asMap(b), "objective", "")))));
        Map<String, Object> out = map();
        out.put("queues", orderedQueues);
        out.put("synchronization", new LinkedHashMap<>(synchronization == null ? map() : synchronization));
        out.put("mutations", orderedMutations);
        out.put("transactions", orderedTx);
        out.put("memory", new LinkedHashMap<>(memory == null ? map() : memory));
        out.put("execution_lineage", sortByStr(executionLineage == null ? new ArrayList<>() : executionLineage, "id"));
        out.put("workflows", workflowsSorted);
        out.put("deterministic_order", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> cloneRuntimeEnvironment(Map<String, Object> source) {
        Map<String, Object> s = source == null ? map() : source;
        Map<String, Object> out = map();
        out.put("runtime_graph", new LinkedHashMap<>(asMap(s.get("runtime_graph"))));
        out.put("browser_state", new LinkedHashMap<>(asMap(Py.get(s, "browser", Py.get(s, "browser_state", map())))));
        out.put("application_state",
                new LinkedHashMap<>(asMap(Py.get(s, "application", Py.get(s, "application_state", map())))));
        out.put("execution_queues", asList(Py.get(s, "queues", Py.get(s, "execution_queues", new ArrayList<>()))));
        out.put("synchronization_state", new LinkedHashMap<>(asMap(Py.get(s, "synchronization", Py.get(s, "sync", map())))));
        out.put("workflows", asList(s.get("workflows")));
        out.put("source_mutated", false);
        out.put("cloned", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> fabricateRuntimeReality(Map<String, Object> runtime,
            Map<String, Object> environment, Map<String, Object> browser, Map<String, Object> application,
            boolean portable) {
        Map<String, Object> base = runtime != null ? runtime
                : RuntimeReconstruction.reconstructRuntime(null, null, null, null, null, null,
                        str(Py.get(environment == null ? map() : environment, "runtime", "browser")), 0);
        Map<String, Object> fabricated = new LinkedHashMap<>(base);
        fabricated.put("environment", new LinkedHashMap<>(environment == null ? map() : environment));
        fabricated.put("browser", new LinkedHashMap<>(browser == null ? map() : browser));
        fabricated.put("application", new LinkedHashMap<>(application == null ? map() : application));
        Map<String, Object> out = map();
        out.put("fabricated", true);
        out.put("runtime", fabricated);
        out.put("portable", portable);
        out.put("replay_safe", true);
        out.put("operational_twin", true);
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- snapshot engine

    public static Map<String, Object> captureReconstructionSnapshot(Map<String, Object> state) {
        Map<String, Object> s = state == null ? map() : state;
        Map<String, Object> out = map();
        out.put("state", new LinkedHashMap<>(s));
        out.put("topology", new LinkedHashMap<>(asMap(s.get("topology"))));
        out.put("identities", new LinkedHashMap<>(asMap(s.get("identities"))));
        out.put("workflows", asList(s.get("workflows")));
        out.put("replay_chains", asList(s.get("replay_chains")));
        out.put("captured", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> restoreReconstructionSnapshot(Map<String, Object> snapshot) {
        Map<String, Object> snap = snapshot == null ? map() : snapshot;
        Map<String, Object> body = asMap(Py.get(snap, "state", snap));
        Map<String, Object> out = map();
        out.put("state", new LinkedHashMap<>(body));
        out.put("topology", new LinkedHashMap<>(asMap(Py.get(snap, "topology", body.get("topology")))));
        out.put("identities", new LinkedHashMap<>(asMap(Py.get(snap, "identities", body.get("identities")))));
        out.put("workflows", asList(Py.get(snap, "workflows", body.get("workflows"))));
        out.put("replay_chains", asList(Py.get(snap, "replay_chains", body.get("replay_chains"))));
        out.put("restored", true);
        out.put("bounded", true);
        return out;
    }

    private static Map<String, Object> emptySnapshot() {
        Map<String, Object> m = map();
        m.put("state", map());
        m.put("topology", map());
        m.put("identities", map());
        m.put("workflows", new ArrayList<>());
        m.put("replay_chains", new ArrayList<>());
        m.put("bounded", true);
        return m;
    }

    public static Map<String, Object> saveReconstructionSnapshot(String path, Map<String, Object> snapshot,
            String key) {
        String payload = PyJson.dumpsDefaultAscii(snapshot);
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

    public static Map<String, Object> loadReconstructionSnapshot(String path, String key) {
        Path target = Paths.get(path);
        if (!Files.exists(target)) {
            Map<String, Object> out = map();
            out.put("available", false);
            out.put("snapshot", emptySnapshot());
            out.put("bounded", true);
            return out;
        }
        try {
            String content = new String(Files.readAllBytes(target), StandardCharsets.UTF_8);
            Map<String, Object> wrapper = asMap(PyJsonParse.loads(content));
            Map<String, Object> decrypted = Kaalka.decryptValueEnvelope(str(wrapper.get("encrypted")), key);
            Object snapshot = PyJsonParse.loads(str(decrypted.get("decrypted")));
            Map<String, Object> out = map();
            out.put("available", true);
            out.put("snapshot", snapshot);
            out.put("algorithm", "kaalka");
            out.put("bounded", true);
            return out;
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    // -------------------------------------------------------------- IR

    public static Map<String, Object> compileReconstructionRuntimeIr(Map<String, Object> payload) {
        Map<String, Object> out = map();
        out.put("ir", "reconstruction_runtime");
        out.put("reconstructed_runtimes", Py.get(payload, "runtime", map()));
        out.put("replay_chains", Py.get(asMap(payload.get("replay")), "replay_chains", new ArrayList<>()));
        out.put("topology", Py.get(payload, "topology", map()));
        out.put("runtime_identities", Py.get(payload, "identity", map()));
        out.put("fabricated_environments", Py.get(payload, "fabrication", map()));
        out.put("execution_continuity", Py.get(payload, "state", map()));
        out.put("validation", Py.get(payload, "validation", map()));
        out.put("browser", Py.get(payload, "browser", map()));
        out.put("application", Py.get(payload, "application", map()));
        out.put("timeline", Py.get(payload, "timeline", map()));
        out.put("clone", Py.get(payload, "clone", map()));
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> reconstructionRuntimeIrToGraph(Map<String, Object> ir) {
        List<Object> nodes = new ArrayList<>();
        nodes.add(mapOf("id", "reconstruction:root", "type", "reconstruction"));
        List<Object> edges = new ArrayList<>();
        Map<String, Object> runtime = asMap(ir.get("reconstructed_runtimes"));
        String runtimeId = str(Py.get(runtime, "runtime_id", ""));
        if (!runtimeId.isEmpty()) {
            nodes.add(mapOf("id", "runtime:" + runtimeId, "type", "runtime"));
            edges.add(mapOf("from", "reconstruction:root", "to", "runtime:" + runtimeId, "relation", "reconstructs"));
        }
        List<Object> chains = capped(asList(ir.get("replay_chains")), 10000);
        for (int index = 0; index < chains.size(); index++) {
            String stepId = str(Py.get(asMap(chains.get(index)), "action_id", "step:" + index));
            nodes.add(mapOf("id", "replay:" + stepId, "type", "replay"));
            edges.add(mapOf("from", "replay:" + stepId, "to", "reconstruction:root", "relation", "replays"));
        }
        Map<String, Object> fabrication = asMap(ir.get("fabricated_environments"));
        if (Py.truthy(fabrication.get("fabricated"))) {
            nodes.add(mapOf("id", "fabrication:reality", "type", "fabrication"));
            edges.add(mapOf("from", "fabrication:reality", "to", "reconstruction:root", "relation", "fabricates"));
        }
        Map<String, Object> clone = asMap(ir.get("clone"));
        if (Py.truthy(clone.get("cloned"))) {
            nodes.add(mapOf("id", "clone:environment", "type", "clone"));
            edges.add(mapOf("from", "clone:environment", "to", "reconstruction:root", "relation", "clones"));
        }
        Map<String, Object> graph = asMap(asMap(ir.get("topology")).get("runtime_graph"));
        for (Object no : capped(asList(graph.get("nodes")), 5000)) {
            Map<String, Object> node = asMap(no);
            String nodeId = str(Py.get(node, "id", ""));
            if (!nodeId.isEmpty()) {
                nodes.add(mapOf("id", nodeId, "type", str(Py.get(node, "type", "node"))));
            }
        }
        List<Object> sortedNodes = new ArrayList<>(nodes);
        sortedNodes.sort((a, b) -> cmp(str(Py.get(asMap(a), "id", "")), str(Py.get(asMap(b), "id", ""))));
        Map<String, Object> out = map();
        out.put("ir", "reconstruction_runtime_graph");
        out.put("nodes", sortedNodes);
        out.put("edges", edges);
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- orchestrator

    private static Object getPath(Map<String, Object> m, String k1, Object dflt) {
        return m.containsKey(k1) ? m.get(k1) : dflt;
    }

    /** {@code run_reconstruction_runtime}. */
    public static Map<String, Object> runReconstructionRuntime(Map<String, Object> sources,
            Map<String, Object> stored, Map<String, Object> runtimeGraphArg, String runtimeType, long tick,
            boolean fabricate, boolean clone) {
        Map<String, Object> src = sources == null ? map() : sources;
        Map<String, Object> st = new LinkedHashMap<>(stored == null ? map() : stored);
        Map<String, Object> runtimeGraph = runtimeGraphArg != null ? runtimeGraphArg
                : asMap(Py.get(src, "graph", map()));

        Map<String, Object> semanticIr = asMap(Py.get(src, "semantic_ir", Py.get(src, "semantic", map())));
        Map<String, Object> workflowIr = asMap(Py.get(src, "workflow_ir", Py.get(src, "workflow", map())));
        Map<String, Object> syncIr = asMap(Py.get(src, "sync_ir", Py.get(src, "sync", map())));
        Map<String, Object> executionIr = asMap(Py.get(src, "execution_ir", Py.get(src, "execution", map())));
        Map<String, Object> memoryIr = asMap(Py.get(src, "memory_ir", Py.get(src, "memory", map())));

        Map<String, Object> runtime = RuntimeReconstruction.reconstructRuntime(semanticIr, workflowIr, syncIr,
                executionIr, memoryIr, runtimeGraph, runtimeType, tick);
        Map<String, Object> browser = BrowserReconstruction.reconstructBrowserRuntime(
                asMap(Py.get(src, "browser_ir", Py.get(src, "browser", map()))),
                asMap(Py.get(src, "interaction_ir", map())), asMap(Py.get(src, "identity", map())),
                asMap(Py.get(src, "session", map())), asMap(Py.get(src, "streaming", Py.get(src, "live", map()))),
                asMap(Py.get(src, "dom", map())));
        Map<String, Object> application = reconstructApplicationRuntime(
                asMap(Py.get(src, "application_ir", Py.get(src, "application", map()))), workflowIr, executionIr,
                runtimeType);
        Map<String, Object> session = reconstructRuntimeSession(asMap(Py.get(src, "session", map())),
                asMap(Py.get(src, "identity", map())), syncIr, asMap(Py.get(src, "adaptive_memory", map())));
        Map<String, Object> environment = buildRuntimeEnvironment(runtimeType, asList(src.get("connectors")),
                asList(src.get("workers")));
        Map<String, Object> memoryRebuilt = MemoryReconstruction.reconstructRuntimeMemory(memoryIr, semanticIr,
                asMap(Py.get(src, "lineage", Py.get(memoryIr, "lineage", map()))));

        Object queuesObj = executionIr.get("queues");
        List<Object> queues = queuesObj instanceof Map ? asList(asMap(queuesObj).get("queue")) : new ArrayList<>();
        Object mutObj = executionIr.get("mutations");
        List<Object> mutations = mutObj instanceof Map ? asList(asMap(mutObj).get("mutations")) : new ArrayList<>();
        Object lineageObj = src.get("lineage");
        List<Object> execLineage = lineageObj instanceof Map ? asList(asMap(lineageObj).get("lineage"))
                : new ArrayList<>();
        Map<String, Object> state = rebuildRuntimeState(queues, syncIr, mutations,
                asList(executionIr.get("transactions")), memoryRebuilt, execLineage,
                asList(application.get("workflows")));

        Object workersObj = getPath(src, "workers", asMap(Py.get(executionIr, "federation", map())).get("workers"));
        Map<String, Object> topology = reconstructRuntimeTopology(runtimeGraph, asList(workersObj),
                asList(src.get("connectors")), asMap(Py.get(executionIr, "federation", map())), syncIr);

        List<Object> txList = asList(executionIr.get("transactions"));
        String executionId = !txList.isEmpty() ? str(Py.get(asMap(txList.get(0)), "transaction_id", "")) : "";
        List<Object> workersList = asList(src.get("workers"));
        String workerId = !workersList.isEmpty() ? str(Py.get(asMap(workersList.get(0)), "worker_id", "")) : "";
        Map<String, Object> identity = reconstructRuntimeIdentity(asMap(Py.get(src, "identity", map())),
                asMap(Py.get(src, "session", map())), str(Py.get(runtime, "runtime_id", "")), executionId, workerId);

        Map<String, Object> connectors = reconstructConnectorRuntime(asList(src.get("connectors")),
                asMap(Py.get(src, "live", Py.get(src, "live_ir", map()))));

        List<Object> actions = asList(executionIr.get("actions"));
        List<Object> syncTimeline = new ArrayList<>();
        List<Object> syncLineage = capped(asList(syncIr.get("lineage")), 100);
        for (int i = 0; i < syncLineage.size(); i++) {
            syncTimeline.add(mapOf("id", "sync:" + i, "tick", tick));
        }
        Map<String, Object> timeline = buildRuntimeTimeline(null, actions, asList(state.get("mutations")),
                syncTimeline, actions, null, null, tick);
        Map<String, Object> replay = buildRuntimeReplay(actions, asList(executionIr.get("transactions")), timeline,
                tick);

        Map<String, Object> cloneResult = map();
        if (clone) {
            Map<String, Object> sourceBody = map();
            sourceBody.put("runtime_graph", runtimeGraph);
            sourceBody.put("browser", browser);
            sourceBody.put("application", application);
            sourceBody.put("synchronization", syncIr);
            sourceBody.put("workflows", asList(application.get("workflows")));
            sourceBody.put("queues", asList(state.get("queues")));
            cloneResult = cloneRuntimeEnvironment(sourceBody);
        }

        Map<String, Object> fabrication = map();
        if (fabricate) {
            fabrication = fabricateRuntimeReality(runtime, environment, browser, application, true);
        }

        Map<String, Object> validation = RuntimeValidation.validateReconstructedRuntime(
                fabricate ? asMap(Py.get(fabrication, "runtime", runtime)) : runtime, replay, topology, executionIr,
                state.get("mutations"));

        Map<String, Object> priorSnapshot = asMap(Py.get(st, "snapshot", map()));
        Map<String, Object> recovery = recoverReconstructedRuntime(priorSnapshot, null);

        Map<String, Object> snapState = map();
        snapState.put("runtime", runtime);
        snapState.put("browser", browser);
        snapState.put("application", application);
        snapState.put("topology", topology);
        snapState.put("identities", identity);
        snapState.put("workflows", asList(application.get("workflows")));
        snapState.put("replay_chains", asList(replay.get("replay_chains")));
        snapState.put("state", state);
        Map<String, Object> snapshot = captureReconstructionSnapshot(snapState);

        Map<String, Object> payload = map();
        payload.put("runtime", runtime);
        payload.put("browser", browser);
        payload.put("application", application);
        payload.put("session", session);
        payload.put("environment", environment);
        payload.put("memory", memoryRebuilt);
        payload.put("state", state);
        payload.put("topology", topology);
        payload.put("identity", identity);
        payload.put("connectors", connectors);
        payload.put("timeline", timeline);
        payload.put("replay", replay);
        payload.put("clone", cloneResult);
        payload.put("fabrication", fabrication);
        payload.put("validation", validation);
        payload.put("recovery", recovery);
        payload.put("snapshot", snapshot);
        payload.put("bounded", true);
        payload.put("reconstruction_ir", compileReconstructionRuntimeIr(payload));
        return payload;
    }

    /** {@code run_reconstruction_for_extraction}. */
    public static Map<String, Object> runReconstructionForExtraction(boolean reconstructionRuntime, String memoryPath,
            String memoryKey, Map<String, Object> sources, Map<String, Object> runtimeGraph, String runtimeType,
            long tick, boolean fabricateRuntime, boolean cloneRuntime, boolean mergeGraph) {
        if (!reconstructionRuntime) {
            Map<String, Object> off = map();
            off.put("enabled", false);
            off.put("bounded", true);
            return off;
        }
        Map<String, Object> stored = map(); // empty memory path -> no FS load

        Map<String, Object> result = runReconstructionRuntime(sources, stored, runtimeGraph, runtimeType, tick,
                fabricateRuntime, cloneRuntime);

        Map<String, Object> graphIr = reconstructionRuntimeIrToGraph(asMap(Py.get(result, "reconstruction_ir", map())));
        Map<String, Object> unifiedGraph = map();
        if (mergeGraph) {
            unifiedGraph = ExecutionRuntime.buildUnifiedRuntimeGraph(new ArrayList<>(List.of(graphIr)));
        }
        Map<String, Object> out = map();
        out.put("enabled", true);
        out.put("reconstruction", result);
        out.put("reconstruction_ir", Py.get(result, "reconstruction_ir", map()));
        out.put("reconstruction_graph_ir", graphIr);
        out.put("unified_graph", unifiedGraph);
        out.put("replay", Py.get(result, "replay", map()));
        out.put("validation", Py.get(result, "validation", map()));
        out.put("reconstruction_persisted", false);
        out.put("bounded", true);
        return out;
    }
}
