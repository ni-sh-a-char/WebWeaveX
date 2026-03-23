import { Entity, GraphResult, GraphEdge } from './schema';
import { getSpec, deterministicSort } from './utils';

export interface GraphConfig {
  edge_rule: string;
  min_occurrence: number;
  directed: boolean;
}

export class GraphEngine {
  private config: GraphConfig;
  private spec: any;

  constructor(config?: any) {
    this.spec = config || getSpec();
    const graphConfig = this.spec.graph || {};
    this.config = {
      edge_rule: graphConfig.edge_rule || 'cooccurrence',
      min_occurrence: graphConfig.min_occurrence || 1,
      directed: graphConfig.directed || false,
    };
  }

  build(entities: Entity[]): GraphResult {
    if (!entities || entities.length === 0) {
      return { nodes: [], edges: [] };
    }

    const uniqueEntities = this.deduplicateEntities(entities);
    const sortedEntities = deterministicSort(uniqueEntities);
    const edges = this.buildEdges(sortedEntities);

    return {
      nodes: sortedEntities,
      edges: edges,
    };
  }

  buildFromText(entities: Entity[], _text: string): GraphResult {
    return this.build(entities);
  }

  private deduplicateEntities(entities: Entity[]): Entity[] {
    const seen = new Set<string>();
    const unique: Entity[] = [];

    for (const entity of entities) {
      const key = `${entity.type}:${entity.value}`;
      if (!seen.has(key)) {
        seen.add(key);
        unique.push(entity);
      }
    }

    return unique;
  }

  private buildEdges(entities: Entity[]): GraphEdge[] {
    const edges: GraphEdge[] = [];

    for (let i = 0; i < entities.length; i++) {
      for (let j = i + 1; j < entities.length; j++) {
        const edge = this.createEdge(entities[i], entities[j]);
        if (edge) {
          edges.push(edge);
        }
      }
    }

    return deterministicSort(edges);
  }

  private createEdge(entity1: Entity, entity2: Entity): GraphEdge | null {
    if (this.config.edge_rule === 'cooccurrence') {
      const edge: GraphEdge = {
        source: `${entity1.type}:${entity1.value}`,
        target: `${entity2.type}:${entity2.value}`,
        weight: 1,
      };

      if (this.config.directed) {
        edge.directed = true;
      }

      return edge;
    }

    return null;
  }
}
