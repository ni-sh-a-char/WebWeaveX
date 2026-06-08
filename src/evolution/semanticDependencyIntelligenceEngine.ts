/**
 * Converted from Python: core/evolution/semantic_dependency_intelligence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_DEPENDENCIES: any = 10000;
export function analyzeSemanticDependencies(repository_ir: any): any {
  var edges: any = [...py.iter(py.get(repository_ir, "edges", []))];
  var dependency_map: Record<string, any> = {};
  var edge: any;
  for (edge of py.iter(py.slice(edges, null, MAX_DEPENDENCIES))) {
    var source: any = py.toStr(py.get(edge, "from"));
    var target: any = py.toStr(py.get(edge, "to"));
    py.listAppend(py.setdefault(dependency_map, source, []), target);
  }
  for (source of py.iter(dependency_map)) {
    py.setItem(dependency_map, source, py.sorted(py.at(dependency_map, source)));
  }
  return {"dependency_map": py.pyDict(py.sorted(py.items(dependency_map))), "bounded": true};
}
