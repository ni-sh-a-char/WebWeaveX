/**
 * Converted from Python: core/distributed/distributed_frontier_v2_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildDistributedFrontierV2(urls: any): any {
  return py.sorted(py.toSet(py.or2(urls, () => ([]))));
}
