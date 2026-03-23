package com.webweavex;

import java.util.*;

public class Insights {
    
    public Map<String, Object> compute(List<Map<String, String>> entities, 
                                        List<Map<String, Object>> chunks, String text) {
        Map<String, Object> result = new LinkedHashMap<>();
        
        Map<String, Integer> entityCounts = new LinkedHashMap<>();
        Set<String> entityTypes = new HashSet<>();
        
        for (Map<String, String> e : entities) {
            String key = e.get("type") + ":" + e.get("value");
            entityCounts.put(key, entityCounts.getOrDefault(key, 0) + 1);
            entityTypes.add(e.get("type"));
        }
        
        List<Map.Entry<String, Integer>> sortedCounts = new ArrayList<>(entityCounts.entrySet());
        sortedCounts.sort((a, b) -> {
            if (!b.getValue().equals(a.getValue())) {
                return b.getValue() - a.getValue();
            }
            return a.getKey().compareTo(b.getKey());
        });
        
        List<Map<String, Object>> topEntities = new ArrayList<>();
        for (int i = 0; i < Math.min(10, sortedCounts.size()); i++) {
            Map.Entry<String, Integer> entry = sortedCounts.get(i);
            String[] parts = entry.getKey().split(":", 2);
            Map<String, Object> te = new LinkedHashMap<>();
            te.put("type", parts[0]);
            te.put("value", parts.length > 1 ? parts[1] : "");
            te.put("count", entry.getValue());
            topEntities.add(te);
        }
        
        Map<String, Object> stats = new LinkedHashMap<>();
        stats.put("total_entities", entities.size());
        stats.put("unique_entities", entityCounts.size());
        stats.put("entity_types", entityTypes.size());
        stats.put("total_relations", 0);
        if (chunks != null && !chunks.isEmpty()) {
            stats.put("total_chunks", chunks.size());
        }
        if (text != null && !text.isEmpty()) {
            stats.put("text_length", text.length());
            stats.put("word_count", text.trim().split("\\s+").length);
        }
        
        List<String> sortedKeys = new ArrayList<>(entityCounts.keySet());
        Collections.sort(sortedKeys);
        Map<String, Integer> sortedEntityCounts = new LinkedHashMap<>();
        for (String key : sortedKeys) {
            sortedEntityCounts.put(key, entityCounts.get(key));
        }
        
        result.put("top_entities", topEntities);
        result.put("stats", stats);
        result.put("entity_counts", sortedEntityCounts);
        
        return result;
    }
}
