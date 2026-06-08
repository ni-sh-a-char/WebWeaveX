/**
 * Converted from Python: core/repository/semantic/semantic_symbol_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function resolveSemanticSymbols(ast_data: any): any {
  var data: any = py.or2(ast_data, () => ({}));
  var resolved: any = {"classes": py.sorted(py.toSet(py.get(data, "classes", []))), "interfaces": py.sorted(py.toSet(py.get(data, "interfaces", []))), "traits": py.sorted(py.toSet(py.get(data, "traits", []))), "functions": py.sorted(py.toSet(py.get(data, "functions", []))), "methods": py.sorted(py.toSet(py.get(data, "methods", []))), "imports": py.sorted(py.toSet(py.get(data, "imports", []))), "exports": py.sorted(py.toSet(py.get(data, "exports", []))), "symbols": py.sorted(py.toSet(py.get(data, "symbols", [])))};
  py.setItem(resolved, "services", py.iter(py.at(resolved, "symbols")).filter((s: any) => py.truthy(py.endswith(String(s).toLowerCase(), ["service", "controller", "handler"]))).map((s: any) => s));
  return resolved;
}
