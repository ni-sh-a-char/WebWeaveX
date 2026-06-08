/**
 * Converted from Python: core/documents/semantic_support_chain_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reconstructSemanticCausality } from "./semanticCausalityEngine.js";
import { structureCognition } from "../evidence/index.js";

export function reconstructSupportChains(text: any): any {
  var causality: any = reconstructSemanticCausality(text);
  var chains: any = py.get(py.get(causality, "reconciled", {}), "what_explains_what", []);
  var support: any = py.iter(chains).map((c: any) => ({"chain": [py.get(c, "from"), py.get(c, "to")], "evidence": py.get(c, "evidence", [])}));
  var observed: any = {"chain_count": py.len(support)};
  var inferred: any = {"support_chains": support};
  var reconciled: any = {"semantic_support_chains": support};
  var out: any = structureCognition(observed, inferred, reconciled, null);
  py.setItem(out, "semantic_support_chains", support);
  return out;
}
export { reconstructSemanticCausality, structureCognition };
