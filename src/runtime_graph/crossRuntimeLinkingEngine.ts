/**
 * Converted from Python: core/runtime_graph/cross_runtime_linking_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function linkRuntimeEntities(graph: any): any {
  var nodes: any = [...py.iter(py.or2(py.get(graph, "nodes", []), () => ([])))];
  var links: any[] = [];
  var seen: Record<string, any> = {};
  var node: any;
  for (node of py.iter(nodes)) {
    var name: any = String(py.strip(py.toStr(py.get(node, "name", "")))).toLowerCase();
    if (!py.truthy(name)) {
      continue;
    }
    if (!py.contains(seen, name)) {
      py.setItem(seen, name, []);
    }
    py.listAppend(py.at(seen, name), node);
  }
  var grouped: any;
  for ([name, grouped] of py.iter(py.sorted(py.items(seen)))) {
    if ((py.len(grouped) < 2)) {
      continue;
    }
    var ids: any = py.sorted(py.iter(grouped).map((x: any) => py.toStr(py.get(x, "id", ""))));
    var i: any;
    for (i = 0; i < py.sub(py.len(ids), 1); i++) {
      py.listAppend(links, {"from": py.at(ids, i), "to": py.at(ids, py.add(i, 1)), "relation": "same_entity"});
    }
  }
  return {"entity_links": py.slice(links, null, 100000), "bounded": true};
}
