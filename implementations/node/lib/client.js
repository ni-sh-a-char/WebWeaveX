/** Main client for WebWeaveX */

import { Pipeline } from './pipeline.js';

function extractAgent(result) {
  const text = result.content?.text || "";
  const entities = result.entities || [];
  const relations = result.relations || [];
  
  const entityCounts = {};
  const entityTypes = new Set();
  for (const e of entities) {
    const key = `${e.type}:${e.value}`;
    entityCounts[key] = (entityCounts[key] || 0) + 1;
    entityTypes.add(e.type);
  }
  
  const summary = entities.length === 0 
    ? "No entities extracted from input text."
    : `Extracted ${entities.length} entities from text.`;
  
  const actions = [];
  const types = new Set(entities.map(e => e.type));
  if (types.has("url")) actions.push("crawl");
  if (types.has("email")) actions.push("contact");
  if (types.has("phone")) actions.push("call");
  if (entities.length > 5) actions.push("extract_more");
  if (actions.length === 0) actions.push("analyze");
  
  const confidence = text.length > 0 
    ? Math.min((entities.length + relations.length * 0.5) / Math.max(text.length, 1) * 10, 1.0) 
    : 0.0;
  
  return {
    task: "web_analysis",
    input: text.slice(0, 500),
    output: result,
    summary,
    actions,
    confidence: Math.round(confidence * 100) / 100
  };
}

function toMemoryBlock(result) {
  return {
    type: "webweavex_memory",
    entities: result.entities || [],
    relations: result.relations || [],
    graph: result.graph || { nodes: [], edges: [] },
    timestamp: new Date().toISOString(),
    source: "webweavex"
  };
}

function toRagChunks(result) {
  const chunks = result.chunks || [];
  const entities = result.entities || [];
  const relations = result.relations || [];
  
  return chunks.map(chunk => ({
    text: chunk.text,
    metadata: {
      entities: entities.filter(e => chunk.text.includes(e.value)),
      relations: relations.slice(0, 5),
      source: "webweavex"
    }
  }));
}

function prettyPrint(result) {
  const insights = result.insights || {};
  const stats = insights.stats || {};
  const entityCounts = insights.entity_counts || {};
  
  const lines = [
    "=" + "=".repeat(49),
    "WebWeaveX Analysis",
    "=" + "=".repeat(49),
    "",
    "ENTITY SUMMARY:",
    "-".repeat(30),
  ];
  
  for (const [key, count] of Object.entries(entityCounts).sort()) {
    lines.push(`  ${key}: ${count}`);
  }
  
  lines.push(
    "",
    "STATISTICS:",
    "-".repeat(30),
    `  Total Entities: ${stats.total_entities || 0}`,
    `  Unique Entities: ${stats.unique_entities || 0}`,
    `  Entity Types: ${stats.entity_types || 0}`,
    `  Total Relations: ${stats.total_relations || 0}`,
    `  Total Chunks: ${stats.total_chunks || 0}`,
    `  Text Length: ${stats.text_length || 0}`,
    `  Word Count: ${stats.word_count || 0}`,
    "",
    "=" + "=".repeat(49),
  );
  
  return lines.join("\n");
}

function getToolSchema() {
  return {
    name: "webweavex_extract",
    description: "Extract structured intelligence from text",
    parameters: {
      type: "object",
      properties: {
        input: { type: "string" }
      },
      required: ["input"]
    }
  };
}

function getAllTools() {
  return [
    getToolSchema(),
    {
      name: "webweavex_entities",
      description: "Extract only entities from text",
      parameters: {
        type: "object",
        properties: { input: { type: "string" } },
        required: ["input"]
      }
    },
    {
      name: "webweavex_graph",
      description: "Extract entity graph from text",
      parameters: {
        type: "object",
        properties: { input: { type: "string" } },
        required: ["input"]
      }
    }
  ];
}

function getCapabilities() {
  return [
    "extract",
    "entities",
    "graph",
    "rag",
    "agent_mode",
    "memory_export",
    "streaming"
  ];
}

export class WebWeaveX {
  constructor(config = {}) {
    this.pipeline = new Pipeline(config);
  }

  extract(textOrHtml) {
    try {
      if (!textOrHtml) {
        return this.pipeline.extractFromText("");
      }
      
      if (textOrHtml.trim().startsWith("<") && textOrHtml.toLowerCase().includes("</html>")) {
        return this.pipeline.extractFromHtml(textOrHtml);
      }
      
      return this.pipeline.extractFromText(textOrHtml);
    } catch (e) {
      return {
        meta: { title: "", url: "" },
        content: { text: "" },
        chunks: [],
        entities: [],
        relations: [],
        graph: { nodes: [], edges: [] },
        insights: { entity_counts: {}, stats: {}, top_entities: [] }
      };
    }
  }

  clean(text) {
    return this.pipeline.cleaner.clean(text);
  }

  chunk(text) {
    return this.pipeline.chunker.chunk(text);
  }

  entities(text) {
    return this.pipeline.entityEngine.extract(text);
  }

  graph(text) {
    const entities = this.pipeline.entityEngine.extract(text);
    return this.pipeline.graphEngine.build(entities);
  }

  extractAgent(text) {
    try {
      const result = this.extract(text);
      return extractAgent(result);
    } catch (e) {
      return {
        task: "web_analysis",
        input: text?.slice(0, 500) || "",
        output: {},
        summary: `Error: ${e.message}`,
        actions: [],
        confidence: 0.0
      };
    }
  }

  toMemoryBlock(result) {
    try {
      return toMemoryBlock(result);
    } catch (e) {
      return {
        type: "webweavex_memory",
        entities: [],
        relations: [],
        graph: { nodes: [], edges: [] },
        timestamp: new Date().toISOString(),
        source: "webweavex"
      };
    }
  }

  toRagChunks(result) {
    try {
      return toRagChunks(result);
    } catch (e) {
      return [];
    }
  }

  *extractStream(text) {
    try {
      yield "cleaning";
      yield "chunking";
      yield "entities";
      yield "relations";
      yield "graph";
      yield "insights";
    } catch (e) {
      yield "error";
      yield `Error: ${e.message}`;
    }
  }

  prettyPrint(result) {
    try {
      return prettyPrint(result);
    } catch (e) {
      return `Error formatting output: ${e.message}`;
    }
  }

  static getToolSchema() {
    return getToolSchema();
  }

  static getAllTools() {
    return getAllTools();
  }

  static getCapabilities() {
    return getCapabilities();
  }
}

export default WebWeaveX;
