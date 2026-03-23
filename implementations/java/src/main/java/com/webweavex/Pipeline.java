package com.webweavex;

import java.util.*;

public class Pipeline {
    private Cleaner cleaner;
    private Chunker chunker;
    private Entities entities;
    private Relations relations;
    private Graph graph;
    private Insights insights;
    
    public Pipeline() {
        this.cleaner = new Cleaner();
        this.chunker = new Chunker();
        this.entities = new Entities();
        this.relations = new Relations();
        this.graph = new Graph();
        this.insights = new Insights();
    }
    
    public Map<String, Object> extractFromText(String text) {
        String cleanedText = cleaner.clean(text);
        List<Map<String, Object>> chunks = chunker.chunk(cleanedText);
        List<Map<String, String>> entityList = entities.extract(cleanedText);
        List<Map<String, String>> relList = relations.extract(entityList);
        Map<String, Object> graphResult = graph.build(entityList);
        Map<String, Object> insightsResult = insights.compute(entityList, chunks, cleanedText);
        
        return buildResult("", "", cleanedText, chunks, entityList, relList, graphResult, insightsResult);
    }
    
    private Map<String, Object> buildResult(String url, String title, String text,
                                            List<Map<String, Object>> chunks,
                                            List<Map<String, String>> entityList,
                                            List<Map<String, String>> relationsList,
                                            Map<String, Object> graphResult,
                                            Map<String, Object> insightsResult) {
        Map<String, Object> result = new LinkedHashMap<>();
        
        Map<String, String> meta = new LinkedHashMap<>();
        meta.put("title", title);
        meta.put("url", url);
        result.put("meta", meta);
        
        Map<String, String> content = new LinkedHashMap<>();
        content.put("text", text);
        result.put("content", content);
        
        List<Map<String, Object>> sortedChunks = new ArrayList<>(chunks);
        sortedChunks.sort((a, b) -> ((Integer) a.get("index")).compareTo((Integer) b.get("index")));
        result.put("chunks", sortedChunks);
        
        List<Map<String, String>> sortedEntities = new ArrayList<>(entityList);
        sortedEntities.sort((a, b) -> {
            int typeComp = a.get("type").compareTo(b.get("type"));
            if (typeComp != 0) return typeComp;
            return a.get("value").compareTo(b.get("value"));
        });
        result.put("entities", sortedEntities);
        
        List<Map<String, String>> sortedRelations = new ArrayList<>(relationsList);
        sortedRelations.sort((a, b) -> {
            int sourceComp = a.get("source").compareTo(b.get("source"));
            if (sourceComp != 0) return sourceComp;
            return a.get("target").compareTo(b.get("target"));
        });
        result.put("relations", sortedRelations);
        
        result.put("graph", graphResult);
        result.put("insights", insightsResult);
        
        return result;
    }
}
