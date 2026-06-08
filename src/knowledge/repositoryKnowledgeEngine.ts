/**
 * Converted from Python: core/knowledge/repository_knowledge_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function _uniqueSorted(values: any): any {
  return py.sorted(py.toSet(py.iter(values).filter((v: any) => py.truthy(v)).map((v: any) => py.toStr(v))));
}
export function buildRepositoryKnowledge(repo: any): any {
  var r: any = py.or2(repo, () => ({}));
  var nodes: any = _uniqueSorted(py.add(py.add(py.add(py.or2(py.get(r, "symbols", []), () => ([])), py.or2(py.get(r, "dependencies", []), () => ([]))), py.or2(py.get(r, "frameworks", []), () => ([]))), py.or2(py.get(r, "services", []), () => ([]))));
  var edges: any = py.range(py.max([0, py.sub(py.len(nodes), 1)])).map((i: any) => ({"from": py.at(nodes, i), "to": py.at(nodes, py.add(i, 1))}));
  return {"nodes": nodes, "edges": edges};
}
