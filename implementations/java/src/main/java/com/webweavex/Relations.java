package com.webweavex;

import java.util.*;

public class Relations {
    
    public List<Map<String, String>> extract(List<Map<String, String>> entities) {
        List<Map<String, String>> relations = new ArrayList<>();
        if (entities == null || entities.isEmpty()) return relations;
        
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
        
        for (int i = 0; i < uniqueEntities.size(); i++) {
            for (int j = i + 1; j < uniqueEntities.size(); j++) {
                Map<String, String> rel = new LinkedHashMap<>();
                rel.put("source", uniqueEntities.get(i).get("type") + ":" + uniqueEntities.get(i).get("value"));
                rel.put("target", uniqueEntities.get(j).get("type") + ":" + uniqueEntities.get(j).get("value"));
                rel.put("type", "cooccurrence");
                relations.add(rel);
            }
        }
        
        Collections.sort(relations, (a, b) -> {
            int sourceComp = a.get("source").compareTo(b.get("source"));
            if (sourceComp != 0) return sourceComp;
            return a.get("target").compareTo(b.get("target"));
        });
        
        return relations;
    }
}
