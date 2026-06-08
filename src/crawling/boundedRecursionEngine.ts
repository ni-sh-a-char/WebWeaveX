/**
 * Converted from Python: core/crawling/bounded_recursion_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function recursionGuardV3(depth: any, max_depth: any = 3): any {
  return {"allowed": (py.toInt(depth) <= py.toInt(max_depth)), "depth": py.toInt(depth), "max_depth": py.toInt(max_depth)};
}
