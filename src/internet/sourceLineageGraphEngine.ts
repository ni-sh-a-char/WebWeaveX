/**
 * Converted from Python: core/internet/source_lineage_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildSemanticProvenance } from "./semanticProvenanceEngine.js";

export function buildSourceLineageGraph(text: any, url: any = ""): any {
  var prov: any = buildSemanticProvenance(text, url);
  var citations: any = ((Array.isArray(py.get(prov, "citations"))) ? py.get(prov, "citations", []) : []);
  var nodes: any = py.add([url], py.iter(py.slice(citations, null, 30)).map((c: any) => py.slice(py.toStr(c), null, 40)));
  var edges: any = py.range(py.max([0, py.sub(py.len(nodes), 1)])).map((i: any) => ({"from": py.at(nodes, i), "to": py.at(nodes, py.add(i, 1)), "relation": "cites"}));
  return {"nodes": nodes, "edges": edges, "lineage": py.get(prov, "lineage", {})};
}
export { buildSemanticProvenance };
