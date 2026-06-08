/**
 * Converted from Python: core/internet/evidence_consensus_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { corroborateSources } from "./sourceCorroborationEngine.js";
import { measureSemanticConsensus } from "./semanticConsensusEngine.js";

export function buildEvidenceConsensus(sources: any, claims: any): any {
  var corr: any = corroborateSources(sources);
  var consensus: any = measureSemanticConsensus(claims);
  var strength: any = py.round(py.min([py.F(1.0), py.add(py.mul(py.get(corr, "corroboration_count", 0), py.F(0.2)), py.mul(py.get(consensus, "consensus", 0), py.F(0.8)))]), 3);
  return {"corroboration": corr, "consensus": consensus, "strength": strength, "deterministic_inputs": [`strength=${py.floatStr(strength)}`]};
}
export { corroborateSources, measureSemanticConsensus };
