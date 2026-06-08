/**
 * Converted from Python: core/application/application_recovery_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildFormRuntime } from "./formRuntimeEngine.js";

export function recoverApplicationRuntime(html: any, state: any): any {
  var forms: any = buildFormRuntime(html);
  var recovered_forms: any[] = [];
  var form: any;
  for (form of py.iter(py.get(forms, "forms", []))) {
    if (!py.truthy(py.get(form, "inputs"))) {
      py.listAppend(recovered_forms, {...(form), "recovered": true, "inputs": [{"name": "fallback", "type": "text", "required": false}]});
    } else {
      py.listAppend(recovered_forms, {...(form), "recovered": true});
    }
  }
  return {"route": py.get(state, "route", "/"), "forms_recovered": recovered_forms, "modals_cleared": py.eq(py.len(py.get(state, "modals", [])), 0), "session_valid": py.get(state, "authenticated", false), "workflow_resumed": true, "bounded": true};
}
export { buildFormRuntime };
