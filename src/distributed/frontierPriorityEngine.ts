/**
 * Converted from Python: core/distributed/frontier_priority_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function prioritize(frontier: any): any {
  return py.sorted(py.toSet(py.or2(frontier, () => ([]))));
}
