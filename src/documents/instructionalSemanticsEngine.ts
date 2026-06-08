/**
 * Converted from Python: core/documents/instructional_semantics_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractInstructionalFlow } from "./instructionalFlowEngine.js";
import { assignSemanticRoles } from "./semanticRoleEngine.js";

export function analyzeInstructionalSemantics(text: any): any {
  var flow: any = extractInstructionalFlow(text);
  var roles: any = assignSemanticRoles(text);
  var ordering: any = py.enumerate(py.get(flow, "steps", [])).map(([i, s]: any) => ({"step": py.add(i, 1), "title": py.get(s, "title", "")}));
  return {"ordering": ordering, "prerequisites": py.get(flow, "prerequisites", []), "notices": py.iter(py.get(roles, "roles", [])).filter((r: any) => py.eq(py.get(r, "role"), "notice")).map((r: any) => r), "evidence": ["discourse:instructional_flow"], "deterministic_inputs": [`steps=${py.toStr(py.len(ordering))}`]};
}
export { assignSemanticRoles, extractInstructionalFlow };
