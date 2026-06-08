/**
 * Converted from Python: core/distributed/crawl_persistence_v2_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { dumpsDeterministic } from "../utils/deterministicSerializer.js";

export function serializeCrawlStateV2(state: any): any {
  return dumpsDeterministic(py.or2(state, () => ({})));
}
export { dumpsDeterministic };
