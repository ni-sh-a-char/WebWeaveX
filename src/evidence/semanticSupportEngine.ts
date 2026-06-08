/**
 * Converted from Python: core/evidence/semantic_support_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildSupport(evidence: any, extra: any = null): any {
  var items: any = py.sorted(py.toSet(py.iter(py.add(py.or2(evidence, () => ([])), py.or2(extra, () => ([])))).filter((e: any) => py.truthy(e)).map((e: any) => py.toStr(e))));
  return {"supporting_evidence": items, "support_count": py.len(items), "support_strength": py.round(py.min([py.F(1.0), py.add(py.F(0.15), py.mul(py.len(items), py.F(0.1)))]), 3)};
}
