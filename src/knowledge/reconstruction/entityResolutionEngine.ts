/**
 * Converted from Python: core/knowledge/reconstruction/entity_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function resolveEntities(items: any): any {
  var vals: any = py.sorted(py.toSet(py.iter(py.or2(items, () => ([]))).filter((x: any) => py.truthy(x)).map((x: any) => String(py.strip(py.or2(x, () => ("")))).toLowerCase())));
  return {"entities": vals};
}
