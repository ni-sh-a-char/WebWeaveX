/**
 * Converted from Python: core/evidence/reality_constraint_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { modelEvidenceBoundaries } from "./evidenceBoundaryEngine.js";
import { modelOntologyBoundaries } from "./ontologyBoundaryEngine.js";
import { modelTopologyBoundaries } from "./topologyBoundaryEngine.js";

export function applyRealityConstraints(evidence: any, parser_grounded: any, drift_pressure: any): any {
  var ev_bound: any = modelEvidenceBoundaries(evidence);
  return {"evidence_bounded": py.at(ev_bound, "bounded"), "semantic_growth_allowed": py.and2(py.at(ev_bound, "bounded"), () => ((drift_pressure < py.F(0.3)))), "ontology_expansion_allowed": py.at(modelOntologyBoundaries(evidence), "expansion_allowed"), "topology_propagation_allowed": py.at(modelTopologyBoundaries(evidence, parser_grounded), "propagation_allowed"), "speculative_coherence_allowed": false, "continuity_allowed": py.at(ev_bound, "bounded")};
}
export { modelEvidenceBoundaries, modelOntologyBoundaries, modelTopologyBoundaries };
