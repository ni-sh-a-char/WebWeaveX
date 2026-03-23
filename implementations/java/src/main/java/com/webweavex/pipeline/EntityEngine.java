package com.webweavex.pipeline;

import com.webweavex.core.*;
import java.util.*;
import java.util.regex.*;

public class EntityEngine {
    private final Map<String, Pattern> patterns;
    private static final Pattern EMAIL_PATTERN = Pattern.compile("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}");
    private static final Pattern URL_PATTERN = Pattern.compile("https?://[^\\s<>\\\"]+");
    private static final Pattern NUMBER_PATTERN = Pattern.compile("\\b\\d+(?:\\.\\d+)?\\b");
    private static final Pattern CAPITALIZED_PATTERN = Pattern.compile("\\b[A-Z][a-z]+(?:\\s+[A-Z][a-z]+)*\\b");
    private static final Pattern PHONE_PATTERN = Pattern.compile("\\+?[0-9]{1,4}?[-.\\s]?\\(?[0-9]{1,4}\\)?[-.\\s]?[0-9]{1,4}[-.\\s]?[0-9]{1,9}");

    public EntityEngine() {
        patterns = new HashMap<>();
        patterns.put("email", EMAIL_PATTERN);
        patterns.put("url", URL_PATTERN);
        patterns.put("number", NUMBER_PATTERN);
        patterns.put("capitalized", CAPITALIZED_PATTERN);
        patterns.put("phone", PHONE_PATTERN);
    }

    public List<Entity> extract(String text) {
        if (text == null || text.isEmpty()) {
            return new ArrayList<>();
        }

        Set<String> seen = new LinkedHashSet<>();
        List<Entity> entities = new ArrayList<>();

        for (Map.Entry<String, Pattern> entry : patterns.entrySet()) {
            Matcher matcher = entry.getValue().matcher(text);
            while (matcher.find()) {
                String value = matcher.group().trim();
                String key = entry.getKey() + ":" + value;
                if (!seen.contains(key) && !value.isEmpty()) {
                    seen.add(key);
                    entities.add(new Entity(entry.getKey(), value));
                }
            }
        }

        entities.sort((a, b) -> {
            int typeCompare = a.getType().compareTo(b.getType());
            if (typeCompare != 0) return typeCompare;
            return a.getValue().compareTo(b.getValue());
        });

        return entities;
    }
}
