/**
 * Converted from Python: core/application/runtime_goal_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let OBJECTIVES: any = {"login": ["open_login", "fill_credentials", "submit"], "extract_dashboard": ["navigate_dashboard", "capture_widgets", "capture_tables"], "export_report": ["open_reports", "select_report", "export"], "extract_invoices": ["open_invoices", "paginate", "extract_rows"], "monitor_metrics": ["open_dashboard", "observe_metrics", "checkpoint"]};
export function buildRuntimeGoal(objective: any): any {
  var steps: any = py.get(OBJECTIVES, objective, ["observe", "extract"]);
  return {"objective": objective, "steps": [...py.iter(steps)], "bounded": true};
}
