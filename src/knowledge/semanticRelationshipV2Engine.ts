/**
 * Converted from Python: core/knowledge/semantic_relationship_v2_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildSemanticRelationships(symbols: any, dependencies: any): any {
  var sym: any = py.sorted(py.toSet(py.iter(py.or2(symbols, () => ([]))).filter((s: any) => py.truthy(s)).map((s: any) => String(py.strip(py.toStr(s))).toLowerCase())));
  var deps: any = py.sorted(py.toSet(py.iter(py.or2(dependencies, () => ([]))).filter((d: any) => py.truthy(d)).map((d: any) => String(py.strip(py.toStr(d))).toLowerCase())));
  var edges: any = py.range(py.max([0, py.sub(py.len(sym), 1)])).map((i: any) => ({"from": py.at(sym, i), "to": py.at(sym, py.add(i, 1))}));
  var d: any;
  for (d of py.iter(py.slice(deps, null, 50))) {
    if (py.truthy(sym)) {
      py.listAppend(edges, {"from": py.at(sym, 0), "to": d});
    }
  }
  return {"nodes": sym, "edges": py.sorted(edges, {key: ((e: any) => [py.at(e, "from"), py.at(e, "to")]) as (item: any) => any})};
}
