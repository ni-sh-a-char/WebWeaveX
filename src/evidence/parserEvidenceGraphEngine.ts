/**
 * Converted from Python: core/evidence/parser_evidence_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildEvidenceGraph } from "./evidenceGraphEngine.js";

export function buildParserEvidenceGraph(parsed: any): any {
  var claims: any[] = [];
  if (!((parsed !== null && typeof parsed === "object" && !Array.isArray(parsed) && !(parsed instanceof Set) && !(parsed instanceof Map)))) {
    return {"nodes": [], "edges": []};
  }
  var sym: any = (((py.get(parsed, "symbols") !== null && typeof py.get(parsed, "symbols") === "object" && !Array.isArray(py.get(parsed, "symbols")) && !(py.get(parsed, "symbols") instanceof Set) && !(py.get(parsed, "symbols") instanceof Map))) ? py.get(parsed, "symbols", {}) : {});
  var name: any;
  for (name of py.iter(py.or2(py.get(sym, "classes", []), () => ([])))) {
    py.listAppend(claims, {"id": `class:${py.toStr(name)}`, "sources": ["parser:symbols"]});
  }
  for (name of py.iter(py.or2(py.get(sym, "functions", []), () => ([])))) {
    py.listAppend(claims, {"id": `func:${py.toStr(name)}`, "sources": ["parser:symbols"]});
  }
  var dep: any;
  for (dep of py.iter((((py.get(parsed, "dependencies") !== null && typeof py.get(parsed, "dependencies") === "object" && !Array.isArray(py.get(parsed, "dependencies")) && !(py.get(parsed, "dependencies") instanceof Set) && !(py.get(parsed, "dependencies") instanceof Map))) ? py.get(py.or2(py.get(parsed, "dependencies", {}), () => ({})), "dependencies", []) : []))) {
    py.listAppend(claims, {"id": `dep:${py.toStr(dep)}`, "sources": ["parser:dependencies"]});
  }
  return buildEvidenceGraph(claims);
}
export { buildEvidenceGraph };
