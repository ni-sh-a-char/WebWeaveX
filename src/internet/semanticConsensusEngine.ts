/**
 * Converted from Python: core/internet/semantic_consensus_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function measureSemanticConsensus(claims: any): any {
  var texts: any = py.iter(py.or2(claims, () => ([]))).map((c: any) => String(py.strip(py.toStr(py.get(c, "text", py.get(c, "claim", ""))))).toLowerCase());
  var unique: any = py.toSet(py.iter(texts).filter((t: any) => py.truthy(t)).map((t: any) => t));
  var agreement: any = (py.truthy(texts) ? py.sub(py.F(1.0), py.div(py.len(unique), py.max([1, py.len(texts)]))) : py.F(0.0));
  return {"consensus": py.round(agreement, 3), "claim_count": py.len(texts), "unique_count": py.len(unique), "deterministic_inputs": [`consensus=${py.floatStr(py.round(agreement, 3))}`]};
}
