/**
 * Converted from Python: core/knowledge/reconstruction/repository_knowledge_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function buildRepositoryKnowledge(repo: any): any {
  var nodes: any = py.sorted(py.toSet(py.add(py.add(py.get(repo, "symbols", []), py.get(repo, "dependencies", [])), py.get(repo, "frameworks", []))));
  var edges: any = py.range(py.max([0, py.sub(py.len(nodes), 1)])).map((i: any) => ({"from": py.at(nodes, i), "to": py.at(nodes, py.add(i, 1))}));
  return {"nodes": nodes, "edges": edges};
}
