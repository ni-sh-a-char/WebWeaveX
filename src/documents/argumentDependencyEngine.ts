/**
 * Converted from Python: core/documents/argument_dependency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_EDGES: any = 300;
export function buildArgumentDependencies(text: any): any {
  var lines: any = py.iter(py.splitlines(text)).filter((ln: any) => py.truthy(py.strip(ln))).map((ln: any) => py.strip(ln));
  var claims: any = py.enumerate(lines).map(([i, ln]: any) => ({"id": `c${py.toStr(i)}`, "order": i, "content": ln}));
  var r: any = reconstructArgumentDependencies(claims);
  var nodes: any = py.iter(claims).map((c: any) => ({"id": py.at(c, "id"), "content": py.get(c, "content")}));
  return {"dependencies": py.get(r, "edges", []), "nodes": nodes, "evidence": ["discourse:argument_order"], "deterministic": true};
}
export function reconstructArgumentDependencies(claims: any): any {
  var ordered: any = py.sorted(claims, {key: ((c: any) => py.toInt(py.get(c, "order", 0))) as (item: any) => any});
  var edges: any[] = [];
  var idx: any;
  for (idx = 1; idx < py.len(ordered); idx++) {
    const _d1 = py.iter([py.at(ordered, py.sub(idx, 1)), py.at(ordered, idx)]) as any[];
    var prev_c: any = _d1[0];
    var cur_c: any = _d1[1];
    if (py.truthy(py.get(cur_c, "depends_on"))) {
      py.listAppend(edges, {"from": py.get(cur_c, "depends_on"), "to": py.get(cur_c, "id"), "metadata": {"kind": "argument_support", "basis": "explicit_dependency"}});
    } else {
      py.listAppend(edges, {"from": py.get(prev_c, "id"), "to": py.get(cur_c, "id"), "metadata": {"kind": "argument_sequence", "basis": "document_order"}});
    }
  }
  return {"edges": py.slice(edges, null, MAX_EDGES), "count": py.min([py.len(edges), MAX_EDGES]), "deterministic": true};
}
