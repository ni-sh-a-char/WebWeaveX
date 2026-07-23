package io.webweavex.ir;

import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Port of {@code core.ir.unified_runtime_ir} — {@code compile_unified_runtime_ir}
 * and {@code unified_runtime_ir_to_graph}. Output is byte-identical to Python
 * under {@code compute_deterministic_hash}.
 */
public final class UnifiedRuntimeIr {

    private UnifiedRuntimeIr() {
    }

    public static Map<String, Object> compile(
            Map<String, Object> registry,
            Map<String, Object> graph,
            List<Map<String, Object>> bus,
            List<Map<String, Object>> phaseResults,
            Map<String, Object> sources) {

        Map<String, Object> reg = registry == null ? Map.of() : registry;
        Map<String, Object> g = graph == null ? new LinkedHashMap<>() : graph;
        List<Map<String, Object>> busList = bus == null ? List.of() : bus;
        List<Map<String, Object>> prList = phaseResults == null ? List.of() : phaseResults;
        Map<String, Object> src = sources == null ? Map.of() : sources;

        Map<String, Object> phases = Py.asMap(Py.get(reg, "phases", null));
        if (phases == null) {
            phases = new LinkedHashMap<>();
        }
        Map<String, Object> ph = phases;

        List<Map<String, Object>> sortedBus = new ArrayList<>(busList);
        sortedBus.sort(Comparator
                .comparingDouble((Map<String, Object> m) -> num(Py.get(m, "tick", 0L)))
                .thenComparingDouble(m -> num(Py.get(m, "order", 0L))));

        List<Map<String, Object>> sortedPr = new ArrayList<>(prList);
        sortedPr.sort(Comparator.comparing(
                m -> Py.str(Py.get(m, "phase", "")), Normalization::codePointCompare));

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("ir", "unified_runtime");
        out.put("browser", phasePayload(ph, src, "browser"));
        out.put("interaction", phasePayload(ph, src, "interaction"));
        out.put("streaming", phasePayload(ph, src, "streaming"));
        out.put("adaptive", phasePayload(ph, src, "adaptive"));
        out.put("application", phasePayload(ph, src, "application"));
        out.put("native", phasePayload(ph, src, "native"));
        out.put("causality", phasePayload(ph, src, "causality"));
        out.put("semantic", Py.get(ph, "semantic", Py.get(src, "semantic", Map.of())));
        out.put("workflow", Py.get(ph, "workflow", Py.get(src, "workflow", Map.of())));
        out.put("synchronization", Py.get(ph, "synchronization", Py.get(src, "sync", Map.of())));
        out.put("evolution", phasePayload(ph, src, "evolution"));
        out.put("connectors", phasePayload(ph, src, "connectors"));
        out.put("memory", Py.get(ph, "memory", Py.get(src, "memory", Map.of())));
        out.put("execution", Py.get(ph, "execution", Py.get(src, "execution", Map.of())));
        out.put("reconstruction",
                Py.get(ph, "reconstruction", Py.get(src, "reconstruction", Map.of())));
        out.put("runtime_graph", g);
        out.put("event_bus", new ArrayList<Object>(sortedBus));
        out.put("phase_results", new ArrayList<Object>(sortedPr));
        out.put("bounded", true);
        return out;
    }

    /** Port of {@code unified_runtime_ir_to_graph}. */
    public static Map<String, Object> toGraph(Map<String, Object> unifiedIr) {
        List<Object> nodes = new ArrayList<>();
        nodes.add(node("unified:root", "unified_runtime"));
        List<Object> edges = new ArrayList<>();

        Map<String, Object> graph = Py.asMap(Py.get(unifiedIr, "runtime_graph", null));
        List<Object> graphNodes = graph == null ? null : Py.asList(Py.get(graph, "nodes", null));
        if (graphNodes != null) {
            int limit = Math.min(graphNodes.size(), 100000);
            for (int i = 0; i < limit; i++) {
                Object n = graphNodes.get(i);
                String nodeId = Py.str(Py.get(n, "id", ""));
                if (!nodeId.isEmpty()) {
                    Map<String, Object> copy = new LinkedHashMap<>();
                    Map<String, Object> nm = Py.asMap(n);
                    if (nm != null) {
                        copy.putAll(nm);
                    }
                    nodes.add(copy);
                    Map<String, Object> edge = new LinkedHashMap<>();
                    edge.put("from", "unified:root");
                    edge.put("to", nodeId);
                    edge.put("relation", "contains");
                    edges.add(edge);
                }
            }
        }

        for (String phase : new String[] {
                "semantic", "memory", "execution", "reconstruction", "synchronization"}) {
            if (Py.truthy(Py.get(unifiedIr, phase, null))) {
                String pid = "phase:" + phase;
                nodes.add(node(pid, phase));
                Map<String, Object> edge = new LinkedHashMap<>();
                edge.put("from", pid);
                edge.put("to", "unified:root");
                edge.put("relation", "grounds");
                edges.add(edge);
            }
        }

        nodes.sort(Comparator.comparing(
                n -> Py.str(Py.get(n, "id", "")), Normalization::codePointCompare));

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("ir", "unified_runtime_graph");
        out.put("nodes", nodes);
        out.put("edges", edges);
        out.put("bounded", true);
        return out;
    }

    private static Map<String, Object> phasePayload(
            Map<String, Object> phases, Map<String, Object> sources, String key) {
        if (phases.containsKey(key)) {
            Object value = phases.get(key);
            Map<String, Object> m = Py.asMap(value);
            if (m != null) {
                return new LinkedHashMap<>(m);
            }
            Map<String, Object> wrap = new LinkedHashMap<>();
            wrap.put("payload", value);
            return wrap;
        }
        Map<String, Object> src = Py.asMap(Py.get(sources, key, null));
        return src == null ? new LinkedHashMap<>() : new LinkedHashMap<>(src);
    }

    private static Map<String, Object> node(String id, String type) {
        Map<String, Object> n = new LinkedHashMap<>();
        n.put("id", id);
        n.put("type", type);
        return n;
    }

    private static double num(Object o) {
        return o instanceof Number ? ((Number) o).doubleValue() : 0.0;
    }
}
