/** Relation extraction - entity co-occurrence */

export class RelationEngine {
  constructor(config = {}) {
    this.edgeType = "cooccurrence";
  }

  extract(entities, chunks) {
    if (!entities || entities.length === 0) return [];
    
    const uniqueEntities = [];
    const seen = new Set();
    
    for (const e of entities) {
      const key = `${e.type}:${e.value}`;
      if (!seen.has(key)) {
        seen.add(key);
        uniqueEntities.push(e);
      }
    }
    
    uniqueEntities.sort((a, b) => {
      if (a.type !== b.type) return a.type.localeCompare(b.type);
      return a.value.localeCompare(b.value);
    });
    
    const relations = [];
    for (let i = 0; i < uniqueEntities.length; i++) {
      for (let j = i + 1; j < uniqueEntities.length; j++) {
        relations.push({
          source: `${uniqueEntities[i].type}:${uniqueEntities[i].value}`,
          target: `${uniqueEntities[j].type}:${uniqueEntities[j].value}`,
          type: this.edgeType
        });
      }
    }
    
    relations.sort((a, b) => {
      if (a.source !== b.source) return a.source.localeCompare(b.source);
      return a.target.localeCompare(b.target);
    });
    
    return relations;
  }
}
