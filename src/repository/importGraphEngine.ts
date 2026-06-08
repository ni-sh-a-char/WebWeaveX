/**
 * Converted from Python: core/repository/import_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildImportGraph(text: any): any {
  var src: any = py.or2(text, () => (""));
  var py_: any = py.reFindall("^\\s*(?:import|from)\\s+([A-Za-z0-9_.]+)", src, "m");
  var js: any = py.reFindall("import\\s+.*?from\\s+['\"]([^'\"]+)['\"]", src, "");
  var dart: any = py.reFindall("import\\s+['\"]([^'\"]+)['\"]", src, "");
  var java: any = py.reFindall("^\\s*import\\s+([A-Za-z0-9_.]+);", src, "m");
  var nodes: any = py.sorted(py.toSet(py.add(py.add(py.add(py_, js), dart), java)));
  var edges: any = py.range(py.max([0, py.sub(py.len(nodes), 1)])).map((i: any) => ({"from": py.at(nodes, i), "to": py.at(nodes, py.add(i, 1))}));
  return {"nodes": nodes, "edges": edges};
}
