/**
 * Converted from Python: core/distributed/distributed_frontier_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildFrontier(urls: any): any {
  return py.sorted(py.toSet(py.or2(urls, () => ([]))));
}
