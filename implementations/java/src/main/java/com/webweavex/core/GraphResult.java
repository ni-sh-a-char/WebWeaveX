package com.webweavex.core;

import java.util.*;

public class GraphResult {
    private final List<Entity> nodes;
    private final List<GraphEdge> edges;

    public GraphResult(List<Entity> nodes, List<GraphEdge> edges) {
        this.nodes = nodes;
        this.edges = edges;
    }

    public List<Entity> getNodes() { return nodes; }
    public List<GraphEdge> getEdges() { return edges; }

    public Map<String, Object> toMap() {
        Map<String, Object> map = new LinkedHashMap<>();
        List<Map<String, String>> nodeMaps = new ArrayList<>();
        for (Entity node : nodes) {
            nodeMaps.add(node.toMap());
        }
        List<Map<String, Object>> edgeMaps = new ArrayList<>();
        for (GraphEdge edge : edges) {
            edgeMaps.add(edge.toMap());
        }
        map.put("nodes", nodeMaps);
        map.put("edges", edgeMaps);
        return map;
    }
}
