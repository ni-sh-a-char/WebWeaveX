/**
 * Converted from Python: core/crawling/crawl_persistence_v3_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { dumpsDeterministic } from "../utils/deterministicSerializer.js";

export function persistCrawlStateV3(state: any): any {
  return dumpsDeterministic(py.or2(state, () => ({})));
}
export { dumpsDeterministic };
