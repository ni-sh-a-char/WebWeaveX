/**
 * Converted from Python: core/crawling/advanced/crawl_persistence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { dumpsDeterministic } from "../../serialize/deterministicSerializer.js";

export function serializeCrawlState(state: any): any {
  return dumpsDeterministic(state);
}
export { dumpsDeterministic };
