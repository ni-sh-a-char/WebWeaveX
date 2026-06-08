/**
 * Converted from Python: core/evidence/recursive_entropy_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelRecursiveEntropy(ambiguities: any, uncertainties: any, contradicted: any, depth: any): any {
  var pairs: any = (((contradicted !== null && typeof contradicted === "object" && !Array.isArray(contradicted) && !(contradicted instanceof Set) && !(contradicted instanceof Map))) ? py.get(contradicted, "pairs", []) : []);
  var base: any = py.add(py.add(py.mul(py.len(ambiguities), py.F(0.1)), py.mul(py.len(uncertainties), py.F(0.08))), py.mul(py.len(pairs), py.F(0.15)));
  var entropy: any = py.round(py.min([py.F(1.0), py.add(base, py.mul(depth, py.F(0.05)))]), 3);
  return {"entropy": entropy, "depth": depth, "preserved": true, "suppress_recursive_stabilization": (entropy >= py.F(0.15)), "suppress_recursive_closure": (entropy >= py.F(0.2))};
}
