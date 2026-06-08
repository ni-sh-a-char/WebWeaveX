/**
 * Converted from Python: core/documents/tutorial_reasoning_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractSections } from "./sectionEngine.js";
import { structureCognition } from "../evidence/index.js";

export function extractTutorialFlow(text: any): any {
  var hierarchy: any = py.get(extractSections(py.or2(text, () => (""))), "hierarchy", []);
  var steps: any = py.iter(hierarchy).filter((h: any) => py.truthy(py.get(h, "title"))).map((h: any) => py.get(h, "title", ""));
  var evidence_kind: any = "section_hierarchy";
  if (!py.truthy(steps)) {
    steps = py.sorted(py.toSet(py.reFindall("^\\s*\\d+\\.\\s+(.+)$", py.or2(text, () => ("")), "m")));
    evidence_kind = "numbered_list_fallback";
  }
  var observed: any = {"steps": steps};
  var inferred: any = {"requires_prior": py.range(1, py.len(steps)).filter((i: any) => (py.truthy(py.at(steps, i)) && py.truthy(py.at(steps, py.sub(i, 1))))).map((i: any) => ({"step": py.at(steps, i), "requires": py.at(steps, py.sub(i, 1))}))};
  var reconciled: any = {"steps": steps, "flow_edges": py.range(py.max([0, py.sub(py.len(steps), 1)])).map((i: any) => ({"from": py.at(steps, i), "to": py.at(steps, py.add(i, 1))}))};
  var result: any = structureCognition(observed, inferred, reconciled, null);
  py.setItem(result, "confidence_basis", {...(py.get(result, "confidence_basis", {})), "flow_evidence": evidence_kind});
  return result;
}
export { extractSections, structureCognition };
