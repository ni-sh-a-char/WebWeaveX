/**
 * Converted from Python: core/documents/explanation_dependency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildExplanationChains } from "./explanationChainEngine.js";
import { structureCognition } from "../evidence/index.js";

export function reconstructExplanationDependencies(text: any): any {
  var chains: any = buildExplanationChains(text);
  var explains: any = py.get(py.get(chains, "reconciled", {}), "what_explains_what", []);
  var observed: any = {"chains_observed": py.len(explains)};
  var inferred: any = {"explanation_dependencies": explains};
  var reconciled: any = {"what_explains_what": explains};
  var out: any = structureCognition(observed, inferred, reconciled, null);
  py.setItem(out, "explanation_dependencies", explains);
  return out;
}
export { buildExplanationChains, structureCognition };
