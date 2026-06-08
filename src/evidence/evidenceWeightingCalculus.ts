/**
 * Converted from Python: core/evidence/evidence_weighting_calculus.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function weightEvidenceCalculus(evidence: any, parser_backed: any = false): any {
  var items: any = py.sorted(py.toSet(py.iter(evidence).filter((e: any) => py.truthy(e)).map((e: any) => py.toStr(e))));
  var weights: Record<string, any> = {};
  var e: any;
  for (e of py.iter(items)) {
    if (py.truthy(py.startswith(e, "parser:"))) {
      py.setItem(weights, e, py.F(1.0));
    } else if (py.truthy(parser_backed)) {
      py.setItem(weights, e, py.F(0.85));
    } else {
      py.setItem(weights, e, py.F(0.6));
    }
  }
  var total: any = py.round(py.sum(py.values(weights)), 3);
  return {"weights": weights, "total": total, "parser_backed": parser_backed, "deterministic_inputs": [`items=${py.toStr(py.len(items))}`, `total=${py.toStr(total)}`]};
}
