package com.webweavex;

import java.util.*;
import java.time.Instant;

public class WebWeaveX {
    private Pipeline pipeline;
    
    public WebWeaveX() {
        this.pipeline = new Pipeline();
    }
    
    public Map<String, Object> extract(String textOrHtml) {
        try {
            if (textOrHtml == null || textOrHtml.isEmpty()) {
                return pipeline.extractFromText("");
            }
            
            if (textOrHtml.trim().startsWith("<") && textOrHtml.toLowerCase().contains("</html>")) {
                return pipeline.extractFromText(textOrHtml);
            }
            
            return pipeline.extractFromText(textOrHtml);
        } catch (Exception e) {
            Map<String, Object> errorResult = new LinkedHashMap<>();
            Map<String, String> meta = new LinkedHashMap<>();
            meta.put("title", "");
            meta.put("url", "");
            Map<String, String> content = new LinkedHashMap<>();
            content.put("text", "");
            
            errorResult.put("meta", meta);
            errorResult.put("content", content);
            errorResult.put("chunks", new ArrayList<>());
            errorResult.put("entities", new ArrayList<>());
            errorResult.put("relations", new ArrayList<>());
            
            Map<String, Object> graph = new LinkedHashMap<>();
            graph.put("nodes", new ArrayList<>());
            graph.put("edges", new ArrayList<>());
            errorResult.put("graph", graph);
            
            Map<String, Object> insights = new LinkedHashMap<>();
            insights.put("entity_counts", new LinkedHashMap<>());
            insights.put("stats", new LinkedHashMap<>());
            insights.put("top_entities", new ArrayList<>());
            errorResult.put("insights", insights);
            
            return errorResult;
        }
    }
    
    public Map<String, Object> extractAgent(String text) {
        try {
            Map<String, Object> result = extract(text);
            return extractAgentFromResult(result);
        } catch (Exception e) {
            Map<String, Object> agentResult = new LinkedHashMap<>();
            agentResult.put("task", "web_analysis");
            agentResult.put("input", text != null ? text.substring(0, Math.min(500, text.length())) : "");
            agentResult.put("output", new LinkedHashMap<>());
            agentResult.put("summary", "Error: " + e.getMessage());
            agentResult.put("actions", new ArrayList<>());
            agentResult.put("confidence", 0.0);
            return agentResult;
        }
    }
    
    @SuppressWarnings("unchecked")
    private Map<String, Object> extractAgentFromResult(Map<String, Object> result) {
        Map<String, Object> agentResult = new LinkedHashMap<>();
        agentResult.put("task", "web_analysis");
        
        Map<String, Object> content = (Map<String, Object>) result.get("content");
        String text = content != null ? (String) content.getOrDefault("text", "") : "";
        agentResult.put("input", text.length() > 500 ? text.substring(0, 500) : text);
        
        List<Map<String, String>> entities = (List<Map<String, String>>) result.get("entities");
        List<Map<String, String>> relations = (List<Map<String, String>>) result.get("relations");
        
        if (entities == null) entities = new ArrayList<>();
        if (relations == null) relations = new ArrayList<>();
        
        agentResult.put("output", result);
        
        if (entities.isEmpty()) {
            agentResult.put("summary", "No entities extracted from input text.");
        } else {
            agentResult.put("summary", String.format("Extracted %d entities from text.", entities.size()));
        }
        
        List<String> actions = new ArrayList<>();
        Set<String> types = new HashSet<>();
        for (Map<String, String> e : entities) {
            types.add(e.get("type"));
        }
        if (types.contains("url")) actions.add("crawl");
        if (types.contains("email")) actions.add("contact");
        if (types.contains("phone")) actions.add("call");
        if (entities.size() > 5) actions.add("extract_more");
        if (actions.isEmpty()) actions.add("analyze");
        agentResult.put("actions", actions);
        
        double confidence = text.length() > 0 
            ? Math.min((entities.size() + relations.size() * 0.5) / Math.max(text.length(), 1) * 10, 1.0) 
            : 0.0;
        agentResult.put("confidence", Math.round(confidence * 100.0) / 100.0);
        
        return agentResult;
    }
    
    @SuppressWarnings("unchecked")
    public Map<String, Object> toMemoryBlock(Map<String, Object> result) {
        Map<String, Object> memory = new LinkedHashMap<>();
        memory.put("type", "webweavex_memory");
        memory.put("entities", result.getOrDefault("entities", new ArrayList<>()));
        memory.put("relations", result.getOrDefault("relations", new ArrayList<>()));
        memory.put("graph", result.getOrDefault("graph", createEmptyGraph()));
        memory.put("timestamp", Instant.now().toString());
        memory.put("source", "webweavex");
        return memory;
    }
    
    @SuppressWarnings("unchecked")
    public List<Map<String, Object>> toRagChunks(Map<String, Object> result) {
        List<Map<String, Object>> ragChunks = new ArrayList<>();
        List<Map<String, Object>> chunks = (List<Map<String, Object>>) result.get("chunks");
        List<Map<String, String>> entities = (List<Map<String, String>>) result.get("entities");
        List<Map<String, String>> relations = (List<Map<String, String>>) result.get("relations");
        
        if (chunks == null) chunks = new ArrayList<>();
        if (entities == null) entities = new ArrayList<>();
        if (relations == null) relations = new ArrayList<>();
        
        for (Map<String, Object> chunk : chunks) {
            Map<String, Object> ragChunk = new LinkedHashMap<>();
            ragChunk.put("text", chunk.get("text"));
            
            Map<String, Object> metadata = new LinkedHashMap<>();
            metadata.put("entities", entities);
            metadata.put("relations", relations.subList(0, Math.min(5, relations.size())));
            metadata.put("source", "webweavex");
            ragChunk.put("metadata", metadata);
            
            ragChunks.add(ragChunk);
        }
        
        return ragChunks;
    }
    
    public Iterable<String> extractStream(String text) {
        return () -> new Iterator<String>() {
            private int stage = 0;
            private final String[] stages = {"cleaning", "chunking", "entities", "relations", "graph", "insights"};
            
            public boolean hasNext() {
                return stage < stages.length;
            }
            
            public String next() {
                return stages[stage++];
            }
        };
    }
    
    public String prettyPrint(Map<String, Object> result) {
        StringBuilder sb = new StringBuilder();
        sb.append("==================================================\n");
        sb.append("WebWeaveX Analysis\n");
        sb.append("==================================================\n\n");
        sb.append("ENTITY SUMMARY:\n");
        sb.append("------------------------------\n");
        
        Map<String, Object> insights = (Map<String, Object>) result.get("insights");
        if (insights != null) {
            Map<String, Integer> entityCounts = (Map<String, Integer>) insights.get("entity_counts");
            if (entityCounts != null) {
                for (Map.Entry<String, Integer> entry : entityCounts.entrySet()) {
                    sb.append(String.format("  %s: %d\n", entry.getKey(), entry.getValue()));
                }
            }
            
            Map<String, Object> stats = (Map<String, Object>) insights.get("stats");
            if (stats != null) {
                sb.append("\nSTATISTICS:\n");
                sb.append("------------------------------\n");
                sb.append(String.format("  Total Entities: %s\n", stats.getOrDefault("total_entities", 0)));
                sb.append(String.format("  Unique Entities: %s\n", stats.getOrDefault("unique_entities", 0)));
                sb.append(String.format("  Entity Types: %s\n", stats.getOrDefault("entity_types", 0)));
                sb.append(String.format("  Total Relations: %s\n", stats.getOrDefault("total_relations", 0)));
                sb.append(String.format("  Total Chunks: %s\n", stats.getOrDefault("total_chunks", 0)));
                sb.append(String.format("  Text Length: %s\n", stats.getOrDefault("text_length", 0)));
                sb.append(String.format("  Word Count: %s\n", stats.getOrDefault("word_count", 0)));
            }
        }
        
        sb.append("\n==================================================\n");
        return sb.toString();
    }
    
    public static Map<String, Object> getToolSchema() {
        Map<String, Object> schema = new LinkedHashMap<>();
        schema.put("name", "webweavex_extract");
        schema.put("description", "Extract structured intelligence from text");
        
        Map<String, Object> params = new LinkedHashMap<>();
        params.put("type", "object");
        
        Map<String, Object> properties = new LinkedHashMap<>();
        Map<String, String> inputProp = new LinkedHashMap<>();
        inputProp.put("type", "string");
        properties.put("input", inputProp);
        params.put("properties", properties);
        
        List<String> required = new ArrayList<>();
        required.add("input");
        params.put("required", required);
        
        schema.put("parameters", params);
        return schema;
    }
    
    public static List<Map<String, Object>> getAllTools() {
        List<Map<String, Object>> tools = new ArrayList<>();
        tools.add(getToolSchema());
        
        Map<String, Object> entitiesTool = new LinkedHashMap<>();
        entitiesTool.put("name", "webweavex_entities");
        entitiesTool.put("description", "Extract only entities from text");
        
        Map<String, Object> entitiesParams = new LinkedHashMap<>();
        entitiesParams.put("type", "object");
        Map<String, Object> entitiesProps = new LinkedHashMap<>();
        entitiesProps.put("input", Map.of("type", "string"));
        entitiesParams.put("properties", entitiesProps);
        entitiesParams.put("required", List.of("input"));
        entitiesTool.put("parameters", entitiesParams);
        tools.add(entitiesTool);
        
        return tools;
    }
    
    public static List<String> getCapabilities() {
        return Arrays.asList(
            "extract", "entities", "graph", "rag", 
            "agent_mode", "memory_export", "streaming"
        );
    }
    
    private Map<String, Object> createEmptyGraph() {
        Map<String, Object> graph = new LinkedHashMap<>();
        graph.put("nodes", new ArrayList<>());
        graph.put("edges", new ArrayList<>());
        return graph;
    }
    
    public Pipeline getPipeline() {
        return pipeline;
    }
    
    public static void main(String[] args) {
        WebWeaveX wx = new WebWeaveX();
        Map<String, Object> result = wx.extract("Contact test@example.com 555-1234");
        System.out.println("WebWeaveX Java initialized successfully");
    }
}
