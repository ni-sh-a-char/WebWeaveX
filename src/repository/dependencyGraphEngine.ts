/**
 * Converted from Python: core/repository/dependency_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildDependencyGraph(text: any): any {
  var src: any = py.or2(text, () => (""));
  var lines: any = py.iter(py.splitlines(src)).filter((ln: any) => py.truthy(py.strip(ln))).map((ln: any) => py.strip(ln));
  var req_nodes: any[] = [];
  var ln: any;
  for (ln of py.iter(lines)) {
    var m: any = py.reMatch("^([A-Za-z0-9_.\\-]+)\\s*(?:==|>=|~=|<=|>|<)", ln, "");
    if (py.truthy(m)) {
      py.listAppend(req_nodes, m.group(1));
    }
  }
  var pkg_nodes: any = py.reFindall("\"([@A-Za-z0-9_.\\-/]+)\"\\s*:\\s*\"[~^<>=0-9.*]+\"", src, "");
  var nodes: any = py.sorted(py.toSet(py.add(req_nodes, pkg_nodes)));
  var edges: any = py.range(py.max([0, py.sub(py.len(nodes), 1)])).map((i: any) => ({"from": py.at(nodes, i), "to": py.at(nodes, py.add(i, 1))}));
  return {"nodes": nodes, "edges": edges};
}
