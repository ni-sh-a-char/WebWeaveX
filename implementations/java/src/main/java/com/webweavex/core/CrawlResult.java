package com.webweavex.core;

import java.util.*;

public class CrawlResult {
    private final String url;
    private final String text;
    private final List<Chunk> chunks;
    private final List<Entity> entities;
    private final GraphResult graph;
    private final Map<String, String> metadata;

    public CrawlResult(String url, String text, List<Chunk> chunks, List<Entity> entities, 
                       GraphResult graph, Map<String, String> metadata) {
        this.url = url;
        this.text = text;
        this.chunks = chunks;
        this.entities = entities;
        this.graph = graph;
        this.metadata = metadata;
    }

    public String getUrl() { return url; }
    public String getText() { return text; }
    public List<Chunk> getChunks() { return chunks; }
    public List<Entity> getEntities() { return entities; }
    public GraphResult getGraph() { return graph; }
    public Map<String, String> getMetadata() { return metadata; }

    public Map<String, Object> toMap() {
        Map<String, Object> map = new LinkedHashMap<>();
        map.put("url", url);
        map.put("text", text);
        if (chunks != null && !chunks.isEmpty()) {
            List<Map<String, Object>> chunkMaps = new ArrayList<>();
            for (Chunk chunk : chunks) chunkMaps.add(chunk.toMap());
            map.put("chunks", chunkMaps);
        }
        if (entities != null && !entities.isEmpty()) {
            List<Map<String, String>> entityMaps = new ArrayList<>();
            for (Entity entity : entities) entityMaps.add(entity.toMap());
            map.put("entities", entityMaps);
        }
        if (graph != null) {
            map.put("graph", graph.toMap());
        }
        if (metadata != null) {
            map.put("metadata", metadata);
        }
        return map;
    }
}
