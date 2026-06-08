/**
 * Converted from Python: core/documents/recursive/reference_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";
import { extractReferences } from "../referenceEngine.js";

export function buildReferenceGraph(text: any): any {
  var refs: any = extractReferences(text);
  var nodes: any = py.sorted(py.toSet(py.add(py.add(["document"], py.get(refs, "external_links", [])), py.get(refs, "internal_links", []))));
  var edges: any = py.iter(nodes).filter((n: any) => !py.eq(n, "document")).map((n: any) => ({"from": "document", "to": n}));
  edges = py.sorted(edges, {key: ((x: any) => [py.at(x, "from"), py.at(x, "to")]) as (item: any) => any});
  return {"nodes": nodes, "edges": edges};
}
export { extractReferences };
