/**
 * Converted from Python: core/documents/tutorial_prerequisite_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { analyzeInstructionalSemantics } from "./instructionalSemanticsEngine.js";
import { reconstructTutorialDependencies } from "./tutorialDependencyEngine.js";

export function inferTutorialPrerequisites(text: any): any {
  var inst: any = analyzeInstructionalSemantics(text);
  var legacy: any = reconstructTutorialDependencies(text);
  var chain: any[] = [];
  var steps: any = py.get(inst, "ordering", []);
  var i: any;
  for (i = 1; i < py.len(steps); i++) {
    py.listAppend(chain, {"prerequisite": py.get(py.at(steps, py.sub(i, 1)), "title", ""), "requires": py.get(py.at(steps, i), "title", ""), "evidence": "discourse:instructional_order"});
  }
  return {"chain": chain, "prerequisites": py.get(inst, "prerequisites", []), "legacy_flow": py.get(legacy, "reconciled", {}), "deterministic_inputs": [`chain=${py.toStr(py.len(chain))}`]};
}
export { analyzeInstructionalSemantics, reconstructTutorialDependencies };
