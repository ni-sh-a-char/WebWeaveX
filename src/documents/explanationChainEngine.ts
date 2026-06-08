/**
 * Converted from Python: core/documents/explanation_chain_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reconstructSemanticSections } from "./semanticSectionReconstructionEngine.js";
import { structureCognition } from "../evidence/index.js";

export function buildExplanationChains(text: any): any {
  var sections: any = reconstructSemanticSections(text);
  var chains: any = py.get(py.get(py.get(sections, "reconciled", {}), "structure", {}), "explains", []);
  var observed: any = {"section_structure": py.get(sections, "observed", {})};
  var inferred: any = {"chains": chains};
  var reconciled: any = {"what_explains_what": chains};
  return structureCognition(observed, inferred, reconciled, null);
}
export { reconstructSemanticSections, structureCognition };
