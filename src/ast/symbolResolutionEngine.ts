/**
 * Converted from Python: core/ast/symbol_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function resolveSymbols(ast_ir: any): any {
  var symbols: any[] = [];
  var fn: any;
  for (fn of py.iter(py.get(ast_ir, "functions", []))) {
    py.listAppend(symbols, {"symbol": py.at(fn, "name"), "kind": "function", "args": py.get(fn, "args", [])});
  }
  var cls: any;
  for (cls of py.iter(py.get(ast_ir, "classes", []))) {
    py.listAppend(symbols, {"symbol": py.at(cls, "name"), "kind": "class", "bases": py.get(cls, "bases", [])});
  }
  return {"symbols": py.sorted(symbols, {key: ((x: any) => py.at(x, "symbol")) as (item: any) => any}), "symbol_count": py.len(symbols), "grounded": true};
}
