/**
 * Converted from Python: core/parsers/import_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function resolveImports(symbols: any, source_id: any = "module"): any {
  var imports: any = py.sorted(py.toSet(py.get(py.or2(symbols, () => ({})), "imports", [])));
  var exports: any = py.sorted(py.toSet(py.get(py.or2(symbols, () => ({})), "exports", [])));
  var nodes: any = py.sorted(new Set([source_id, ...py.iter(imports), ...py.iter(exports)]));
  var edges: any = py.iter(imports).map((imp: any) => ({"from": source_id, "to": imp}));
  return {"nodes": nodes, "edges": edges, "exports": exports};
}
