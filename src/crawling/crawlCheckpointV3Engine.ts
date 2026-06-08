/**
 * Converted from Python: core/crawling/crawl_checkpoint_v3_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { persistCrawlStateV3 } from "./crawlPersistenceV3Engine.js";

export function checkpointCrawlV3(state: any): any {
  return {"checkpoint": persistCrawlStateV3(state)};
}
export { persistCrawlStateV3 };
