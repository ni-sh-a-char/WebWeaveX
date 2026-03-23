import * as cheerio from 'cheerio';
import { getSpec } from './utils';

export interface ParserConfig {
  extract_visible_text: boolean;
  remove_scripts: boolean;
  remove_styles: boolean;
  remove_comments: boolean;
  remove_hidden: boolean;
}

export class Parser {
  private config: ParserConfig;
  private spec: any;

  constructor(config?: any) {
    this.spec = config || getSpec();
    const parseConfig = this.spec.parse || {};
    this.config = {
      extract_visible_text: parseConfig.extract_visible_text !== false,
      remove_scripts: parseConfig.remove_scripts !== false,
      remove_styles: parseConfig.remove_styles !== false,
      remove_comments: parseConfig.remove_comments !== false,
      remove_hidden: parseConfig.remove_hidden !== false,
    };
  }

  parse(html: string, url?: string): string {
    const $ = cheerio.load(html);

    if (this.config.remove_scripts) {
      $('script').remove();
    }

    if (this.config.remove_styles) {
      $('style').remove();
    }

    if (this.config.remove_comments) {
      $('*').contents().each((_, node) => {
        if (node.type === 'comment') {
          $(node).remove();
        }
      });
    }

    if (this.config.extract_visible_text) {
      return this.extractVisibleText($);
    }

    return $('body').text() || '';
  }

  private extractVisibleText($: cheerio.CheerioAPI): string {
    const skipTags = ['script', 'style', 'noscript', 'iframe', 'svg', 'noscript', 'head'];
    const textParts: string[] = [];

    $('body').contents().each((_, node) => {
      if (node.type === 'text') {
        const text = $(node).text().trim();
        if (text) {
          const parent = $(node).parent();
          if (parent.length && !skipTags.includes(parent.get(0)?.tagName || '')) {
            textParts.push(text);
          }
        }
      } else if (node.type === 'tag') {
        const tagName = node.tagName?.toLowerCase() || '';
        if (!skipTags.includes(tagName)) {
          const text = $(node).text().trim();
          if (text) {
            textParts.push(text);
          }
        }
      }
    });

    return textParts.join(' ').replace(/\s+/g, ' ').trim();
  }

  extractMetadata(html: string, url?: string): Record<string, string> {
    const $ = cheerio.load(html);
    const metadata: Record<string, string> = {};

    const title = $('title').text();
    if (title) {
      metadata['title'] = title.trim();
    }

    $('meta').each((_, el) => {
      const name = $(el).attr('name') || $(el).attr('property') || '';
      const content = $(el).attr('content') || '';
      if (name && content) {
        metadata[name] = content;
      }
    });

    return metadata;
  }
}
