/**
 * Converted from Python: core/documents/explanation_proof_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function proveExplanationChain(sections: any): any {
  var ordered: any = py.sorted(sections, {key: ((s: any) => py.toInt(py.get(s, "order", 0))) as (item: any) => any});
  var gaps: any = py.iter(ordered).filter((s: any) => !py.truthy(py.get(s, "content"))).map((s: any) => py.get(s, "id"));
  return {"complete": py.eq(py.len(gaps), 0), "gaps": gaps, "section_count": py.len(ordered), "deterministic": true};
}
