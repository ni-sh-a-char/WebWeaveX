/**
 * Converted from Python: core/ast/control_flow_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildControlFlowGraph(ast_ir: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var funcs: any = py.get(ast_ir, "functions", []);
  var fn: any;
  for (fn of py.iter(funcs)) {
    py.listAppend(nodes, {"id": py.at(fn, "name"), "type": "function"});
  }
  var i: any;
  for (i = 0; i < py.sub(py.len(funcs), 1); i++) {
    py.listAppend(edges, {"from": py.at(py.at(funcs, i), "name"), "to": py.at(py.at(funcs, py.add(i, 1)), "name"), "relation": "possible_flow"});
  }
  return {"nodes": nodes, "edges": edges, "bounded": true, "deterministic": true};
}
