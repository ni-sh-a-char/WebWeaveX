package com.webweavex.pipeline;

import com.webweavex.core.*;
import java.util.*;

public class GraphEngine {
    private final boolean directed;

    public GraphEngine() {
        this.directed = false;
    }

    public GraphEngine(boolean directed) {
        this.directed = directed;
    }

    public GraphResult build(List<Entity> entities) {
        if (entities == null || entities.isEmpty()) {
            return new GraphResult(new ArrayList<>(), new ArrayList<>());
        }

        List<Entity> uniqueEntities = deduplicateEntities(entities);
        List<Entity> sortedEntities = sortEntities(uniqueEntities);
        List<GraphEdge> edges = buildEdges(sortedEntities);

        return new GraphResult(sortedEntities, edges);
    }

    private List<Entity> deduplicateEntities(List<Entity> entities) {
        Set<String> seen = new HashSet<>();
        List<Entity> unique = new ArrayList<>();

        for (Entity entity : entities) {
            String key = entity.getType() + ":" + entity.getValue();
            if (!seen.contains(key)) {
                seen.add(key);
                unique.add(entity);
            }
        }

        return unique;
    }

    private List<Entity> sortEntities(List<Entity> entities) {
        List<Entity> sorted = new ArrayList<>(entities);
        sorted.sort((a, b) -> {
            int typeCompare = a.getType().compareTo(b.getType());
            if (typeCompare != 0) return typeCompare;
            return a.getValue().compareTo(b.getValue());
        });
        return sorted;
    }

    private List<GraphEdge> buildEdges(List<Entity> entities) {
        List<GraphEdge> edges = new ArrayList<>();

        for (int i = 0; i < entities.size(); i++) {
            for (int j = i + 1; j < entities.size(); j++) {
                Entity e1 = entities.get(i);
                Entity e2 = entities.get(j);
                GraphEdge edge = new GraphEdge(
                    e1.getType() + ":" + e1.getValue(),
                    e2.getType() + ":" + e2.getValue(),
                    1,
                    directed
                );
                edges.add(edge);
            }
        }

        edges.sort((a, b) -> {
            int sourceCompare = a.getSource().compareTo(b.getSource());
            if (sourceCompare != 0) return sourceCompare;
            return a.getTarget().compareTo(b.getTarget());
        });

        return edges;
    }
}
