/**
 * Converted from Python: core/semantic/semantic_divergence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function trackDivergence(views: any): any {
  var keys: Record<string, any> = {};
  var view: any;
  for (view of py.iter(py.or2(views, () => ([])))) {
    if (!((view !== null && typeof view === "object" && !Array.isArray(view) && !(view instanceof Set) && !(view instanceof Map)))) {
      continue;
    }
    var k: any;
    var v: any;
    for ([k, v] of py.iter(py.sorted(py.items(view)))) {
      py.setAdd(py.setdefault(keys, k, new Set()), py.toStr(v));
    }
  }
  var divergent: any = py.sorted(py.items(keys).filter(([k, vals]: any) => (py.len(vals) > 1)).map(([k, vals]: any) => k));
  return {"divergent_keys": divergent, "preserved": divergent, "evidence": ["semantic_divergence"], "lineage": {"views": py.len(py.or2(views, () => ([])))}};
}
