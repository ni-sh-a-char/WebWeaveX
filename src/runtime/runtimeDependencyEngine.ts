/**
 * Converted from Python: core/runtime/runtime_dependency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export let MAX_DEPS: any = 500;
export function resolveRuntimeDependencies(nodes: any, edges: any, parser_evidence: any): any {
  var adj: Record<string, any> = {};
  var e: any;
  for (e of py.iter(py.slice(edges, null, MAX_DEPS))) {
    if (!((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map)))) {
      continue;
    }
    const _d1 = py.iter([py.get(e, "from"), py.get(e, "to")]) as any[];
    var src: any = _d1[0];
    var dst: any = _d1[1];
    if ((py.truthy(src) && py.truthy(dst))) {
      py.listAppend(py.setdefault(adj, py.toStr(src), []), py.toStr(dst));
    }
  }
  var k: any;
  for (k of py.iter(adj)) {
    py.setItem(adj, k, py.sorted(py.toSet(py.at(adj, k))));
  }
  return {"adjacency": adj, "nodes": py.slice(py.sorted(py.toSet(nodes)), null, MAX_DEPS), "evidence": py.sorted(py.toSet(parser_evidence)), "grounded": py.truthy(parser_evidence), "deterministic": true};
}
