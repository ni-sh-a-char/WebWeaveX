/**
 * Converted from Python: core/evidence/unsupported_scope_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelUnsupportedScope(dimensions: any): any {
  var dims: any = py.sorted(py.toSet(py.iter(py.or2(dimensions, () => ([]))).filter((d: any) => py.truthy(d)).map((d: any) => py.toStr(d))));
  return {"dimensions": dims, "scope_unsupported": py.truthy(dims), "count": py.len(dims)};
}
