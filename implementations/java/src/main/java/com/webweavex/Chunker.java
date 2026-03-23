package com.webweavex;

import java.util.*;

public class Chunker {
    private int size = 500;
    private int overlap = 50;
    
    public Chunker() {}
    
    public List<Map<String, Object>> chunk(String text) {
        List<Map<String, Object>> chunks = new ArrayList<>();
        if (text == null || text.isEmpty()) return chunks;
        
        int start = 0;
        int index = 0;
        
        while (start < text.length()) {
            int end = start + size;
            
            if (end < text.length()) {
                end = findWordBoundary(text, end);
            }
            
            String chunkText = text.substring(start, Math.min(end, text.length()));
            if (!chunkText.trim().isEmpty()) {
                Map<String, Object> chunk = new LinkedHashMap<>();
                chunk.put("text", chunkText);
                chunk.put("index", index);
                chunk.put("start", start);
                chunk.put("end", end);
                chunks.add(chunk);
                index++;
            }
            
            start = end - overlap;
            if (start < 0) start = 0;
        }
        
        return chunks;
    }
    
    private int findWordBoundary(String text, int position) {
        if (position >= text.length()) return position;
        
        for (int i = position; i > Math.max(0, position - 50); i--) {
            char c = text.charAt(i);
            if (c == ' ' || c == '\t' || c == '\n' || c == '\r') {
                return i;
            }
        }
        
        return position;
    }
}
