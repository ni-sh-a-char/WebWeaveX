import { loadSpec, getSpec } from './utils';

export interface FetchConfig {
  timeout: number;
  retries: number;
  retry_delay: number;
  user_agent: string;
  accept_language: string;
  accept_encoding: string;
  follow_redirects: boolean;
  max_redirects: number;
}

export class Fetcher {
  private config: FetchConfig;
  private spec: any;

  constructor(config?: any) {
    this.spec = config || getSpec();
    const fetchConfig = this.spec.fetch || {};
    this.config = {
      timeout: fetchConfig.timeout || 10,
      retries: fetchConfig.retries || 3,
      retry_delay: fetchConfig.retry_delay || 1,
      user_agent: fetchConfig.user_agent || 'WebWeaveX/1.0',
      accept_language: fetchConfig.accept_language || 'en-US,en;q=0.9',
      accept_encoding: fetchConfig.accept_encoding || 'gzip, deflate',
      follow_redirects: fetchConfig.follow_redirects !== false,
      max_redirects: fetchConfig.max_redirects || 5,
    };
  }

  async fetch(url: string): Promise<string> {
    const headers: Record<string, string> = {
      'User-Agent': this.config.user_agent,
      'Accept-Language': this.config.accept_language,
      'Accept-Encoding': this.config.accept_encoding,
    };

    let lastError: Error | null = null;

    for (let attempt = 0; attempt < this.config.retries; attempt++) {
      try {
        const response = await fetch(url, {
          method: 'GET',
          headers,
          signal: AbortSignal.timeout(this.config.timeout * 1000),
          redirect: this.config.follow_redirects ? 'follow' : 'manual',
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.text();
      } catch (error) {
        lastError = error as Error;
        if (attempt < this.config.retries - 1) {
          await this.sleep(this.config.retry_delay * 1000);
        }
      }
    }

    throw lastError || new Error(`Failed to fetch ${url} after ${this.config.retries} attempts`);
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
