import { getSpec, normalizeWhitespace, stripText, removeEmptyLines } from './utils';

export interface CleanerConfig {
  normalize_whitespace: boolean;
  strip: boolean;
  remove_empty_lines: boolean;
}

export class Cleaner {
  private config: CleanerConfig;
  private spec: any;

  constructor(config?: any) {
    this.spec = config || getSpec();
    const cleanConfig = this.spec.clean || {};
    this.config = {
      normalize_whitespace: cleanConfig.normalize_whitespace !== false,
      strip: cleanConfig.strip !== false,
      remove_empty_lines: cleanConfig.remove_empty_lines !== false,
    };
  }

  clean(text: string): string {
    if (!text) return '';

    if (this.config.normalize_whitespace) {
      text = this.normalizeWhitespace(text);
    }

    if (this.config.strip) {
      text = text.trim();
    }

    if (this.config.remove_empty_lines) {
      text = this.removeEmptyLines(text);
    }

    return text;
  }

  private normalizeWhitespace(text: string): string {
    return text.replace(/[ \t]+/g, ' ')
               .replace(/\n[ \t]+/g, '\n')
               .replace(/[\v]+/g, ' ');
  }

  private removeEmptyLines(text: string): string {
    return text.split('\n')
               .map(line => line.trim())
               .filter(line => line.length > 0)
               .join('\n');
  }
}
