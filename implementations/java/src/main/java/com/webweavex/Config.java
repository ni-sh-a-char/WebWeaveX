package com.webweavex;

import java.util.*;

public class Config {
    public static final Map<String, Object> DEFAULT_CONFIG = new HashMap<>();
    
    static {
        Map<String, Object> chunking = new LinkedHashMap<>();
        chunking.put("size", 500);
        chunking.put("overlap", 50);
        
        Map<String, Object> insights = new LinkedHashMap<>();
        insights.put("enabled", true);
        insights.put("top_entities_count", 10);
        insights.put("include_stats", true);
        
        DEFAULT_CONFIG.put("chunking", chunking);
        DEFAULT_CONFIG.put("insights", insights);
    }
    
    public static Map<String, Object> getConfig(Map<String, Object> overrides) {
        Map<String, Object> result = new HashMap<>(DEFAULT_CONFIG);
        if (overrides != null) {
            for (Map.Entry<String, Object> entry : overrides.entrySet()) {
                result.put(entry.getKey(), entry.getValue());
            }
        }
        return result;
    }
}
