/**
 * Converted from Python: core/reasoning/semantic_proof_runtime.py
 * @generated — WebWeaveX python→javascript library port
 */

import { proveSemanticClaim } from "../evidence/semanticProofEngine.js";

export function proveSemanticClaimRuntime(claim: any, evidence: any): any {
  return proveSemanticClaim(claim, evidence);
}
export { proveSemanticClaim };
