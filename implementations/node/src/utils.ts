import * as yaml from 'yaml';
import * as fs from 'fs';
import * as path from 'path';

export interface Spec {
  version: string;
  name: string;
  pipeline: {
    stages: string[];
    strict_order: boolean;
  };
  fetch: any;
  parse: any;
  clean: any;
  chunking: any;
  entity_patterns: any;
  graph: any;
  sorting: any;
  ai: any;
  agent_tools: any[];
  schemas: any;
  metadata: any;
  cache: any;
  async: any;
}

let specCache: Spec | null = null;

export function loadSpec(specPath?: string): Spec {
  if (specCache) return specCache;
  
  if (!specPath) {
    specPath = path.join(__dirname, '..', '..', '..', '..', 'core', 'specs', 'wxp_v1.yaml');
  }
  
  const content = fs.readFileSync(specPath, 'utf-8');
  specCache = yaml.parse(content) as Spec;
  return specCache;
}

export function getSpec(): Spec {
  return loadSpec();
}

export function deterministicSort<T>(items: T[]): T[] {
  return items.sort((a, b) => JSON.stringify(a).localeCompare(JSON.stringify(b)));
}

export function normalizeWhitespace(text: string): string {
  return text.replace(/\s+/g, ' ').trim();
}

export function stripText(text: string): string {
  return text.trim();
}

export function removeEmptyLines(text: string): string {
  return text.split('\n')
    .map(line => line.trim())
    .filter(line => line.length > 0)
    .join('\n');
}
