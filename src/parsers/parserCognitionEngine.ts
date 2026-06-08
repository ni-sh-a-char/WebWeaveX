/**
 * Converted from Python: core/parsers/parser_cognition_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildLineage } from "../evidence/lineageEngine.js";

export function buildParserCognitionEvidence(parsed: any): any {
  if (!((parsed !== null && typeof parsed === "object" && !Array.isArray(parsed) && !(parsed instanceof Set) && !(parsed instanceof Map)))) {
    return {"parser_evidence": [], "semantic_evidence": [], "graph_evidence": [], "lineage": buildLineage([])};
  }
  var flags: any = py.get(parsed, "parser_evidence", py.get(parsed, "evidence", {}));
  if (!((flags !== null && typeof flags === "object" && !Array.isArray(flags) && !(flags instanceof Set) && !(flags instanceof Map)))) {
    flags = {};
  }
  var sym: any = (((py.get(parsed, "symbols") !== null && typeof py.get(parsed, "symbols") === "object" && !Array.isArray(py.get(parsed, "symbols")) && !(py.get(parsed, "symbols") instanceof Set) && !(py.get(parsed, "symbols") instanceof Map))) ? py.get(parsed, "symbols", {}) : {});
  var parser_evidence: any = py.iter(py.sorted(py.items(flags))).filter(([k, v]: any) => py.truthy(v)).map(([k, v]: any) => `parser:${py.toStr(k)}`);
  var name: any;
  for (name of py.iter(py.or2(py.get(sym, "classes", []), () => ([])))) {
    py.listAppend(parser_evidence, `symbol:class:${py.toStr(name)}`);
  }
  for (name of py.iter(py.or2(py.get(sym, "functions", []), () => ([])))) {
    py.listAppend(parser_evidence, `symbol:function:${py.toStr(name)}`);
  }
  var semantic_evidence: any[] = [];
  var deps: any = py.get(py.or2(py.get(parsed, "dependencies", {}), () => ({})), "dependencies", []);
  var d: any;
  for (d of py.iter(py.or2(deps, () => ([])))) {
    py.listAppend(semantic_evidence, `dependency:${py.toStr(d)}`);
  }
  var graph: any = py.or2(py.get(parsed, "semantic_graph", {}), () => ({}));
  var graph_evidence: any = py.iter(py.slice(py.or2(py.get(graph, "edges", []), () => ([])), null, 50)).filter((e: any) => ((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map)))).map((e: any) => `graph:edge:${py.toStr(py.get(e, "from"))}->${py.toStr(py.get(e, "to"))}`);
  var lineage: any = buildLineage([{"stage": "parser_cognition", "inputs": [], "outputs": py.sorted(py.slice(parser_evidence, null, 20))}]);
  return {"parser_evidence": py.sorted(py.toSet(parser_evidence)), "semantic_evidence": py.sorted(py.toSet(semantic_evidence)), "graph_evidence": py.sorted(py.toSet(graph_evidence)), "lineage": lineage};
}
export { buildLineage };
