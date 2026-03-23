/** Insights engine - analytics */

export class InsightsEngine {
  constructor(config = {}) {
    this.topN = 10;
    this.includeStats = true;
  }

  compute(entities, chunks, text) {
    const entityCounts = {};
    
    for (const e of entities) {
      const key = `${e.type}:${e.value}`;
      entityCounts[key] = (entityCounts[key] || 0) + 1;
    }
    
    const sortedCounts = Object.entries(entityCounts)
      .sort((a, b) => {
        if (b[1] !== a[1]) return b[1] - a[1];
        return a[0].localeCompare(b[0]);
      })
      .slice(0, this.topN);
    
    const topEntities = sortedCounts.map(([key, count]) => {
      const [type, ...valueParts] = key.split(":");
      return {
        type,
        value: valueParts.join(":"),
        count
      };
    });
    
    const stats = {};
    if (this.includeStats) {
      stats.total_entities = entities.length;
      stats.unique_entities = Object.keys(entityCounts).length;
      stats.entity_types = new Set(entities.map(e => e.type)).size;
      stats.total_relations = 0;
      if (chunks && chunks.length > 0) {
        stats.total_chunks = chunks.length;
      }
      if (text) {
        stats.text_length = text.length;
        stats.word_count = text.split(/\s+/).filter(w => w).length;
      }
    }
    
    const sortedEntityCounts = {};
    const sortedKeys = Object.keys(entityCounts).sort((a, b) => a.localeCompare(b));
    for (const k of sortedKeys) {
      sortedEntityCounts[k] = entityCounts[k];
    }
    
    return {
      top_entities: topEntities,
      stats,
      entity_counts: sortedEntityCounts
    };
  }
}
