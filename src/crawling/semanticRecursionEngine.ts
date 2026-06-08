/**
 * Converted from Python: core/crawling/semantic_recursion_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { crawl } from "./crawlerEngine.js";

export function recursiveExtractV3(url: any, max_depth: any = 3, max_pages: any = 100): any {
  return crawl(url, max_depth, max_pages);
}
export { crawl };
