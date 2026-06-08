/**
 * Converted from Python: core/evolution_runtime/runtime_strategy_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimeStrategy(evidence: any = null): any {
  evidence = py.or2(evidence, () => ({}));
  var drift_count: any = py.toInt(py.get(evidence, "drift_count", 0));
  var failed_steps: any = py.toInt(py.get(evidence, "failed_steps", 0));
  return {"extraction_path": (py.eq(drift_count, 0) ? "browser_first" : "repair_then_extract"), "synchronization_path": (py.eq(failed_steps, 0) ? "continuous" : "converge_then_sync"), "workflow_order": "priority_asc", "selector_hierarchy": ["healed", "structural", "fallback"], "recovery_order": ["heal_selector", "recover_workflow", "resync_runtime"], "bounded": true};
}
