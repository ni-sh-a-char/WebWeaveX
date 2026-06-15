package io.webweavex.graph;

import io.webweavex.determinism.Normalization;
import io.webweavex.determinism.Py;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/** Port of {@code core.graph.graph_reconstruction_engine.reconstruct_graph}. */
public final class GraphReconstruction {

    private GraphReconstruction() {
    }

    public static final int MAX_NODES = 5000;
    public static final int MAX_EDGES = 20000;

    public static Map<String, Object> reconstructGraph(Map<String, Object> systemGraph) {
        return reconstructGraph(systemGraph, MAX_EDGES, MAX_NODES);
    }

    public static Map<String, Object> reconstructGraph(
            Map<String, Object> systemGraph, int maxEdges, int maxNodes) {
        if (systemGraph == null) {
            Map<String, Object> empty = new LinkedHashMap<>();
            empty.put("nodes", new ArrayList<>());
            empty.put("edges", new ArrayList<>());
            empty.put("max_edges", (long) maxEdges);
            return empty;
        }

        List<Object> rawNodes = GraphUtil.list(systemGraph, "nodes");
        List<Object> components = GraphUtil.list(systemGraph, "components");
        List<Object> rawEdges = GraphUtil.list(systemGraph, "edges");
        List<Object> relationships = GraphUtil.list(systemGraph, "relationships");

        Set<String> nodeSet = new HashSet<>();
        for (Object n : rawNodes) {
            nodeSet.add(n instanceof Map ? nodeId(((Map<?, ?>) n).get("id")) : nodeId(n));
        }
        for (Object c : components) {
            if (c instanceof Map) {
                nodeSet.add(nodeId(((Map<?, ?>) c).get("name")));
            }
        }

        Set<List<String>> edgeSet = new LinkedHashSet<>();
        List<Object> merged = new ArrayList<>(rawEdges);
        merged.addAll(relationships);
        for (Object eo : merged) {
            if (!(eo instanceof Map)) {
                continue;
            }
            Map<?, ?> e = (Map<?, ?>) eo;
            if (e.containsKey("type")) {
                continue;
            }
            String f = nodeId(e.get("from"));
            String t = nodeId(e.get("to"));
            if (f.isEmpty() || t.isEmpty()) {
                continue;
            }
            nodeSet.add(f);
            nodeSet.add(t);
            edgeSet.add(List.of(f, t));
        }

        List<String> sortedNodeIds = new ArrayList<>();
        for (String n : nodeSet) {
            if (!n.isEmpty()) {
                sortedNodeIds.add(n);
            }
        }
        sortedNodeIds.sort(Normalization::codePointCompare);
        if (sortedNodeIds.size() > maxNodes) {
            sortedNodeIds = sortedNodeIds.subList(0, maxNodes);
        }

        List<Object> nodes = new ArrayList<>();
        Set<String> allowed = new HashSet<>();
        for (String nid : sortedNodeIds) {
            Map<String, Object> node = new LinkedHashMap<>();
            node.put("id", nid);
            node.put("kind", "structural");
            node.put("metadata", new LinkedHashMap<>());
            nodes.add(node);
            allowed.add(nid);
        }

        List<List<String>> sortedEdges = new ArrayList<>(edgeSet);
        sortedEdges.sort(Comparator
                .comparing((List<String> p) -> p.get(0), Normalization::codePointCompare)
                .thenComparing(p -> p.get(1), Normalization::codePointCompare));
        List<Object> edges = new ArrayList<>();
        for (List<String> p : sortedEdges) {
            if (edges.size() >= maxEdges) {
                break;
            }
            if (allowed.contains(p.get(0)) && allowed.contains(p.get(1))) {
                Map<String, Object> edge = new LinkedHashMap<>();
                edge.put("from", p.get(0));
                edge.put("to", p.get(1));
                edges.add(edge);
            }
        }

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("nodes", nodes);
        out.put("edges", edges);
        out.put("max_edges", (long) maxEdges);
        return out;
    }

    /** Python {@code _node_id(value) = str(value or "").strip()}. */
    private static String nodeId(Object value) {
        return Py.str(Py.truthy(value) ? value : "").strip();
    }
}
