/**
 * Converted from Python: core/documents/explanation_structure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { modelDiscourseCausality } from "./discourseCausalityEngine.js";
import { analyzeArgumentSemantics } from "./argumentSemanticsEngine.js";

export function buildExplanationStructure(text: any): any {
  var causal: any = modelDiscourseCausality(text);
  var args: any = analyzeArgumentSemantics(text);
  return {"explanation_causal": py.get(causal, "causal", []), "argument": args, "layers": ["lexical", "syntactic", "semantic", "rhetorical", "argumentative"]};
}
export { analyzeArgumentSemantics, modelDiscourseCausality };
