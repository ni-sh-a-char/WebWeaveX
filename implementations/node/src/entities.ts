import { Entity } from './schema';
import { getSpec, deterministicSort } from './utils';

export class EntityEngine {
  private patterns: Record<string, RegExp> = {};
  private spec: any;

  constructor(config?: any) {
    this.spec = config || getSpec();
    this.compilePatterns();
  }

  private compilePatterns(): void {
    const patterns = this.spec.entity_patterns || {};
    for (const [name, config] of Object.entries(patterns)) {
      const pattern = config as { regex?: string };
      if (pattern && pattern.regex) {
        try {
          this.patterns[name] = new RegExp(pattern.regex, 'g');
        } catch (e) {
          // Skip invalid patterns
        }
      }
    }
  }

  extract(text: string): Entity[] {
    if (!text) return [];

    const entitiesSet = new Set<string>();
    const entities: Entity[] = [];

    for (const [name, pattern] of Object.entries(this.patterns)) {
      const regex = new RegExp(pattern.source, 'gi');
      let match;
      while ((match = regex.exec(text)) !== null) {
        const value = (match[0] || '').trim();
        if (value) {
          const key = `${name}:${value}`;
          if (!entitiesSet.has(key)) {
            entitiesSet.add(key);
            entities.push({ type: name, value: value });
          }
        }
      }
    }

    return deterministicSort(entities);
  }

  extractByType(text: string, entityType: string): Entity[] {
    if (!text || !this.patterns[entityType]) return [];

    const regex = new RegExp(this.patterns[entityType].source, 'gi');
    const entities: Entity[] = [];
    const seen = new Set<string>();
    let match;

    while ((match = regex.exec(text)) !== null) {
      const value = (match[0] || '').trim();
      if (value && !seen.has(value)) {
        seen.add(value);
        entities.push({ type: entityType, value: value });
      }
    }

    return entities.sort((a, b) => a.value.localeCompare(b.value));
  }
}
