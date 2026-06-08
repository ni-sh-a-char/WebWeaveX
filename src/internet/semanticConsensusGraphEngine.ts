/**
 * Converted from Python: core/internet/semantic_consensus_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildEvidenceConsensus } from "./evidenceConsensusEngine.js";

export function buildSemanticConsensusGraph(sources: any, claims: any): any {
  var consensus: any = buildEvidenceConsensus(sources, claims);
  return {"nodes": py.iter(py.or2(sources, () => ([]))).map((s: any) => py.get(s, "url", py.get(s, "id", ""))), "consensus": consensus, "strength": py.get(consensus, "strength", 0), "evidence": py.get(consensus, "deterministic_inputs", [])};
}
export { buildEvidenceConsensus };
