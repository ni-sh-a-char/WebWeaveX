/**
 * Converted from Python: core/evidence/recursive_semantic_independence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelRecursiveSemanticIndependence(keys: any, depth: any): any {
  return {"independent": py.or2((py.len(py.toSet(keys)) > 1), () => ((depth < 2))), "reliance_blocked": true};
}
