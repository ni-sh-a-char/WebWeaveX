/**
 * Converted from Python: core/repository/semantic/semantic_call_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

const ast: any = py.astModule;
export function buildSemanticCallGraph(text: any): any {
  var source: any = py.or2(text, () => (""));
  var calls: any[] = [];
  try {
    var tree: any = ast.parse(source);
    var func_stack: any[] = [];
    /* nested class Visitor unsupported */ var Visitor: any;
    new Visitor().visit(tree);
  } catch (_e: any) {
    var m: any;
    for (m of py.iter(py.reFinditer("([A-Za-z_][A-Za-z0-9_]*)\\s*\\(", source, ""))) {
      var name: any = m.group(1);
      if (!py.contains(new Set(["if", "for", "while", "switch", "return"]), name)) {
        py.listAppend(calls, {"from": "<module>", "to": name});
      }
    }
  }
  var dedup: any = py.sorted(py.toSet(py.iter(calls).map((c: any) => [py.at(c, "from"), py.at(c, "to")])));
  return {"calls": py.iter(dedup).map(([f, t]: any) => ({"from": f, "to": t}))};
}
