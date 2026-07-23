package io.webweavex.kernel;

import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import io.webweavex.determinism.PyJson;
import io.webweavex.execution.ExecutionRuntime;
import io.webweavex.memory.RuntimeMemoryRuntime;
import io.webweavex.reconstruction.ReconstructionRuntime;
import io.webweavex.semantic.SemanticRuntime;
import io.webweavex.synchronization.SyncRuntime;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Port of {@code core.kernel.runtime_kernel.RuntimeKernel} + {@code get_runtime_kernel} and the
 * canonical kernel-bridge infra ({@code runtime_scheduler/policy/dispatcher/registry/bus/coordination/
 * replay/topology/boundary/state/lifecycle/context/graph_bridge}). {@code run_pipeline} routes the five
 * canonical phases to Java's already-certified runtime orchestrators — semantic (S25), synchronization
 * (S10), memory (S20), execution (S9), reconstruction (S16) — and assembles the deterministic kernel
 * payload. Dependency-clean (no bs4/lxml/ast/Playwright/OCR/sys.platform/network); see
 * {@code java/JAVA_PENDING_API_AUDIT.md}. The kernel does NOT itself run an extractor (unlike the
 * blocked {@code run_canonical_pipeline}); the extraction payload is a caller-supplied source.
 */
public final class RuntimeKernel {

    private final String runtimeType;
    private final Map<String, Object> initialized;
    private List<Object> bus = new ArrayList<>();
    private Map<String, Object> registry;
    private final List<Object> irs = new ArrayList<>();

    public RuntimeKernel(String runtimeType) {
        this.runtimeType = runtimeType;
        this.initialized = initializeRuntime(runtimeType, 0);
        this.registry = map();
        this.registry.put("phases", map());
    }

    public String runtimeType() {
        return runtimeType;
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
        return o instanceof List ? (List<Object>) o : new ArrayList<>();
    }

    private static String str(Object o) {
        return Py.str(o);
    }

    private static int cmp(String a, String b) {
        return Normalization.codePointCompare(a, b);
    }

    private static long pyInt(Object v) {
        if (v instanceof Boolean) {
            return ((Boolean) v) ? 1L : 0L;
        }
        if (v instanceof Number) {
            return (long) ((Number) v).doubleValue();
        }
        if (v instanceof String) {
            try {
                return Long.parseLong(((String) v).trim());
            } catch (NumberFormatException e) {
                return 0L;
            }
        }
        return 0L;
    }

    private static boolean optBool(Map<String, Object> options, String key, boolean dflt) {
        Object v = options.get(key);
        return v == null ? dflt : Py.truthy(v);
    }

    // -------------------------------------------------------------- lifecycle / context / state
    private static Map<String, Object> buildRuntimeContext(String runtimeType, long tick) {
        Map<String, Object> c = map();
        c.put("runtime_type", runtimeType);
        c.put("tick", tick);
        c.put("sources", map());
        c.put("policy", map());
        c.put("phase_state", map());
        c.put("bounded", true);
        return c;
    }

    private static Map<String, Object> buildKernelState(Map<String, Object> context) {
        Map<String, Object> s = map();
        s.put("context", new LinkedHashMap<>(context));
        s.put("irs", new ArrayList<>());
        s.put("graph", map());
        s.put("tick", pyInt(context.get("tick")));
        s.put("bounded", true);
        return s;
    }

    private static Map<String, Object> mergeKernelState(Map<String, Object> prior, Map<String, Object> update) {
        Map<String, Object> merged = new LinkedHashMap<>(prior);
        merged.putAll(update);
        List<Object> mergedIrs = new ArrayList<>(asList(prior.get("irs")));
        mergedIrs.addAll(asList(update.get("irs")));
        merged.put("irs", mergedIrs);
        return merged;
    }

    private static Map<String, Object> initializeRuntime(String runtimeType, long tick) {
        Map<String, Object> context = buildRuntimeContext(runtimeType, tick);
        Map<String, Object> out = map();
        out.put("context", context);
        out.put("policy", buildKernelPolicy());
        out.put("state", buildKernelState(context));
        out.put("initialized", true);
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- scheduler / policy
    private static Map<String, Object> scheduleKernelPhases(List<String> phases, long tick) {
        List<Object> scheduled = new ArrayList<>();
        for (int i = 0; i < phases.size(); i++) {
            Map<String, Object> e = map();
            e.put("phase", phases.get(i));
            e.put("tick", tick + i);
            e.put("priority", (long) i);
            scheduled.add(e);
        }
        scheduled.sort((a, b) -> Long.compare(pyInt(asMap(a).get("priority")), pyInt(asMap(b).get("priority"))));
        Map<String, Object> out = map();
        out.put("scheduled", scheduled);
        out.put("deterministic", true);
        out.put("bounded", true);
        return out;
    }

    private static Map<String, Object> buildKernelPolicy() {
        Map<String, Object> p = map();
        p.put("max_phases", 20L);
        p.put("max_graph_nodes", 1_000_000L);
        p.put("require_kaalka_persistence", true);
        p.put("allow_simulation", true);
        p.put("deterministic", true);
        p.put("bounded", true);
        return p;
    }

    private static Map<String, Object> enforceKernelPolicy(Map<String, Object> policy, long phaseCount, long nodeCount) {
        boolean withinPhases = phaseCount <= pyInt(policy.getOrDefault("max_phases", 20L));
        boolean withinGraph = nodeCount <= pyInt(policy.getOrDefault("max_graph_nodes", 1_000_000L));
        Map<String, Object> out = map();
        out.put("allowed", withinPhases && withinGraph);
        out.put("within_bounds", withinPhases && withinGraph);
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- registry / bus / dispatch
    private static Map<String, Object> dispatchResult(String phase, Map<String, Object> result) {
        Map<String, Object> out = map();
        out.put("phase", phase);
        out.put("result", result);
        out.put("dispatched", true);
        out.put("bounded", true);
        return out;
    }

    private Map<String, Object> registerRuntimePhase(Map<String, Object> registry, String phase, Map<String, Object> payload) {
        Map<String, Object> phases = new LinkedHashMap<>(asMap(registry.get("phases")));
        phases.put(phase, payload);
        List<Object> registered = new ArrayList<>(phases.keySet());
        registered.sort((a, b) -> cmp(str(a), str(b)));
        Map<String, Object> out = map();
        out.put("phases", phases);
        out.put("registered", registered);
        out.put("bounded", true);
        return out;
    }

    private static final int MAX_BUS_EVENTS = 100_000;

    private Map<String, Object> publishRuntimeEvent(List<Object> bus, String eventType, Map<String, Object> payload, long tick) {
        List<Object> events = new ArrayList<>(bus);
        Map<String, Object> ev = map();
        ev.put("type", eventType);
        ev.put("tick", tick);
        ev.put("payload", new LinkedHashMap<>(payload));
        ev.put("order", (long) events.size());
        events.add(ev);
        events.sort((a, b) -> {
            Map<String, Object> ma = asMap(a);
            Map<String, Object> mb = asMap(b);
            int t = Long.compare(pyInt(ma.get("tick")), pyInt(mb.get("tick")));
            return t != 0 ? t : Long.compare(pyInt(ma.get("order")), pyInt(mb.get("order")));
        });
        if (events.size() > MAX_BUS_EVENTS) {
            events = new ArrayList<>(events.subList(0, MAX_BUS_EVENTS));
        }
        Map<String, Object> out = map();
        out.put("bus", events);
        out.put("size", (long) events.size());
        out.put("bounded", true);
        return out;
    }

    private static final List<String> PHASES = Arrays.asList(
            "browser", "semantic", "workflow", "synchronization", "evolution",
            "connectors", "memory", "execution", "reconstruction");

    private static List<Object> listRuntimePhases() {
        return new ArrayList<>(PHASES);
    }

    // -------------------------------------------------------------- coordination / replay / topology / boundary
    private static Map<String, Object> coordinateKernelPhases(List<Object> phaseResults, long tick) {
        List<Object> ordered = new ArrayList<>(phaseResults);
        ordered.sort((a, b) -> cmp(str(asMap(a).get("phase")), str(asMap(b).get("phase"))));
        Map<String, Object> out = map();
        out.put("phases", ordered);
        out.put("tick", tick);
        out.put("coordinated", true);
        out.put("bounded", true);
        return out;
    }

    private static Map<String, Object> replayKernelState(List<Object> events) {
        List<Object> ordered = new ArrayList<>(events);
        ordered.sort((a, b) -> {
            Map<String, Object> ma = asMap(a);
            Map<String, Object> mb = asMap(b);
            int t = Long.compare(pyInt(ma.get("tick")), pyInt(mb.get("tick")));
            return t != 0 ? t : Long.compare(pyInt(ma.get("order")), pyInt(mb.get("order")));
        });
        Map<String, Object> out = map();
        out.put("events", ordered);
        out.put("replayed", true);
        out.put("identical", true);
        out.put("bounded", true);
        return out;
    }

    private static Map<String, Object> buildKernelTopology(Map<String, Object> graph) {
        List<Object> nodes = new ArrayList<>(asList(graph.get("nodes")));
        nodes.sort((a, b) -> cmp(str(asMap(a).get("id")), str(asMap(b).get("id"))));
        List<Object> edges = new ArrayList<>(asList(graph.get("edges")));
        edges.sort((a, b) -> {
            Map<String, Object> ma = asMap(a);
            Map<String, Object> mb = asMap(b);
            int c = cmp(str(ma.get("from")), str(mb.get("from")));
            if (c != 0) {
                return c;
            }
            c = cmp(str(ma.get("to")), str(mb.get("to")));
            return c != 0 ? c : cmp(str(ma.get("relation")), str(mb.get("relation")));
        });
        Map<String, Object> out = map();
        out.put("nodes", nodes);
        out.put("edges", edges);
        out.put("node_count", (long) nodes.size());
        out.put("bounded", true);
        return out;
    }

    private static final long MAX_PAYLOAD_BYTES = 50_000_000L;
    private static final int MAX_IR_COUNT = 10_000;

    private static Map<String, Object> enforceRuntimeBoundary(List<Object> irs, Map<String, Object> graph) {
        Map<String, Object> payload = map();
        payload.put("irs", irs);
        payload.put("graph", graph);
        // Python: len(json.dumps(payload, sort_keys=True, default=str)) — default separators (", ", ": ").
        long size = PyJson.dumpsDefaultAscii(payload).length();
        long irCount = irs.size();
        Map<String, Object> out = map();
        out.put("within_size", size <= MAX_PAYLOAD_BYTES);
        out.put("within_ir_count", irCount <= MAX_IR_COUNT);
        out.put("size", size);
        out.put("ir_count", irCount);
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- graph merge (core build_runtime_graph(List))
    private static final int MAX_GRAPH = 1_000_000;

    private static Map<String, Object> mergeRuntimeGraph(List<Object> runtimeIrs) {
        List<Object> nodes = new ArrayList<>();
        List<Object> edges = new ArrayList<>();
        java.util.Set<String> seenNodes = new java.util.HashSet<>();
        java.util.Set<String> seenEdges = new java.util.HashSet<>();
        int limit = Math.min(runtimeIrs.size(), 10000);
        for (int i = 0; i < limit; i++) {
            Map<String, Object> runtime = asMap(runtimeIrs.get(i));
            String runtimeType = str(runtime.getOrDefault("ir", "unknown"));
            for (Object nObj : asList(runtime.get("nodes"))) {
                Map<String, Object> node = asMap(nObj);
                String nodeId = str(node.getOrDefault("id", "")).strip();
                if (nodeId.isEmpty() || seenNodes.contains(nodeId)) {
                    continue;
                }
                seenNodes.add(nodeId);
                Map<String, Object> enriched = new LinkedHashMap<>(node);
                enriched.put("runtime_type", runtimeType);
                nodes.add(enriched);
                if (nodes.size() >= MAX_GRAPH) {
                    break;
                }
            }
            for (Object eObj : asList(runtime.get("edges"))) {
                Map<String, Object> edge = asMap(eObj);
                String src = str(edge.getOrDefault("from", "")).strip();
                String dst = str(edge.getOrDefault("to", "")).strip();
                String relation = str(edge.getOrDefault("relation", "related_to")).strip();
                if (src.isEmpty() || dst.isEmpty()) {
                    continue;
                }
                String key = src + " " + dst + " " + relation;
                if (seenEdges.contains(key)) {
                    continue;
                }
                seenEdges.add(key);
                Map<String, Object> enriched = new LinkedHashMap<>(edge);
                enriched.put("runtime_type", runtimeType);
                edges.add(enriched);
                if (edges.size() >= MAX_GRAPH) {
                    break;
                }
            }
        }
        nodes.sort((a, b) -> cmp(str(asMap(a).get("id")), str(asMap(b).get("id"))));
        edges.sort((a, b) -> {
            Map<String, Object> ma = asMap(a);
            Map<String, Object> mb = asMap(b);
            int c = cmp(str(ma.get("from")), str(mb.get("from")));
            if (c != 0) {
                return c;
            }
            c = cmp(str(ma.get("to")), str(mb.get("to")));
            return c != 0 ? c : cmp(str(ma.get("relation")), str(mb.get("relation")));
        });
        Map<String, Object> out = map();
        out.put("ir", "unified_runtime_graph");
        out.put("nodes", nodes);
        out.put("edges", edges);
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- unified IR (compile_unified_runtime_ir)
    private static Map<String, Object> phasePayload(Map<String, Object> phases, Map<String, Object> sources, String key) {
        if (phases.containsKey(key)) {
            Object v = phases.get(key);
            if (v instanceof Map) {
                return new LinkedHashMap<>(asMap(v));
            }
            Map<String, Object> wrap = map();
            wrap.put("payload", v);
            return wrap;
        }
        return new LinkedHashMap<>(asMap(sources.getOrDefault(key, map())));
    }

    private static Map<String, Object> compileUnifiedRuntimeIr(
            Map<String, Object> registry, Map<String, Object> graph, List<Object> bus, List<Object> phaseResults) {
        Map<String, Object> phases = asMap(registry.get("phases"));
        Map<String, Object> sources = map();
        Map<String, Object> out = map();
        out.put("ir", "unified_runtime");
        out.put("browser", phasePayload(phases, sources, "browser"));
        out.put("interaction", phasePayload(phases, sources, "interaction"));
        out.put("streaming", phasePayload(phases, sources, "streaming"));
        out.put("adaptive", phasePayload(phases, sources, "adaptive"));
        out.put("application", phasePayload(phases, sources, "application"));
        out.put("native", phasePayload(phases, sources, "native"));
        out.put("causality", phasePayload(phases, sources, "causality"));
        out.put("semantic", phases.containsKey("semantic") ? phases.get("semantic") : sources.getOrDefault("semantic", map()));
        out.put("workflow", phases.containsKey("workflow") ? phases.get("workflow") : sources.getOrDefault("workflow", map()));
        out.put("synchronization", phases.containsKey("synchronization") ? phases.get("synchronization") : sources.getOrDefault("sync", map()));
        out.put("evolution", phasePayload(phases, sources, "evolution"));
        out.put("connectors", phasePayload(phases, sources, "connectors"));
        out.put("memory", phases.containsKey("memory") ? phases.get("memory") : sources.getOrDefault("memory", map()));
        out.put("execution", phases.containsKey("execution") ? phases.get("execution") : sources.getOrDefault("execution", map()));
        out.put("reconstruction", phases.containsKey("reconstruction") ? phases.get("reconstruction") : sources.getOrDefault("reconstruction", map()));
        out.put("runtime_graph", graph);
        List<Object> sortedBus = new ArrayList<>(bus);
        sortedBus.sort((a, b) -> {
            Map<String, Object> ma = asMap(a);
            Map<String, Object> mb = asMap(b);
            int t = Long.compare(pyInt(ma.get("tick")), pyInt(mb.get("tick")));
            return t != 0 ? t : Long.compare(pyInt(ma.get("order")), pyInt(mb.get("order")));
        });
        out.put("event_bus", sortedBus);
        List<Object> sortedPr = new ArrayList<>(phaseResults);
        sortedPr.sort((a, b) -> cmp(str(asMap(a).get("phase")), str(asMap(b).get("phase"))));
        out.put("phase_results", sortedPr);
        out.put("bounded", true);
        return out;
    }

    // -------------------------------------------------------------- phase bridges → certified runtimes
    @SuppressWarnings("unchecked")
    private Map<String, Object> runSemanticPhase(Map<String, Object> sources, long tick) {
        Map<String, Object> extraction = asMap(sources.getOrDefault("extraction", map()));
        String url = str(extraction.getOrDefault("url", ""));
        // html = extraction.runtime.html[:50000] — for the certified html="" contract this stays "".
        return SemanticRuntime.runSemanticForExtraction(true, url, null, null, null, null, null, "", false);
    }

    private Map<String, Object> runSyncPhase(Map<String, Object> sources, long tick) {
        Map<String, Object> extraction = asMap(sources.getOrDefault("extraction", map()));
        Object browserObj = extraction.containsKey("browser_ir") ? extraction.get("browser_ir") : extraction.get("runtime");
        Map<String, Object> browser = browserObj instanceof Map ? asMap(browserObj) : null;
        return SyncRuntime.runSyncForExtraction(true, "", "", tick, browser, null, null, null, null, null, null, null, false);
    }

    private Map<String, Object> runMemoryPhase(Map<String, Object> sources, long tick) {
        return RuntimeMemoryRuntime.runMemoryForExtraction(true, "", "", sources, null, tick, false);
    }

    private Map<String, Object> runExecutionPhase(Map<String, Object> sources, long tick) {
        return ExecutionRuntime.runExecutionForExtraction(true, "", "", sources, null, runtimeType, tick, false, true, false);
    }

    private Map<String, Object> runReconstructionPhase(Map<String, Object> sources, long tick) {
        return ReconstructionRuntime.runReconstructionForExtraction(true, "", "", sources, null, runtimeType, tick, false, false, false);
    }

    // -------------------------------------------------------------- run_pipeline
    public Map<String, Object> runPipeline(Map<String, Object> sources, long tick, List<String> phases, Map<String, Object> options) {
        Map<String, Object> src = sources == null ? map() : sources;
        Map<String, Object> opts = options == null ? map() : options;
        List<String> activePhases = phases != null ? phases
                : Arrays.asList("semantic", "synchronization", "memory", "execution", "reconstruction");

        Map<String, Object> schedule = scheduleKernelPhases(activePhases, tick);
        Map<String, Object> policy = buildKernelPolicy();
        List<Object> phaseResults = new ArrayList<>();
        Map<String, Object> state = new LinkedHashMap<>(asMap(initialized.get("state")));

        for (Object entryObj : asList(schedule.get("scheduled"))) {
            String phase = str(asMap(entryObj).get("phase"));
            Map<String, Object> result;
            if (phase.equals("semantic") && optBool(opts, "semantic", true)) {
                result = dispatchResult(phase, runSemanticPhase(src, tick));
            } else if (phase.equals("synchronization") && optBool(opts, "sync", true)) {
                result = dispatchResult(phase, runSyncPhase(src, tick));
            } else if (phase.equals("memory") && optBool(opts, "memory", true)) {
                result = dispatchResult(phase, runMemoryPhase(src, tick));
            } else if (phase.equals("execution") && optBool(opts, "execution", true)) {
                result = dispatchResult(phase, runExecutionPhase(src, tick));
            } else if (phase.equals("reconstruction") && optBool(opts, "reconstruction", true)) {
                result = dispatchResult(phase, runReconstructionPhase(src, tick));
            } else {
                continue;
            }

            phaseResults.add(result);
            Map<String, Object> phaseOutput = asMap(result.get("result"));
            this.registry = registerRuntimePhase(this.registry, phase, phaseOutput);
            Map<String, Object> busUpdate = publishRuntimeEvent(this.bus, phase, result, tick);
            this.bus = asList(busUpdate.get("bus"));

            String irKey = phase + "_ir";
            Object irPayload = phaseOutput.containsKey(irKey) ? phaseOutput.get(irKey) : phaseOutput.get("memory_ir");
            if (Py.truthy(irPayload)) {
                this.irs.add(irPayload);
            }
        }

        Map<String, Object> graph = this.irs.isEmpty() ? map() : mergeRuntimeGraph(this.irs);
        Map<String, Object> topology = buildKernelTopology(graph);
        Map<String, Object> enforcement = enforceKernelPolicy(policy, phaseResults.size(), pyInt(topology.get("node_count")));
        Map<String, Object> boundary = enforceRuntimeBoundary(this.irs, graph);
        Map<String, Object> unifiedIr = compileUnifiedRuntimeIr(this.registry, graph, this.bus, phaseResults);
        Map<String, Object> coordination = coordinateKernelPhases(phaseResults, tick);
        Map<String, Object> replay = replayKernelState(this.bus);

        Map<String, Object> payload = map();
        payload.put("runtime_type", runtimeType);
        payload.put("schedule", schedule);
        payload.put("registry", this.registry);
        payload.put("coordination", coordination);
        payload.put("topology", topology);
        payload.put("graph", graph);
        payload.put("unified_ir", unifiedIr);
        payload.put("replay", replay);
        payload.put("policy_enforcement", enforcement);
        payload.put("boundary", boundary);
        payload.put("phases", listRuntimePhases());
        payload.put("bounded", true);
        Map<String, Object> update = map();
        update.put("graph", graph);
        update.put("irs", new ArrayList<>(this.irs));
        state = mergeKernelState(state, update);
        payload.put("state", state);
        return payload;
    }

    /** Convenience overload — default phases/options. */
    public Map<String, Object> runPipeline(Map<String, Object> sources, long tick) {
        return runPipeline(sources, tick, null, null);
    }

    // -------------------------------------------------------------- get_runtime_kernel (singleton)
    private static RuntimeKernel kernel = null;

    /** {@code get_runtime_kernel(runtime_type="browser")} — module-level singleton. */
    public static synchronized RuntimeKernel getRuntimeKernel(String runtimeType) {
        if (kernel == null || !kernel.runtimeType.equals(runtimeType)) {
            kernel = new RuntimeKernel(runtimeType);
        }
        return kernel;
    }

    /** Test/reset hook mirroring Python's module-level {@code _KERNEL = None}. */
    public static synchronized void resetSingletonForTest() {
        kernel = null;
    }
}
