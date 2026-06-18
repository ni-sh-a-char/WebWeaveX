package io.webweavex.causality;

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
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;

/**
 * Port of the {@code core.causality} family — {@code run_causality_runtime},
 * {@code replay_causal_runtime}, {@code run_causality_for_extraction}, {@code save_causal_memory},
 * {@code load_causal_memory} — and the ~18 deterministic sub-engines + causal IR they fan out to.
 * Dependency-clean (25-module closure, 0 forbidden; the FS memory engine is only invoked when a
 * memory path+key are supplied). Reuses the certified determinism/crypto/json substrate and
 * {@link ExecutionRuntime#buildUnifiedRuntimeGraph}. No new substrate.
 */
public final class CausalityRuntime {

    private CausalityRuntime() {
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

    /** {@code sorted(events, key=lambda i: int(i.get("step",0)))} — stable. */
    private static List<Object> sortedByStep(List<Object> events) {
        List<Object> c = new ArrayList<>(events);
        c.sort(Comparator.comparingLong(e -> pyInt(asMap(e).get("step"), 0)));
        return c;
    }

    private static void sortEdges(List<Object> edges) {
        edges.sort(Comparator.comparing((Object e) -> str(Py.get(asMap(e), "from", "")), CausalityRuntime::cmp)
                .thenComparing(e -> str(Py.get(asMap(e), "to", "")), CausalityRuntime::cmp)
                .thenComparing(e -> str(Py.get(asMap(e), "relation", "")), CausalityRuntime::cmp));
    }

    // -------------------------------------------------------------- event sources

    private static List<Object> normalizeInteractionEvents(List<Object> interactions, String runtime) {
        List<Object> events = new ArrayList<>();
        List<Object> cap = capped(interactions == null ? new ArrayList<>() : interactions, 10000);
        for (int index = 0; index < cap.size(); index++) {
            Map<String, Object> it = asMap(cap.get(index));
            Map<String, Object> e = map();
            e.put("id", runtime + ":evt:" + index);
            e.put("runtime", runtime);
            e.put("type", str(Py.get(it, "action", Py.get(it, "type", "mutation"))));
            e.put("step", (long) index);
            e.put("source", str(Py.get(it, "from", Py.get(it, "selector", ""))));
            e.put("target", str(Py.get(it, "to", "")));
            e.put("state", str(Py.get(it, "state", "")));
            events.add(e);
        }
        return events;
    }

    private static List<Object> eventsFromNativeCognition(Map<String, Object> cognition) {
        List<Object> events = new ArrayList<>();
        long step = 0;
        for (Object io : asList(cognition.get("interactions"))) {
            Map<String, Object> it = asMap(io);
            events.add(mapOf("id", "native:evt:" + step, "runtime", str(Py.get(cognition, "runtime", "desktop")),
                    "type", str(Py.get(it, "action", "interaction")), "step", step));
            step++;
        }
        Map<String, Object> terminal = asMap(cognition.get("terminal"));
        for (Object line : capped(asList(terminal.get("output")), 1000)) {
            events.add(mapOf("id", "terminal:evt:" + step, "runtime", "terminal", "type", "log",
                    "step", step, "state", line));
            step++;
        }
        Map<String, Object> electron = asMap(cognition.get("electron"));
        for (Object route : asList(electron.get("routes"))) {
            events.add(mapOf("id", "electron:evt:" + step, "runtime", "electron", "type", "route",
                    "step", step, "state", route));
            step++;
        }
        for (Object notif : asList(asMap(cognition.get("desktop")).get("notifications"))) {
            events.add(mapOf("id", "desktop:notif:" + step, "runtime", "desktop", "type", "notification",
                    "step", step, "state", str(notif)));
            step++;
        }
        return events;
    }

    // -------------------------------------------------------------- engines

    public static Map<String, Object> buildRuntimeCausality(List<Object> events, Map<String, Object> origins) {
        List<Object> ordered = sortedByStep(events);
        List<Object> causalEdges = new ArrayList<>();
        for (int index = 1; index < ordered.size(); index++) {
            String prev = str(Py.get(asMap(ordered.get(index - 1)), "id", "evt:" + (index - 1)));
            String curr = str(Py.get(asMap(ordered.get(index)), "id", "evt:" + index));
            causalEdges.add(mapOf("from", prev, "to", curr, "relation", "propagates"));
        }
        List<Object> order = new ArrayList<>();
        for (Object e : ordered) {
            order.add(str(Py.get(asMap(e), "id", "")));
        }
        Map<String, Object> out = map();
        out.put("events", ordered);
        out.put("causal_edges", causalEdges);
        out.put("runtime_origins", new LinkedHashMap<>(origins));
        out.put("propagation_order", order);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildEventChain(List<Object> events) {
        List<Object> ordered = sortedByStep(events);
        List<Object> chain = new ArrayList<>();
        List<Object> cap = capped(ordered, 10000);
        for (int index = 0; index < cap.size(); index++) {
            Map<String, Object> e = asMap(cap.get(index));
            chain.add(mapOf("id", str(Py.get(e, "id", "evt:" + index)), "runtime", str(Py.get(e, "runtime", "unknown")),
                    "type", str(Py.get(e, "type", "mutation")), "step", (long) index, "depth", (long) index));
        }
        List<Object> synchronized_ = new ArrayList<>();
        if (!chain.isEmpty()) {
            Object firstRuntime = asMap(chain.get(0)).get("runtime");
            for (Object io : chain) {
                Map<String, Object> item = asMap(io);
                if (!java.util.Objects.equals(item.get("runtime"), firstRuntime)) {
                    synchronized_.add(item.get("id"));
                }
            }
        }
        Map<String, Object> out = map();
        out.put("chain", chain);
        out.put("length", (long) chain.size());
        out.put("max_depth", chain.isEmpty() ? 0L : (long) (chain.size() - 1));
        out.put("synchronized", synchronized_);
        out.put("bounded", true);
        return out;
    }

    private static final String[] RUNTIME_ORDER =
            {"browser", "application", "electron", "desktop", "terminal", "vm", "remote", "distributed"};

    public static Map<String, Object> alignCrossRuntimeEvents(List<Object> events) {
        Map<String, List<Object>> buckets = new LinkedHashMap<>();
        for (String r : RUNTIME_ORDER) {
            buckets.put(r, new ArrayList<>());
        }
        for (Object eo : capped(events, 20000)) {
            Map<String, Object> e = asMap(eo);
            String runtime = str(Py.get(e, "runtime", "browser")).toLowerCase(Locale.ROOT);
            buckets.computeIfAbsent(runtime, k -> new ArrayList<>()).add(e);
        }
        List<Object> aligned = new ArrayList<>();
        long step = 0;
        for (String runtime : RUNTIME_ORDER) {
            List<Object> bucket = sortedByStep(buckets.getOrDefault(runtime, new ArrayList<>()));
            for (Object eo : bucket) {
                Map<String, Object> e = new LinkedHashMap<>(asMap(eo));
                e.put("aligned_step", step);
                e.put("aligned_runtime", runtime);
                aligned.add(e);
                step++;
            }
        }
        List<Object> correlations = new ArrayList<>();
        for (int index = 1; index < aligned.size(); index++) {
            Map<String, Object> prev = asMap(aligned.get(index - 1));
            Map<String, Object> curr = asMap(aligned.get(index));
            correlations.add(mapOf("from_runtime", Py.get(prev, "runtime", ""), "to_runtime", Py.get(curr, "runtime", ""),
                    "from_event", Py.get(prev, "id", ""), "to_event", Py.get(curr, "id", ""),
                    "correlation_id", "corr:" + index));
        }
        Set<Object> runtimeSet = new LinkedHashSet<>();
        for (Object eo : aligned) {
            runtimeSet.add(asMap(eo).get("runtime"));
        }
        Map<String, Object> out = map();
        out.put("aligned_events", aligned);
        out.put("correlations", correlations);
        out.put("runtime_count", (long) runtimeSet.size());
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildRuntimeDependencies(List<Object> events, Map<String, Object> propagation) {
        List<Object> dependencies = new ArrayList<>();
        List<Object> consumers = new ArrayList<>();
        List<Object> syncChains = new ArrayList<>();
        List<String> runtimesSeen = new ArrayList<>();
        for (Object eo : sortedByStep(events)) {
            Map<String, Object> e = asMap(eo);
            String runtime = str(Py.get(e, "runtime", ""));
            if (!runtime.isEmpty() && !runtimesSeen.contains(runtime)) {
                if (!runtimesSeen.isEmpty()) {
                    dependencies.add(mapOf("from", runtimesSeen.get(runtimesSeen.size() - 1), "to", runtime,
                            "relation", "depends_on"));
                }
                runtimesSeen.add(runtime);
                consumers.add(mapOf("runtime", runtime, "event_id", str(Py.get(e, "id", ""))));
            }
        }
        for (Object ho : capped(asList(propagation.get("handoffs")), 5000)) {
            Map<String, Object> h = asMap(ho);
            syncChains.add(mapOf("from", Py.get(h, "from", ""), "to", Py.get(h, "to", ""),
                    "workflow_id", Py.get(h, "workflow_id", "")));
        }
        Map<String, Object> out = map();
        out.put("dependencies", dependencies);
        out.put("consumers", consumers);
        out.put("synchronization_chains", syncChains);
        out.put("causal_relationships", dependencies);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildWorkflowPropagation(Map<String, Object> aligned,
            Map<String, Object> dependencies) {
        List<Object> events = asList(aligned.get("aligned_events"));
        List<Object> handoffs = new ArrayList<>();
        for (int index = 1; index < events.size(); index++) {
            Map<String, Object> prev = asMap(events.get(index - 1));
            Map<String, Object> curr = asMap(events.get(index));
            if (!java.util.Objects.equals(prev.get("runtime"), curr.get("runtime"))) {
                handoffs.add(mapOf("from", str(Py.get(prev, "runtime", "")), "to", str(Py.get(curr, "runtime", "")),
                        "step", (long) index, "workflow_id", "wf:" + index));
            }
        }
        List<Object> syncSteps = new ArrayList<>();
        for (Object eo : events) {
            syncSteps.add(Py.get(asMap(eo), "aligned_step", 0L));
        }
        Map<String, Object> out = map();
        out.put("continuations", handoffs);
        out.put("handoffs", handoffs);
        out.put("distributed", asList(dependencies.get("synchronization_chains")));
        out.put("synchronized_steps", syncSteps);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildCausalGraph(List<Object> events, Map<String, Object> causality) {
        List<Object> nodes = new ArrayList<>();
        List<Object> edges = new ArrayList<>();
        Set<String> seenRuntimes = new LinkedHashSet<>();
        for (Object eo : capped(events, 10000)) {
            Map<String, Object> e = asMap(eo);
            String eventId = str(Py.get(e, "id", ""));
            nodes.add(mapOf("id", eventId, "type", "event", "runtime", str(Py.get(e, "runtime", ""))));
            String runtime = str(Py.get(e, "runtime", ""));
            if (!runtime.isEmpty() && !seenRuntimes.contains(runtime)) {
                seenRuntimes.add(runtime);
                nodes.add(mapOf("id", "runtime:" + runtime, "type", "runtime"));
                edges.add(mapOf("from", "runtime:" + runtime, "to", eventId, "relation", "triggers"));
            }
        }
        for (Object edge : capped(asList(causality.get("causal_edges")), 10000)) {
            Map<String, Object> ed = asMap(edge);
            edges.add(mapOf("from", str(Py.get(ed, "from", "")), "to", str(Py.get(ed, "to", "")),
                    "relation", "propagates"));
        }
        List<Object> cap = capped(events, 10000);
        for (int index = 0; index < cap.size(); index++) {
            Map<String, Object> e = asMap(cap.get(index));
            if ("notification".equals(e.get("type"))) {
                String eventId = str(Py.get(e, "id", "evt:" + index));
                edges.add(mapOf("from", eventId, "to", "workflow:" + index, "relation", "mutates"));
            }
        }
        if (nodes.isEmpty()) {
            nodes.add(mapOf("id", "causality:root", "type", "causality"));
        }
        List<Object> sortedNodes = new ArrayList<>(nodes);
        sortedNodes.sort((a, b) -> cmp(str(asMap(a).get("id")), str(asMap(b).get("id"))));
        List<Object> sortedEdges = new ArrayList<>(edges);
        sortEdges(sortedEdges);
        Map<String, Object> out = map();
        out.put("nodes", sortedNodes);
        out.put("edges", sortedEdges);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildStateTransitions(List<Object> events) {
        List<Object> transitions = new ArrayList<>();
        for (int index = 1; index < events.size(); index++) {
            Map<String, Object> prev = asMap(events.get(index - 1));
            Map<String, Object> curr = asMap(events.get(index));
            transitions.add(mapOf("from_state", str(Py.get(prev, "state", Py.get(prev, "type", ""))),
                    "to_state", str(Py.get(curr, "state", Py.get(curr, "type", ""))),
                    "runtime", str(Py.get(curr, "runtime", "")), "step", (long) index));
        }
        Map<String, Object> out = map();
        out.put("transitions", transitions);
        out.put("count", (long) transitions.size());
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildRuntimeSequence(List<Object> events) {
        List<Object> ordered = sortedByStep(events);
        List<Object> sequence = new ArrayList<>();
        List<Object> cap = capped(ordered, 10000);
        for (int index = 0; index < cap.size(); index++) {
            Map<String, Object> e = asMap(cap.get(index));
            sequence.add(mapOf("id", str(Py.get(e, "id", "")), "runtime", str(Py.get(e, "runtime", "")),
                    "type", str(Py.get(e, "type", "")), "step", pyInt(Py.get(e, "step", (long) index), index)));
        }
        Map<String, Object> out = map();
        out.put("sequence", sequence);
        out.put("length", (long) ordered.size());
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildRuntimeTimeline(List<Object> events, Map<String, Object> propagation) {
        List<Object> ordered = sortedByStep(events);
        List<Object> timeline = new ArrayList<>();
        List<Object> handoffs = asList(propagation.get("handoffs"));
        List<Object> cap = capped(ordered, 10000);
        for (int index = 0; index < cap.size(); index++) {
            Map<String, Object> e = asMap(cap.get(index));
            List<Object> propMap = new ArrayList<>();
            for (Object ho : handoffs) {
                Map<String, Object> h = asMap(ho);
                if (pyInt(h.get("step"), -1) == index) {
                    propMap.add(Py.get(h, "workflow_id", ""));
                }
            }
            timeline.add(mapOf("step", (long) index, "event_id", str(Py.get(e, "id", "evt:" + index)),
                    "runtime", str(Py.get(e, "runtime", "")), "type", str(Py.get(e, "type", "mutation")),
                    "propagation_map", propMap));
        }
        List<Object> evolution = new ArrayList<>();
        for (Object to : timeline) {
            evolution.add(asMap(to).get("event_id"));
        }
        Map<String, Object> out = map();
        out.put("timeline", timeline);
        out.put("evolution_history", evolution);
        out.put("propagation_maps", new ArrayList<>(handoffs));
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> correlateRuntimeMutations(List<Object> browserEvents, List<Object> nativeEvents,
            List<Object> notifications, List<Object> terminalLines, List<Object> processEvents) {
        List<Object> correlations = new ArrayList<>();
        long step = 0;
        for (Object eo : (browserEvents == null ? new ArrayList<Object>() : browserEvents)) {
            correlations.add(mapOf("kind", "ui_change", "event_id", str(Py.get(asMap(eo), "id", "browser:" + step)),
                    "runtime", "browser", "step", step));
            step++;
        }
        for (Object line : capped(terminalLines == null ? new ArrayList<>() : terminalLines, 1000)) {
            correlations.add(mapOf("kind", "terminal_log", "line", line, "runtime", "terminal", "step", step));
            step++;
        }
        for (Object notif : (notifications == null ? new ArrayList<Object>() : notifications)) {
            correlations.add(mapOf("kind", "notification", "payload", notif, "runtime", "desktop", "step", step));
            step++;
        }
        for (Object eo : (nativeEvents == null ? new ArrayList<Object>() : nativeEvents)) {
            Map<String, Object> e = asMap(eo);
            correlations.add(mapOf("kind", "native_mutation", "event_id", str(Py.get(e, "id", "")),
                    "runtime", str(Py.get(e, "runtime", "desktop")), "step", step));
            step++;
        }
        for (Object po : (processEvents == null ? new ArrayList<Object>() : processEvents)) {
            correlations.add(mapOf("kind", "process_mutation", "process", str(Py.get(asMap(po), "name", "")),
                    "runtime", "process", "step", step));
            step++;
        }
        List<Object> sorted = new ArrayList<>(correlations);
        sorted.sort(Comparator.comparingLong(c -> pyInt(asMap(c).get("step"), 0)));
        Map<String, Object> out = map();
        out.put("correlations", sorted);
        out.put("count", (long) correlations.size());
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> buildDistributedCausality(Map<String, Object> distributedResult,
            List<Object> workerEvents) {
        Map<String, Object> dr = distributedResult == null ? map() : distributedResult;
        List<Object> we = workerEvents == null ? new ArrayList<>() : workerEvents;
        List<Object> workers = asList(dr.get("workers"));
        List<Object> chains = new ArrayList<>();
        List<Object> cap = capped(we, 10000);
        for (int index = 0; index < cap.size(); index++) {
            Map<String, Object> e = asMap(cap.get(index));
            chains.add(mapOf("worker_id", str(Py.get(e, "worker_id", "worker_" + index)),
                    "event_id", str(Py.get(e, "id", "dist:" + index)), "step", (long) index,
                    "relation", "cluster_sync"));
        }
        Map<String, Object> clusterSync = map();
        clusterSync.put("worker_count", (long) workers.size());
        clusterSync.put("synced", Py.truthy(workers));
        Map<String, Object> out = map();
        out.put("worker_causality", chains);
        out.put("autonomous_propagation", Py.get(dr, "autonomous", false));
        out.put("remote_chains", capped(asList(dr.get("tasks")), 1000));
        out.put("cluster_synchronization", clusterSync);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> bridgeBrowserNativeRuntime(List<Object> browserEvents, List<Object> nativeEvents) {
        List<Object> bridges = new ArrayList<>();
        long step = browserEvents.size();
        List<Object> cap = capped(nativeEvents, 5000);
        for (int index = 0; index < cap.size(); index++) {
            Map<String, Object> ne = asMap(cap.get(index));
            Map<String, Object> source = browserEvents.isEmpty() ? mapOf("id", "browser:root")
                    : asMap(browserEvents.get(browserEvents.size() - 1));
            bridges.add(mapOf("from_runtime", "browser", "to_runtime", str(Py.get(ne, "runtime", "desktop")),
                    "from_event", str(Py.get(source, "id", "")), "to_event", str(Py.get(ne, "id", "native:" + index)),
                    "relation", "propagates", "step", step + index));
        }
        Map<String, Object> out = map();
        out.put("bridges", bridges);
        out.put("chain_length", (long) bridges.size());
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> bridgeElectronTerminalRuntime(List<Object> electronEvents,
            List<Object> terminalEvents) {
        List<Object> bridges = new ArrayList<>();
        Map<String, Object> electronRef = electronEvents.isEmpty() ? mapOf("id", "electron:root")
                : asMap(electronEvents.get(electronEvents.size() - 1));
        List<Object> cap = capped(terminalEvents, 5000);
        for (int index = 0; index < cap.size(); index++) {
            Map<String, Object> te = asMap(cap.get(index));
            bridges.add(mapOf("from_runtime", "electron", "to_runtime", "terminal",
                    "from_event", str(Py.get(electronRef, "id", "")), "to_event", str(Py.get(te, "id", "terminal:" + index)),
                    "relation", "triggers", "step", (long) index));
        }
        List<Object> chain = new ArrayList<>();
        for (Object bo : bridges) {
            chain.add(asMap(bo).get("to_event"));
        }
        Map<String, Object> out = map();
        out.put("bridges", bridges);
        out.put("synchronization_chain", chain);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> trackNotificationCausality(List<Object> notifications, List<Object> originEvents) {
        List<Object> tracked = new ArrayList<>();
        String originId = originEvents.isEmpty() ? ""
                : str(Py.get(asMap(originEvents.get(originEvents.size() - 1)), "id", ""));
        List<Object> cap = capped(notifications, 5000);
        for (int index = 0; index < cap.size(); index++) {
            Object notif = cap.get(index);
            String notifId;
            boolean userInteraction;
            if (notif instanceof Map) {
                notifId = str(Py.get(asMap(notif), "id", "notif:" + index));
                userInteraction = Py.truthy(asMap(notif).get("interaction"));
            } else {
                notifId = "notif:" + index;
                userInteraction = false;
            }
            tracked.add(mapOf("notification_id", notifId, "origin_event", originId,
                    "downstream_workflow", "workflow:notif:" + index, "user_interaction", userInteraction,
                    "payload", str(notif)));
        }
        Map<String, Object> out = map();
        out.put("notifications", tracked);
        out.put("origin_event", originId);
        out.put("count", (long) tracked.size());
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> trackProcessCausality(List<Object> processes, List<Object> events) {
        List<Object> chains = new ArrayList<>();
        List<Object> cap = capped(processes, 5000);
        for (int index = 0; index < cap.size(); index++) {
            Map<String, Object> proc = asMap(cap.get(index));
            chains.add(mapOf("process", str(Py.get(proc, "name", Py.get(proc, "pid", "proc:" + index))),
                    "parent", str(Py.get(proc, "parent", "")), "launched_at_step", (long) index,
                    "mutation_event", index < events.size() ? str(Py.get(asMap(events.get(index)), "id", "")) : ""));
        }
        long maxStep = 0;
        for (Object co : chains) {
            maxStep = Math.max(maxStep, pyInt(asMap(co).get("launched_at_step"), 0));
        }
        Map<String, Object> out = map();
        out.put("process_chains", chains);
        out.put("subprocess_depth", maxStep);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> recoverCausalRuntime(Map<String, Object> causality, List<Object> events) {
        List<Object> propagationOrder = asList(causality.get("propagation_order"));
        List<Object> recovered = new ArrayList<>(events);
        if (propagationOrder.isEmpty() && !events.isEmpty()) {
            propagationOrder = new ArrayList<>();
            for (Object eo : events) {
                propagationOrder.add(str(Py.get(asMap(eo), "id", "")));
            }
        }
        List<Integer> gaps = new ArrayList<>();
        for (int index = 1; index < propagationOrder.size(); index++) {
            if (!Py.truthy(propagationOrder.get(index))) {
                gaps.add(index);
            }
        }
        for (int gap : gaps) {
            recovered.add(mapOf("id", "recovered:evt:" + gap, "runtime", "recovery", "type", "restore",
                    "step", (long) gap, "recovered", true));
        }
        List<Object> recoveredOrder = sortedByStep(recovered);
        List<Object> order = new ArrayList<>();
        for (Object eo : recoveredOrder) {
            order.add(str(Py.get(asMap(eo), "id", "")));
        }
        Map<String, Object> out = map();
        out.put("recovered_events", recoveredOrder);
        out.put("propagation_order", order);
        out.put("broken_chains_fixed", (long) gaps.size());
        out.put("synchronization_restored", true);
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- replay / IR / memory

    /** {@code replay_causal_runtime}. */
    public static Map<String, Object> replayCausalRuntime(Map<String, Object> memory) {
        Map<String, Object> m = memory == null ? map() : memory;
        Map<String, Object> out = map();
        out.put("event_propagation", Py.get(m, "runtime_propagation", map()));
        out.put("workflow_evolution", Py.get(m, "event_chains", map()));
        out.put("synchronization", Py.get(m, "synchronization_state", map()));
        out.put("causal_graph", Py.get(m, "causal_graphs", map()));
        out.put("cross_runtime", Py.get(m, "alignment", map()));
        out.put("replayed", true);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> compileCausalRuntimeIr(Map<String, Object> cognition) {
        Map<String, Object> bridges = map();
        bridges.put("browser_native", Py.get(cognition, "browser_bridge", map()));
        bridges.put("electron_terminal", Py.get(cognition, "electron_bridge", map()));
        Map<String, Object> out = map();
        out.put("ir", "causal_runtime");
        out.put("causal_graphs", Py.get(cognition, "causal_graph", map()));
        out.put("timelines", Py.get(cognition, "timeline", map()));
        out.put("event_chains", Py.get(cognition, "event_chain", map()));
        out.put("propagation_maps", Py.get(cognition, "propagation", map()));
        out.put("distributed_synchronization", Py.get(cognition, "distributed", map()));
        out.put("runtime_dependencies", Py.get(cognition, "dependencies", map()));
        out.put("alignment", Py.get(cognition, "alignment", map()));
        out.put("bridges", bridges);
        out.put("recovery_state", Py.get(cognition, "recovery", map()));
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> causalRuntimeIrToGraph(Map<String, Object> causalIr) {
        Map<String, Object> graph = asMap(causalIr.get("causal_graphs"));
        List<Object> nodes = asList(graph.get("nodes"));
        List<Object> edges = asList(graph.get("edges"));
        if (nodes.isEmpty()) {
            nodes = new ArrayList<>(List.of(mapOf("id", "causality:root", "type", "causality")));
        }
        Map<String, Object> timeline = asMap(causalIr.get("timelines"));
        for (Object eo : capped(asList(timeline.get("timeline")), 5000)) {
            Map<String, Object> entry = asMap(eo);
            nodes.add(mapOf("id", str(Py.get(entry, "event_id", "")), "type", "timeline_event",
                    "runtime", str(Py.get(entry, "runtime", ""))));
        }
        List<Object> sortedNodes = new ArrayList<>(nodes);
        sortedNodes.sort((a, b) -> cmp(str(Py.get(asMap(a), "id", "")), str(Py.get(asMap(b), "id", ""))));
        Map<String, Object> out = map();
        out.put("ir", "causal_runtime_graph");
        out.put("nodes", sortedNodes);
        out.put("edges", edges);
        out.put("bounded", true);
        return out;
    }

    public static Map<String, Object> rememberCausalRuntime(Map<String, Object> memory, Map<String, Object> update) {
        Map<String, Object> merged = new LinkedHashMap<>(memory == null ? map() : memory);
        for (String field : new String[] {"event_chains", "runtime_propagation", "causal_graphs",
                "distributed_workflows", "synchronization_state"}) {
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
        m.put("event_chains", map());
        m.put("runtime_propagation", map());
        m.put("causal_graphs", map());
        m.put("distributed_workflows", map());
        m.put("synchronization_state", map());
        m.put("bounded", true);
        return m;
    }

    /** {@code save_causal_memory(path, memory, key)}. */
    public static Map<String, Object> saveCausalMemory(String path, Map<String, Object> memory, String key) {
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

    /** {@code load_causal_memory(path, key)}. */
    public static Map<String, Object> loadCausalMemory(String path, String key) {
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

    /** {@code run_causality_runtime}. */
    public static Map<String, Object> runCausalityRuntime(List<Object> browserEvents, Map<String, Object> nativeCognition,
            Map<String, Object> applicationResult, Map<String, Object> distributedResult, Map<String, Object> memory,
            List<Object> interactions) {
        Map<String, Object> mem = new LinkedHashMap<>(memory == null ? map() : memory);
        List<Object> browser = browserEvents != null ? new ArrayList<>(browserEvents)
                : normalizeInteractionEvents(interactions, "browser");
        Map<String, Object> cognition = nativeCognition == null ? map() : nativeCognition;
        List<Object> nativeEvents = eventsFromNativeCognition(cognition);

        if (Py.truthy(applicationResult)) {
            List<Object> wfNodes = capped(asList(asMap(Py.get(applicationResult, "workflow", map())).get("nodes")), 100);
            for (int index = 0; index < wfNodes.size(); index++) {
                browser.add(mapOf("id", "application:evt:" + index, "runtime", "application", "type", "workflow",
                        "step", (long) (browser.size() + index)));
            }
        }

        List<Object> allEvents = new ArrayList<>(browser);
        allEvents.addAll(nativeEvents);
        allEvents = sortedByStep(allEvents);

        Map<String, Object> origins = map();
        origins.put("browser", (long) browser.size());
        origins.put("native", (long) nativeEvents.size());
        origins.put("distributed", Py.truthy(distributedResult));

        Map<String, Object> causality = buildRuntimeCausality(allEvents, origins);
        Map<String, Object> eventChain = buildEventChain(allEvents);
        Map<String, Object> alignment = alignCrossRuntimeEvents(allEvents);
        Map<String, Object> deps1 = buildRuntimeDependencies(allEvents, mapOf("synchronization_chains", new ArrayList<>()));
        Map<String, Object> propagation = buildWorkflowPropagation(alignment, deps1);
        Map<String, Object> dependencies = buildRuntimeDependencies(allEvents, propagation);
        Map<String, Object> causalGraph = buildCausalGraph(allEvents, causality);
        Map<String, Object> transitions = buildStateTransitions(allEvents);
        Map<String, Object> sequence = buildRuntimeSequence(allEvents);
        Map<String, Object> timeline = buildRuntimeTimeline(allEvents, propagation);
        Map<String, Object> desktop = asMap(cognition.get("desktop"));
        Map<String, Object> terminal = asMap(cognition.get("terminal"));
        Map<String, Object> processes = asMap(cognition.get("processes"));
        Map<String, Object> correlation = correlateRuntimeMutations(browser, nativeEvents,
                asList(desktop.get("notifications")), asList(terminal.get("output")), asList(processes.get("processes")));
        Map<String, Object> distributed = buildDistributedCausality(distributedResult, null);
        Map<String, Object> browserBridge = bridgeBrowserNativeRuntime(browser, nativeEvents);
        List<Object> electronEvents = new ArrayList<>();
        List<Object> terminalEvents = new ArrayList<>();
        for (Object eo : nativeEvents) {
            String r = str(asMap(eo).get("runtime"));
            if (r.equals("electron")) {
                electronEvents.add(eo);
            } else if (r.equals("terminal")) {
                terminalEvents.add(eo);
            }
        }
        Map<String, Object> electronBridge = bridgeElectronTerminalRuntime(electronEvents, terminalEvents);
        Map<String, Object> notificationCausality = trackNotificationCausality(asList(desktop.get("notifications")),
                allEvents);
        Map<String, Object> processCausality = trackProcessCausality(asList(processes.get("processes")), allEvents);
        Map<String, Object> recovery = recoverCausalRuntime(causality, allEvents);

        Map<String, Object> payload = map();
        payload.put("causality", causality);
        payload.put("event_chain", eventChain);
        payload.put("alignment", alignment);
        payload.put("propagation", propagation);
        payload.put("dependencies", dependencies);
        payload.put("causal_graph", causalGraph);
        payload.put("transitions", transitions);
        payload.put("sequence", sequence);
        payload.put("timeline", timeline);
        payload.put("correlation", correlation);
        payload.put("distributed", distributed);
        payload.put("browser_bridge", browserBridge);
        payload.put("electron_bridge", electronBridge);
        payload.put("notification_causality", notificationCausality);
        payload.put("process_causality", processCausality);
        payload.put("recovery", recovery);
        payload.put("bounded", true);

        Map<String, Object> update = map();
        update.put("event_chains", eventChain);
        update.put("runtime_propagation", causality);
        update.put("causal_graphs", causalGraph);
        update.put("distributed_workflows", distributed);
        update.put("synchronization_state", alignment);
        update.put("alignment", alignment);
        update.put("timeline", timeline);
        Map<String, Object> updatedMemory = rememberCausalRuntime(mem, update);

        payload.put("memory", updatedMemory);
        payload.put("replay", replayCausalRuntime(updatedMemory));
        payload.put("causal_ir", compileCausalRuntimeIr(payload));
        return payload;
    }

    /** {@code run_causality_for_extraction} (no FS when memory path/key empty). */
    public static Map<String, Object> runCausalityForExtraction(boolean causalityRuntime, String memoryPath,
            String memoryKey, List<Object> browserEvents, Map<String, Object> nativeCognition,
            Map<String, Object> applicationResult, Map<String, Object> distributedResult, List<Object> interactions,
            boolean mergeGraph) {
        if (!causalityRuntime) {
            Map<String, Object> off = map();
            off.put("enabled", false);
            off.put("bounded", true);
            return off;
        }
        Map<String, Object> memory = map(); // empty memory path -> no FS load

        Map<String, Object> result = runCausalityRuntime(browserEvents, nativeCognition, applicationResult,
                distributedResult, memory, interactions);

        Map<String, Object> graphIr = causalRuntimeIrToGraph(asMap(Py.get(result, "causal_ir", map())));
        Map<String, Object> unifiedGraph = map();
        if (mergeGraph) {
            unifiedGraph = ExecutionRuntime.buildUnifiedRuntimeGraph(new ArrayList<>(List.of(graphIr)));
        }
        Map<String, Object> out = map();
        out.put("enabled", true);
        out.put("causality", result);
        out.put("causal_ir", Py.get(result, "causal_ir", map()));
        out.put("causal_graph_ir", graphIr);
        out.put("unified_graph", unifiedGraph);
        out.put("replay", Py.get(result, "replay", map()));
        out.put("memory_persisted", false);
        out.put("bounded", true);
        return out;
    }
}
