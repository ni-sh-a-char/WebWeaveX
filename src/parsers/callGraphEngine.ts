/**
 * Converted from Python: core/parsers/call_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

const ast: any = py.astModule;
export function buildCallGraph(source: any, language: any): any {
  var lang: any = String(py.or2(language, () => ("text"))).toLowerCase();
  var src: any = py.or2(source, () => (""));
  var calls: any[] = [];
  if (py.eq(lang, "python")) {
    try {
      var tree: any = ast.parse(src);
      var fn_stack: any[] = [];
      /* nested class Visitor unsupported */ var Visitor: any;
      new Visitor().visit(tree);
    } catch (_e: any) {
    }
  }
  if ((!py.truthy(calls) && !py.eq(lang, "python"))) {
    var skip: any = new Set(["if", "for", "while", "switch", "return", "new", "typeof"]);
    var match: any;
    for (match of py.iter(py.reFinditer("([A-Za-z_][A-Za-z0-9_]*)\\s*\\(", src, ""))) {
      var name: any = match.group(1);
      if (!py.contains(skip, name)) {
        py.listAppend(calls, {"from": "<module>", "to": name});
      }
    }
  }
  var uniq: any = py.toSet(py.iter(calls).map((c: any) => [py.at(c, "from"), py.at(c, "to")]));
  var ordered: any = py.sorted(uniq, {key: ((x: any) => [py.at(x, 0), py.at(x, 1)]) as (item: any) => any});
  return {"calls": py.iter(ordered).map(([f, t]: any) => ({"from": f, "to": t}))};
}
