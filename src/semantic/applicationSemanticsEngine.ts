/**
 * Converted from Python: core/semantic/application_semantics_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractApplicationSemantics(application_result: any = null): any {
  application_result = py.or2(application_result, () => ({}));
  var workflow: any = py.get(application_result, "workflow", {});
  var execution: any = py.get(application_result, "execution", {});
  var forms: any = py.get(application_result, "forms", {});
  return {"workflow_purpose": py.toStr(py.get(py.get(application_result, "intent", {}), "intent", "operate")), "runtime_intent": py.toStr(py.get(execution, "objective", "")), "business_operations": py.iter(py.get(execution, "executed", [])).map((step: any) => py.toStr(py.get(step, "action", ""))), "ui_functionality": [...py.iter(py.keys(py.get(application_result, "ui_semantics", {})))], "operational_actions": py.len(py.get(workflow, "edges", [])), "form_operations": py.len(py.get(forms, "forms", [])), "bounded": true};
}
