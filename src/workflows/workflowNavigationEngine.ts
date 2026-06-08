/**
 * Converted from Python: core/workflows/workflow_navigation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let RUNTIME_NAVIGATORS: any = {"browser": "browser_navigation", "electron": "electron_navigation", "desktop": "modal_traversal", "terminal": "terminal_progression", "native": "vm_runtime_transition", "remote": "remote_runtime_traversal", "application": "application_navigation", "repository": "repository_navigation"};
export function navigateRuntimeWorkflow(plan: any, tick: any = 0): any {
  var navigations: any[] = [];
  var index: any;
  var step: any;
  for ([index, step] of py.enumerate(py.slice(py.get(plan, "steps", []), null, 10000))) {
    var runtime: any = py.toStr(py.get(step, "runtime", "browser"));
    py.listAppend(navigations, {"step_id": py.toStr(py.get(step, "id", `step:${py.toStr(index)}`)), "runtime": runtime, "navigator": py.get(RUNTIME_NAVIGATORS, runtime, "browser_navigation"), "action": py.toStr(py.get(step, "action", "")), "tick": py.add(tick, index)});
  }
  return {"navigations": navigations, "count": py.len(navigations), "bounded": true};
}
