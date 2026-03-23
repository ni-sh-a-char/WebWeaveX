/** Graph building - entity co-occurrence graph */

export class GraphEngine {
  constructor(config = {}) {
    this.directed = false;
  }

  build(entities) {
    if (!entities || entities.length === 0) {
      return { nodes: [], edges: [] };
    }
    
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
    
    const nodes = uniqueEntities.map(e => ({
      id: `${e.type}:${e.value}`,
      type: e.type,
      value: e.value
    }));
    
    const edges = [];
    for (let i = 0; i < uniqueEntities.length; i++) {
      for (let j = i + 1; j < uniqueEntities.length; j++) {
        edges.push({
          source: `${uniqueEntities[i].type}:${uniqueEntities[i].value}`,
          target: `${uniqueEntities[j].type}:${uniqueEntities[j].value}`,
          weight: 1
        });
      }
    }
    
    nodes.sort((a, b) => a.id.localeCompare(b.id));
    edges.sort((a, b) => {
      if (a.source !== b.source) return a.source.localeCompare(b.source);
      return a.target.localeCompare(b.target);
    });
    
    return { nodes, edges };
  }
}
