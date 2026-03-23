package com.webweavex;

import java.util.*;

public class Graph {
    
    public Map<String, Object> build(List<Map<String, String>> entities) {
        Map<String, Object> result = new LinkedHashMap<>();
        
        List<Map<String, Object>> nodes = new ArrayList<>();
        List<Map<String, Object>> edges = new ArrayList<>();
        
        if (entities == null || entities.isEmpty()) {
            result.put("nodes", nodes);
            result.put("edges", edges);
            return result;
        }
        
        List<Map<String, String>> uniqueEntities = new ArrayList<>();
        Set<String> seen = new HashSet<>();
        
        for (Map<String, String> e : entities) {
            String key = e.get("type") + ":" + e.get("value");
            if (!seen.contains(key)) {
                seen.add(key);
                uniqueEntities.add(e);
            }
        }
        
        Collections.sort(uniqueEntities, (a, b) -> {
            int typeComp = a.get("type").compareTo(b.get("type"));
            if (typeComp != 0) return typeComp;
            return a.get("value").compareTo(b.get("value"));
        });
        
        for (Map<String, String> e : uniqueEntities) {
            Map<String, Object> node = new LinkedHashMap<>();
            String id = e.get("type") + ":" + e.get("value");
            node.put("id", id);
            node.put("type", e.get("type"));
            node.put("value", e.get("value"));
            nodes.add(node);
        }
        
        for (int i = 0; i < uniqueEntities.size(); i++) {
            for (int j = i + 1; j < uniqueEntities.size(); j++) {
                Map<String, Object> edge = new LinkedHashMap<>();
                edge.put("source", uniqueEntities.get(i).get("type") + ":" + uniqueEntities.get(i).get("value"));
                edge.put("target", uniqueEntities.get(j).get("type") + ":" + uniqueEntities.get(j).get("value"));
                edge.put("weight", 1);
                edges.add(edge);
            }
        }
        
        nodes.sort((a, b) -> ((String) a.get("id")).compareTo((String) b.get("id")));
        edges.sort((a, b) -> {
            int sourceComp = ((String) a.get("source")).compareTo((String) b.get("source"));
            if (sourceComp != 0) return sourceComp;
            return ((String) a.get("target")).compareTo((String) b.get("target"));
        });
        
        result.put("nodes", nodes);
        result.put("edges", edges);
        return result;
    }
}
