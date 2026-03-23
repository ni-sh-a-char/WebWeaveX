import { Entity, CrawlResult, Chunk, GraphResult } from './schema';
import { getSpec } from './utils';
import { Fetcher } from './fetcher';
import { Parser } from './parser';
import { Cleaner } from './cleaner';
import { Chunker } from './chunker';
import { EntityEngine } from './entities';
import { GraphEngine } from './graph';

export class Pipeline {
  private fetcher: Fetcher;
  private parser: Parser;
  private cleaner: Cleaner;
  private chunker: Chunker;
  private entityEngine: EntityEngine;
  private graphEngine: GraphEngine;

  constructor(config?: any) {
    this.fetcher = new Fetcher(config);
    this.parser = new Parser(config);
    this.cleaner = new Cleaner(config);
    this.chunker = new Chunker(config);
    this.entityEngine = new EntityEngine(config);
    this.graphEngine = new GraphEngine(config);
  }

  async crawl(url: string): Promise<CrawlResult> {
    const html = await this.fetcher.fetch(url);
    const text = this.parser.parse(html, url);
    const cleanedText = this.cleaner.clean(text);
    const chunks = this.chunker.chunk(cleanedText);
    const entities = this.entityEngine.extract(cleanedText);
    const graph = this.graphEngine.build(entities);

    return {
      url,
      text: cleanedText,
      chunks,
      entities,
      graph,
      metadata: {
        url,
        version: '1.0.0',
      },
    };
  }

  extract(html: string, url?: string): string {
    return this.parser.parse(html, url);
  }

  clean(text: string): string {
    return this.cleaner.clean(text);
  }

  chunk(text: string): Chunk[] {
    return this.chunker.chunk(text);
  }

  entities(text: string): Entity[] {
    return this.entityEngine.extract(text);
  }

  graph(entities: Entity[]): GraphResult {
    return this.graphEngine.build(entities);
  }

  graphFromText(text: string): GraphResult {
    const entities = this.entityEngine.extract(text);
    return this.graphEngine.build(entities);
  }

  async rag(url: string, query: string): Promise<any> {
    const result = await this.crawl(url);
    const queryLower = query.toLowerCase();
    const relevantChunks: Chunk[] = [];

    for (const chunk of result.chunks || []) {
      const chunkLower = chunk.text.toLowerCase();
      const queryWords = queryLower.split(/\s+/);
      if (queryWords.some(word => chunkLower.includes(word))) {
        relevantChunks.push(chunk);
      }
    }

    return {
      url,
      query,
      chunks: relevantChunks.slice(0, 5).map(c => ({
        text: c.text,
        index: c.index,
        start: c.start,
        end: c.end,
      })),
      entities: result.entities?.map(e => ({ type: e.type, value: e.value })) || [],
    };
  }

  async compare(urls: string[]): Promise<any> {
    const results: Array<{ url: string; entities: Entity[] }> = [];

    for (const url of urls) {
      const result = await this.crawl(url);
      results.push({ url, entities: result.entities || [] });
    }

    const common = this.findCommonEntities(results.map(r => r.entities));
    const unique: Record<string, Entity[]> = {};

    for (const result of results) {
      const url = result.url;
      unique[url] = result.entities.filter(e => !common.some(c => c.type === e.type && c.value === e.value));
    }

    return {
      urls,
      common_entities: common.map(e => ({ type: e.type, value: e.value })),
      unique_entities: Object.fromEntries(
        Object.entries(unique).map(([url, ents]) => [url, ents.map(e => ({ type: e.type, value: e.value }))])
      ),
    };
  }

  async diff(url1: string, url2: string): Promise<any> {
    const result1 = await this.crawl(url1);
    const result2 = await this.crawl(url2);

    const entities1 = new Set(result1.entities?.map(e => `${e.type}:${e.value}`) || []);
    const entities2 = new Set(result2.entities?.map(e => `${e.type}:${e.value}`) || []);

    const commonEntities: Entity[] = [];
    const uniqueToUrl1: Entity[] = [];
    const uniqueToUrl2: Entity[] = [];

    for (const e of result1.entities || []) {
      const key = `${e.type}:${e.value}`;
      if (entities2.has(key)) {
        commonEntities.push(e);
      } else {
        uniqueToUrl1.push(e);
      }
    }

    for (const e of result2.entities || []) {
      const key = `${e.type}:${e.value}`;
      if (!entities1.has(key)) {
        uniqueToUrl2.push(e);
      }
    }

    return {
      url1,
      url2,
      common_entities: commonEntities.map(e => ({ type: e.type, value: e.value })),
      unique_to_url1: uniqueToUrl1.map(e => ({ type: e.type, value: e.value })),
      unique_to_url2: uniqueToUrl2.map(e => ({ type: e.type, value: e.value })),
    };
  }

  private findCommonEntities(entityLists: Entity[][]): Entity[] {
    if (!entityLists.length) return [];

    const common = new Set(entityLists[0].map(e => `${e.type}:${e.value}`));
    for (let i = 1; i < entityLists.length; i++) {
      const set = new Set(entityLists[i].map(e => `${e.type}:${e.value}`));
      for (const key of common) {
        if (!set.has(key)) {
          common.delete(key);
        }
      }
    }

    return Array.from(common).map(key => {
      const [type, value] = key.split(':');
      return { type, value };
    });
  }
}
