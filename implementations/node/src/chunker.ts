import { Chunk } from './schema';
import { getSpec } from './utils';

export interface ChunkingConfig {
  size: number;
  overlap: number;
  method: string;
  preserve_words: boolean;
}

export class Chunker {
  private config: ChunkingConfig;
  private spec: any;

  constructor(config?: any) {
    this.spec = config || getSpec();
    const chunkingConfig = this.spec.chunking || {};
    this.config = {
      size: chunkingConfig.size || 500,
      overlap: chunkingConfig.overlap || 50,
      method: chunkingConfig.method || 'sliding_window',
      preserve_words: chunkingConfig.preserve_words !== false,
    };
  }

  chunk(text: string): Chunk[] {
    if (!text) return [];

    const chunks: Chunk[] = [];
    let start = 0;
    let index = 0;

    while (start < text.length) {
      let end = start + this.config.size;

      if (this.config.preserve_words && end < text.length) {
        end = this.findWordBoundary(text, end);
      }

      const chunkText = text.substring(start, end);
      if (chunkText.trim()) {
        chunks.push({
          text: chunkText,
          index: index,
          start: start,
          end: end,
        });
        index++;
      }

      start = end - this.config.overlap;
      if (start < 0) start = 0;
    }

    return chunks;
  }

  private findWordBoundary(text: string, position: number): number {
    if (position >= text.length) return position;

    const searchStart = Math.max(0, position - 50);
    for (let i = position; i >= searchStart; i--) {
      if (/\s/.test(text[i])) {
        return i;
      }
    }

    return position;
  }
}
