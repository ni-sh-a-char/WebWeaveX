/**
 * Converted from Python: core/documents/tutorial_dependency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractTutorialFlow } from "./tutorialReasoningEngine.js";
import { structureCognition } from "../evidence/index.js";

export function reconstructTutorialDependencies(text: any): any {
  var flow: any = extractTutorialFlow(text);
  var requires: any = py.get(py.get(flow, "inferred", {}), "requires_prior", []);
  var steps: any = py.get(py.get(flow, "reconciled", {}), "steps", []);
  var observed: any = {"steps": steps};
  var inferred: any = {"tutorial_dependencies": requires, "prerequisite_edges": requires};
  var reconciled: any = {"tutorial_flow": py.get(flow, "reconciled", {}), "dependencies": requires};
  return structureCognition(observed, inferred, reconciled, null);
}
export { extractTutorialFlow, structureCognition };
