/**
 * Converted from Python: core/world_model/semantic_refactor_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { normalizeSymbols } from "./_normalize.js";

export function suggestSemanticRefactor(repository_ir: any): any {
  var symbols: any = normalizeSymbols(py.get(repository_ir, "semantic_ast", {}));
  var duplicated: Record<string, any> = {};
  var symbol: any;
  for (symbol of py.iter(symbols)) {
    var name: any = py.get(symbol, "name");
    py.setItem(duplicated, name, py.add(py.get(duplicated, name, 0), 1));
  }
  var repeated: any = py.sorted(py.items(duplicated).filter(([key, value]: any) => (value > 1)).map(([key, value]: any) => key));
  return {"duplicate_symbols": repeated, "refactor_required": py.truthy(repeated)};
}
export { normalizeSymbols };
