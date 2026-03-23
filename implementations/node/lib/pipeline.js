/** Pipeline - orchestrates the processing chain */

import { Cleaner } from './cleaner.js';
import { Chunker } from './chunker.js';
import { EntityEngine } from './entities.js';
import { RelationEngine } from './relations.js';
import { GraphEngine } from './graph.js';
import { InsightsEngine } from './insights.js';

export class Pipeline {
  constructor(config = {}) {
    this.cleaner = new Cleaner(config);
    this.chunker = new Chunker(config);
    this.entityEngine = new EntityEngine(config);
    this.relationEngine = new RelationEngine(config);
    this.graphEngine = new GraphEngine(config);
    this.insightsEngine = new InsightsEngine(config);
  }

  extractFromText(text) {
    const cleanedText = this.cleaner.clean(text);
    const chunks = this.chunker.chunk(cleanedText);
    const entities = this.entityEngine.extract(cleanedText);
    const relations = this.relationEngine.extract(entities, chunks);
    const graph = this.graphEngine.build(entities);
    const insights = this.insightsEngine.compute(entities, chunks, cleanedText);

    return this._buildResult("", "", cleanedText, chunks, entities, relations, graph, insights);
  }

  _buildResult(url, title, text, chunks, entities, relations, graph, insights) {
    const sortedEntities = [...entities].sort((a, b) => {
      if (a.type !== b.type) return a.type.localeCompare(b.type);
      return a.value.localeCompare(b.value);
    });

    const sortedChunks = [...chunks].sort((a, b) => a.index - b.index);

    const sortedRelations = [...relations].sort((a, b) => {
      if (a.source !== b.source) return a.source.localeCompare(b.source);
      return a.target.localeCompare(b.target);
    });

    return {
      meta: { title, url },
      content: { text },
      chunks: sortedChunks,
      entities: sortedEntities,
      relations: sortedRelations,
      graph: {
        nodes: [...graph.nodes].sort((a, b) => a.id.localeCompare(b.id)),
        edges: [...graph.edges].sort((a, b) => {
          if (a.source !== b.source) return a.source.localeCompare(b.source);
          return a.target.localeCompare(b.target);
        })
      },
      insights
    };
  }
}
