/**
 * Converted from Python: core/typed_ir/typed_repository_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { compileSemanticAstIr } from "../ast/index.js";
import { SemanticNode, SemanticEdge } from "./schemaTypes.js";

export function compileTypedRepositoryIr(source: any): any {
  var ast_ir: any = compileSemanticAstIr(source);
  var nodes: any[] = [];
  var edges: any[] = [];
  var fn: any;
  for (fn of py.iter(py.at(py.at(ast_ir, "ast"), "functions"))) {
    py.listAppend(nodes, new SemanticNode(py.at(fn, "name"), "function"));
  }
  var funcs: any = py.at(py.at(ast_ir, "ast"), "functions");
  var i: any;
  for (i = 0; i < py.sub(py.len(funcs), 1); i++) {
    py.listAppend(edges, new SemanticEdge(py.at(py.at(funcs, i), "name"), py.at(py.at(funcs, py.add(i, 1)), "name"), "execution_flow", ["ast_order"]));
  }
  return {"nodes": nodes, "edges": edges, "typed": true, "deterministic": true};
}
export { SemanticEdge, SemanticNode, compileSemanticAstIr };
