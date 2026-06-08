/**
 * Converted from Python: core/evidence/semantic_refusal_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function refuseUnsupportedConclusions(noninferable_regions: any, suppressed_speculation: any): any {
  var refusals: any[] = [];
  var region: any;
  for (region of py.iter(noninferable_regions)) {
    py.listAppend(refusals, {"target": region, "message": "cannot_determine"});
  }
  var spec: any;
  for (spec of py.iter(suppressed_speculation)) {
    py.listAppend(refusals, {"target": py.get(spec, "reason", "speculation"), "message": "cannot_determine"});
  }
  return {"refusals": refusals, "terminated_inferences": py.iter(refusals).map((r: any) => py.at(r, "target")), "termination_reasons": py.sorted(py.toSet(py.iter(refusals).map((r: any) => py.at(r, "message")))), "unsupported_regions": noninferable_regions};
}
