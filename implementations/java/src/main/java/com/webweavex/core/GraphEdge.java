package com.webweavex.core;

import java.util.*;

public class GraphEdge {
    private final String source;
    private final String target;
    private final int weight;
    private final boolean directed;

    public GraphEdge(String source, String target, int weight, boolean directed) {
        this.source = source;
        this.target = target;
        this.weight = weight;
        this.directed = directed;
    }

    public String getSource() { return source; }
    public String getTarget() { return target; }
    public int getWeight() { return weight; }
    public boolean isDirected() { return directed; }

    public Map<String, Object> toMap() {
        Map<String, Object> map = new LinkedHashMap<>();
        map.put("source", source);
        map.put("target", target);
        map.put("weight", weight);
        if (directed) {
            map.put("directed", true);
        }
        return map;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        GraphEdge graphEdge = (GraphEdge) o;
        return Objects.equals(source, graphEdge.source) && Objects.equals(target, graphEdge.target);
    }

    @Override
    public int hashCode() {
        return Objects.hash(source, target);
    }
}
