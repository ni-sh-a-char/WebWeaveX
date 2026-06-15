package io.webweavex.query;

import io.webweavex.determinism.Py;
import io.webweavex.ir.SemanticGraphIr;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Ports of {@code core.query.graph_query_engine.query_graph},
 * {@code core.agents.graph_query_engine.query_nodes/query_edges}, and
 * {@code core.runtime_graph.runtime_graph_query_engine.query_runtime_graph}.
 */
public final class GraphQuery {

    private GraphQuery() {
    }

    private static final int MAX_RESULTS = 1000;

    public static Map<String, Object> queryGraph(Map<String, Object> graph, String node) {
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("ir", SemanticGraphIr.compile(graph));
        out.put("nodes", queryNodes(graph, node));
        out.put("edges", queryEdges(graph, node));
        out.put("explainable", true);
        out.put("bounded", true);
        return out;
    }

    public static List<Object> queryNodes(Map<String, Object> graph, String node) {
        List<Object> nodes = listOf(Py.get(graph, "nodes", new ArrayList<>()));
        if (node == null || node.isEmpty()) {
            return nodes;
        }
        List<Object> out = new ArrayList<>();
        for (Object n : nodes) {
            if (Py.str(Py.get(n, "id", "")).contains(node)) {
                out.add(n);
            }
        }
        return out;
    }

    public static List<Object> queryEdges(Map<String, Object> graph, String node) {
        List<Object> edges = listOf(Py.get(graph, "edges", new ArrayList<>()));
        if (node == null || node.isEmpty()) {
            return edges;
        }
        List<Object> out = new ArrayList<>();
        for (Object e : edges) {
            String from = Py.str(Py.get(e, "from", ""));
            String to = Py.str(Py.get(e, "to", ""));
            if (from.contains(node) || to.contains(node)) {
                out.add(e);
            }
        }
        return out;
    }

    /** Port of {@code query_runtime_graph(graph, query)} — filter by node type. */
    public static Map<String, Object> queryRuntimeGraph(
            Map<String, Object> graph, Map<String, Object> query) {
        List<Object> nodes = listOf(Py.get(graph, "nodes", new ArrayList<>()));
        String nodeType = Py.str(Py.get(query, "type", "")).strip();

        List<Object> results = new ArrayList<>();
        for (Object node : nodes) {
            if (!nodeType.isEmpty() && !Py.str(Py.get(node, "type", "")).equals(nodeType)) {
                continue;
            }
            results.add(node);
            if (results.size() >= MAX_RESULTS) {
                break;
            }
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("results", results);
        out.put("count", (long) results.size());
        out.put("bounded", true);
        return out;
    }

    private static List<Object> listOf(Object o) {
        List<Object> l = Py.asList(o);
        return l == null ? new ArrayList<>() : l;
    }
}
