package com.webweavex;

import java.util.*;
import java.util.regex.*;

public class Entities {
    private Pattern emailPattern = Pattern.compile("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}");
    private Pattern urlPattern = Pattern.compile("https?://[^\\s<>\"']+");
    private Pattern numberPattern = Pattern.compile("\\b\\d+(?:\\.\\d+)?\\b");
    private Pattern phonePattern = Pattern.compile("\\+?[0-9]{1,4}?[-.\\s]?\\(?[0-9]{1,4}\\)?[-.\\s]?[0-9]{1,4}[-.\\s]?[0-9]{1,9}");
    private Pattern capitalizedPattern = Pattern.compile("\\b[A-Z][a-z]+(?:\\s+[A-Z][a-z]+)*\\b");
    
    public List<Map<String, String>> extract(String text) {
        List<Map<String, String>> entities = new ArrayList<>();
        if (text == null || text.isEmpty()) return entities;
        
        Set<String> seen = new HashSet<>();
        
        extractPattern(text, emailPattern, "email", entities, seen);
        extractPattern(text, urlPattern, "url", entities, seen);
        extractPattern(text, numberPattern, "number", entities, seen);
        extractPattern(text, phonePattern, "phone", entities, seen);
        extractPattern(text, capitalizedPattern, "capitalized", entities, seen);
        
        return entities;
    }
    
    private void extractPattern(String text, Pattern pattern, String type, 
                                 List<Map<String, String>> entities, Set<String> seen) {
        Matcher matcher = pattern.matcher(text);
        while (matcher.find()) {
            String value = matcher.group();
            String key = type + ":" + value;
            if (!seen.contains(key)) {
                seen.add(key);
                Map<String, String> entity = new LinkedHashMap<>();
                entity.put("type", type);
                entity.put("value", value);
                entities.add(entity);
            }
        }
    }
}
