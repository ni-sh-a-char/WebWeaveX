/**
 * Converted from Python: core/crawling/intelligence/adaptive_recursion_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function adaptiveRecursion(depth: any, edges: any, max_depth: any = 3): any {
  if ((edges > 5000)) {
    max_depth = py.min([max_depth, 2]);
  }
  return {"allowed": py.le(depth, max_depth), "max_depth": max_depth};
}
