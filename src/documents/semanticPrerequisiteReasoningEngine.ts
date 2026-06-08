/**
 * Converted from Python: core/documents/semantic_prerequisite_reasoning_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reconstructPrerequisites } from "./semanticPrerequisiteEngine.js";
import { reconstructTutorialDependencies } from "./tutorialDependencyEngine.js";
import { structureCognition } from "../evidence/index.js";

export function reasonPrerequisites(text: any): any {
  var tutorial: any = reconstructTutorialDependencies(text);
  var prereqs: any = reconstructPrerequisites(text);
  var observed: any = {"tutorial_steps": py.get(py.get(tutorial, "reconciled", {}), "tutorial_flow", {})};
  var inferred: any = {"tutorial_prerequisites": py.get(tutorial, "inferred", {}), "concept_prerequisites": py.get(prereqs, "reconciled", {})};
  var reconciled: any = {"what_conceptually_precedes_what": py.get(py.get(prereqs, "reconciled", {}), "concept_prerequisites", []), "tutorial_dependencies": py.get(tutorial, "reconciled", {})};
  return structureCognition(observed, inferred, reconciled, null);
}
export { reconstructPrerequisites, reconstructTutorialDependencies, structureCognition };
