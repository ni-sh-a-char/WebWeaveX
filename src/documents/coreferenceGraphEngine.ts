/**
 * Converted from Python: core/documents/coreference_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { resolveCoreferences } from "./coreferenceResolutionEngine.js";
import { parseRhetoricalStructure } from "./rhetoricalParserEngine.js";

export function buildCoreferenceGraph(text: any): any {
  var coref: any = resolveCoreferences(text);
  var rhet: any = parseRhetoricalStructure(text);
  var headings: any = py.iter(py.get(rhet, "units", [])).filter((u: any) => py.eq(py.get(u, "type"), "heading")).map((u: any) => py.get(u, "title", ""));
  var nodes: any = py.iter(headings).filter((h: any) => py.truthy(h)).map((h: any) => ({"id": h, "kind": "entity"}));
  var edges: any = py.iter(py.get(coref, "chains", [])).filter((c: any) => py.truthy(py.get(c, "antecedent"))).map((c: any) => ({"from": py.get(c, "pronoun", ""), "to": py.get(c, "antecedent", ""), "evidence": ["discourse:coref"]}));
  return {"nodes": nodes, "edges": py.slice(edges, null, 100), "chains": py.get(coref, "chains", [])};
}
export { parseRhetoricalStructure, resolveCoreferences };
