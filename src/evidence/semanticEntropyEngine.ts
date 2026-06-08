/**
 * Converted from Python: core/evidence/semantic_entropy_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelSemanticEntropy(ambiguities: any, uncertainties: any, contradicted: any): any {
  var pairs: any = (((contradicted !== null && typeof contradicted === "object" && !Array.isArray(contradicted) && !(contradicted instanceof Set) && !(contradicted instanceof Map))) ? py.get(contradicted, "pairs", []) : []);
  var entropy: any = py.round(py.min([py.F(1.0), py.add(py.add(py.mul(py.len(ambiguities), py.F(0.1)), py.mul(py.len(uncertainties), py.F(0.08))), py.mul(py.len(pairs), py.F(0.15)))]), 3);
  return {"entropy": entropy, "visible": (entropy > 0), "suppress_stabilization": (entropy >= py.F(0.2)), "suppress_coherence": (entropy >= py.F(0.15)), "preserved": true};
}
