/**
 * Converted from Python: core/documents/document_dependency_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractInstructionalFlow } from "./instructionalFlowEngine.js";
import { modelConceptTransitions } from "./conceptTransitionEngine.js";

export function buildDocumentDependencyGraph(text: any): any {
  var flow: any = extractInstructionalFlow(text);
  var trans: any = modelConceptTransitions(text);
  var nodes: any = py.enumerate(py.at(flow, "steps")).map(([i, s]: any) => ({"id": py.get(s, "title", `step${py.toStr(i)}`), "kind": "step"}));
  var edges: any = py.get(trans, "transitions", []);
  return {"nodes": nodes, "edges": edges, "prerequisites": py.get(flow, "prerequisites", [])};
}
export { extractInstructionalFlow, modelConceptTransitions };
