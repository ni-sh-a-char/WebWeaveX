/**
 * Converted from Python: core/documents/semantic_intent_flow_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { assignSemanticRoles } from "./semanticRoleEngine.js";

export function modelIntentFlow(text: any): any {
  var roles: any = assignSemanticRoles(text);
  var chain: any[] = [];
  var r: any;
  for (r of py.iter(py.get(roles, "roles", []))) {
    py.listAppend(chain, {"line": py.get(r, "line"), "intent": py.get(r, "role", "span")});
  }
  return {"intent_chain": chain, "evidence": ["discourse:semantic_roles"]};
}
export { assignSemanticRoles };
