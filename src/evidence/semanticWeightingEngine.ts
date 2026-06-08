/**
 * Converted from Python: core/evidence/semantic_weighting_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function weightEvidenceItems(items: any): any {
  var weights: any[] = [];
  var item: any;
  for (item of py.iter(py.or2(items, () => ([])))) {
    if (!((item !== null && typeof item === "object" && !Array.isArray(item) && !(item instanceof Set) && !(item instanceof Map)))) {
      continue;
    }
    var ev: any = py.get(item, "evidence", []);
    var count: any = ((Array.isArray(ev)) ? py.len(ev) : 1);
    py.listAppend(weights, {"id": py.get(item, "id", ""), "weight": py.round(py.min([py.F(1.0), py.add(py.F(0.2), py.mul(count, py.F(0.15)))]), 3), "evidence": ev});
  }
  return {"weights": py.sorted(weights, {key: ((x: any) => py.at(x, "id")) as (item: any) => any}), "evidence": ["semantic_weighting"]};
}
