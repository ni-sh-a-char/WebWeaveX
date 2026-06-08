/**
 * Converted from Python: core/documents/semantic_discourse_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildArgumentGraph } from "./argumentGraphEngine.js";
import { modelSemanticTransitions } from "./semanticTransitionEngine.js";

export function buildSemanticDiscourseGraph(text: any): any {
  var arg: any = buildArgumentGraph(text);
  var trans: any = modelSemanticTransitions(text);
  return {"nodes": py.get(arg, "nodes", []), "edges": py.add(py.get(arg, "edges", []), py.get(trans, "transitions", [])), "evidence": ["discourse:argument", "discourse:transition"]};
}
export { buildArgumentGraph, modelSemanticTransitions };
