/**
 * Converted from Python: core/application/application_intent_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let INTENT_MAP: any = {"extract_dashboard": "observe_metrics", "login": "authenticate", "export_report": "export_data", "extract_invoices": "collect_records", "monitor_metrics": "continuous_observe"};
export function resolveApplicationIntent(objective: any): any {
  return {"objective": objective, "intent": py.get(INTENT_MAP, objective, "observe"), "bounded": true};
}
