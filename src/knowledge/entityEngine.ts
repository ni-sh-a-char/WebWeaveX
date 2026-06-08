/**
 * Converted from Python: core/knowledge/entity_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildEntities(symbols: any): any {
  var unique: any = py.sorted(py.toSet(py.iter(py.or2(symbols, () => ([]))).filter((s: any) => py.truthy(s)).map((s: any) => py.toStr(s))));
  return {"entities": py.iter(unique).map((u: any) => ({"id": u, "kind": "symbol"})), "count": py.len(unique)};
}
