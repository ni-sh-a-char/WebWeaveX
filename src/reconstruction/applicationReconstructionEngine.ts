/**
 * Converted from Python: core/reconstruction/application_reconstruction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function reconstructApplicationRuntime(application_ir: any = null, workflow_ir: any = null, execution_ir: any = null, runtime_type: any = "browser"): any {
  application_ir = py.or2(application_ir, () => ({}));
  workflow_ir = py.or2(workflow_ir, () => ({}));
  execution_ir = py.or2(execution_ir, () => ({}));
  var workflows: any = py.get(workflow_ir, "workflows", py.get(workflow_ir, "workflow", {}));
  if ((((workflows !== null && typeof workflows === "object" && !Array.isArray(workflows) && !(workflows instanceof Set) && !(workflows instanceof Map))) && py.contains(workflows, "objective"))) {
    workflows = [workflows];
  }
  return {"runtime_type": runtime_type, "workflows": ((Array.isArray(workflows)) ? [...py.iter(workflows)] : []), "forms": py.pyDict(py.get(application_ir, "forms", {})), "dashboards": [...py.iter(py.get(application_ir, "dashboards", []))], "modals": [...py.iter(py.get(application_ir, "modals", []))], "tabs": [...py.iter(py.get(application_ir, "tabs", []))], "application_graph": py.pyDict(py.get(application_ir, "graph", py.get(application_ir, "action_graphs", {}))), "execution_state": py.pyDict(py.get(execution_ir, "execution_state", py.get(execution_ir, "state", {}))), "replay_safe": true, "bounded": true};
}
