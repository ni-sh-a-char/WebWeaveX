/**
 * Converted from Python: core/world_model/semantic_ownership_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { normalizeSymbols } from "./_normalize.js";

export function buildSemanticOwnershipGraph(repository_irs: any): any {
  var ownership: Record<string, any> = {};
  var ir: any;
  for (ir of py.iter(repository_irs)) {
    var path: any = py.get(ir, "path");
    var semantic_ast: any = py.get(ir, "semantic_ast", {});
    var symbol: any;
    for (symbol of py.iter(normalizeSymbols(semantic_ast))) {
      var name: any = py.get(symbol, "name");
      if (py.truthy(name)) {
        py.setItem(ownership, name, path);
      }
    }
  }
  return {"ownership": py.pyDict(py.sorted(py.items(ownership)))};
}
export { normalizeSymbols };
