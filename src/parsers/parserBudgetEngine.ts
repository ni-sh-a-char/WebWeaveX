/**
 * Converted from Python: core/parsers/parser_budget_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export class ParserBudget {
  declare max_bytes: any;
  declare max_nodes: any;
  declare max_depth: any;
  constructor(max_bytes: any = 5000000, max_nodes: any = 100000, max_depth: any = 256) {
    this.max_bytes = max_bytes;
    this.max_nodes = max_nodes;
    this.max_depth = max_depth;
  }
}
export function enforceBudget(source: any, budget: any = null): any {
  var b: any = py.or2(budget, () => (new ParserBudget()));
  var raw: any = py.encode(py.or2(source, () => ("")), "utf-8");
  if ((py.len(raw) <= b.max_bytes)) {
    return py.or2(source, () => (""));
  }
  return py.decode(py.slice(raw, null, b.max_bytes), "utf-8");
}
