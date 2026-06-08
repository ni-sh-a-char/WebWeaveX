/**
 * Converted from Python: core/distributed/recursive_dedup_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function recursiveDedup(urls: any): any {
  return py.sorted(py.toSet(py.or2(urls, () => ([]))));
}
