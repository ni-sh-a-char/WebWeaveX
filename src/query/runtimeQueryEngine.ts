/**
 * Converted from Python: core/query/runtime_query_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function queryRuntimeIr(runtime_ir: any, field: any): any {
  var value: any = py.get(runtime_ir, field);
  return {"field": field, "value": value, "found": (value !== null && value !== undefined), "deterministic": true};
}
