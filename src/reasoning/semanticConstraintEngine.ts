/**
 * Converted from Python: core/reasoning/semantic_constraint_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function applySemanticConstraints(bundle: any, max_depth: any = 20): any {
  var lineage: any = py.or2(py.get(bundle, "lineage", {}), () => ({}));
  var depth: any = (((lineage !== null && typeof lineage === "object" && !Array.isArray(lineage) && !(lineage instanceof Set) && !(lineage instanceof Map))) ? py.get(lineage, "depth", 0) : 0);
  var bounded: any = py.le(depth, max_depth);
  return {...(bundle), "constraints": {"max_depth": max_depth, "satisfied": bounded}};
}
