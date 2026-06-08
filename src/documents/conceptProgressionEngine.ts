/**
 * Converted from Python: core/documents/concept_progression_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { modelSemanticTransitions } from "./semanticTransitionEngine.js";

export function modelConceptProgression(text: any): any {
  var trans: any = modelSemanticTransitions(text);
  var progression: any[] = [];
  var i: any;
  var t: any;
  for ([i, t] of py.enumerate(py.get(trans, "transitions", []))) {
    py.listAppend(progression, {"index": i, "from": py.get(t, "from"), "to": py.get(t, "to"), "introduces": py.get(t, "to")});
  }
  return {"progression": progression, "concept_count": py.len(progression), "deterministic_inputs": [`concepts=${py.toStr(py.len(progression))}`]};
}
export { modelSemanticTransitions };
