/**
 * Converted from Python: core/evidence/recursive_consensus_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectRecursiveConsensus(reconciled_eq_inferred: any, depth: any, evidence_count: any): any {
  var inflated: any = py.and2(reconciled_eq_inferred, () => (py.and2((depth >= 2), () => ((evidence_count < 2)))));
  return {"consensus_inflated": inflated, "suppress": inflated, "plurality_pressure": {"level": (py.truthy(inflated) ? py.F(0.8) : py.F(0.0))}};
}
