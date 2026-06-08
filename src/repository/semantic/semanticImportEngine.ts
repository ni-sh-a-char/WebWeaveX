/**
 * Converted from Python: core/repository/semantic/semantic_import_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function buildSemanticImportGraph(ast_data: any, source: any = "module"): any {
  var imports: any = py.sorted(py.toSet(py.get(py.or2(ast_data, () => ({})), "imports", [])));
  var nodes: any = py.sorted(py.toSet(py.add([source], imports)));
  var edges: any = py.iter(imports).map((imp: any) => ({"from": source, "to": imp}));
  return {"nodes": nodes, "edges": edges};
}
