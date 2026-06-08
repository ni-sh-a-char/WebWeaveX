/**
 * Converted from Python: core/ir/_base.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function emptyConfidence(): any {
  return {"score": py.F(0.0), "basis": [], "deterministic": true};
}
export function emptyLineage(stage: any = "ir"): any {
  return {"stages": [{"stage": stage}], "depth": 1};
}
export function mergeEvidence(...parts: any[]): any {
  var items: any = py.sorted(py.toSet(py.iter(parts).flatMap((part: any) => py.iter(py.or2(part, () => ([]))).filter((e: any) => py.truthy(e)).map((e: any) => py.toStr(e)))));
  return {"items": items, "count": py.len(items)};
}
