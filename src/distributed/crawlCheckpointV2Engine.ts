/**
 * Converted from Python: core/distributed/crawl_checkpoint_v2_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { dumpsDeterministic } from "../utils/deterministicSerializer.js";

export function createCrawlCheckpointV2(state: any): any {
  var st: any = py.or2(state, () => ({}));
  return {"checkpoint": dumpsDeterministic(st)};
}
export { dumpsDeterministic };
