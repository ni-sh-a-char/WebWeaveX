/**
 * Converted from Python: core/documents/semantic_explanation_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reconstructSemanticCausality } from "./semanticCausalityEngine.js";
import { structureCognition } from "../evidence/index.js";

export function buildExplanationGraph(text: any): any {
  var causality: any = reconstructSemanticCausality(text);
  var edges: any = py.get(py.get(causality, "reconciled", {}), "what_explains_what", []);
  var nodes: any = py.sorted(py.bitor(py.toSet(py.iter(edges).map((e: any) => py.get(e, "from"))), py.toSet(py.iter(edges).map((e: any) => py.get(e, "to")))));
  var graph: any = {"nodes": py.iter(nodes).filter((n: any) => py.truthy(n)).map((n: any) => ({"id": n, "kind": "concept", "metadata": {}})), "edges": py.iter(edges).map((e: any) => ({"from": py.at(e, "from"), "to": py.at(e, "to"), "metadata": {"relation": "explains"}})), "max_edges": 5000};
  var observed: any = {"node_count": py.len(nodes)};
  var inferred: any = {"explanation_graph": graph};
  var reconciled: any = graph;
  return structureCognition(observed, inferred, reconciled, null);
}
export { reconstructSemanticCausality, structureCognition };
