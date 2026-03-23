import { Pipeline } from './pipeline';
import { Entity, CrawlResult, Chunk, GraphResult } from './schema';

export class WebWeaveX {
  private pipeline: Pipeline;

  constructor(config?: any) {
    this.pipeline = new Pipeline(config);
  }

  async crawl(url: string): Promise<CrawlResult> {
    return this.pipeline.crawl(url);
  }

  extract(html: string, url?: string): string {
    return this.pipeline.extract(html, url);
  }

  clean(text: string): string {
    return this.pipeline.clean(text);
  }

  chunk(text: string): Chunk[] {
    return this.pipeline.chunk(text);
  }

  entities(text: string): Entity[] {
    return this.pipeline.entities(text);
  }

  graph(textOrEntities: string | Entity[]): GraphResult {
    if (typeof textOrEntities === 'string') {
      return this.pipeline.graphFromText(textOrEntities);
    }
    return this.pipeline.graph(textOrEntities);
  }

  async rag(url: string, query: string): Promise<any> {
    return this.pipeline.rag(url, query);
  }

  async compare(urls: string[]): Promise<any> {
    return this.pipeline.compare(urls);
  }

  async diff(url1: string, url2: string): Promise<any> {
    return this.pipeline.diff(url1, url2);
  }

  async ask(url: string, prompt: string, _provider?: string): Promise<string> {
    const result = await this.crawl(url);
    const context = result.text.substring(0, 4000);
    return JSON.stringify({
      status: 'no_api',
      message: 'AI API not configured. Set API key for OpenAI, OpenRouter, Groq, or Ollama.',
      prompt_received: prompt.substring(0, 100) + (prompt.length > 100 ? '...' : ''),
    }, null, 2);
  }

  async agent_task(task: string): Promise<any> {
    const taskLower = task.toLowerCase();
    
    const urlMatch = task.match(/https?:\/\/[^\s<>"']+/);
    
    if (taskLower.includes('crawl') && urlMatch) {
      const result = await this.crawl(urlMatch[0]);
      return {
        task,
        tool: 'crawl',
        result: { url: result.url, text: result.text.substring(0, 500) + '...' },
      };
    }
    
    if (taskLower.includes('graph')) {
      const text = task.match(/text[:\s]+["']?([^"']+)["']?/i)?.[1] || '';
      const result = this.graph(text);
      return {
        task,
        tool: 'graph',
        result: result,
      };
    }
    
    return {
      task,
      error: 'Could not determine appropriate tool',
    };
  }

  list_agent_tools(): string[] {
    return ['crawl', 'rag', 'graph', 'compare', 'weave', 'diff'];
  }
}
