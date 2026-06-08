/**
 * Converted from Python: core/workflows/workflow_state_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildWorkflowState(plan: any, execution: any = null, current_step: any = 0): any {
  execution = py.or2(execution, () => ({}));
  var executed: any = [...py.iter(py.get(execution, "executed", []))];
  var steps: any = [...py.iter(py.get(plan, "steps", []))];
  return {"current_step": current_step, "completed_steps": py.iter(executed).filter((item: any) => py.truthy(py.get(item, "completed"))).map((item: any) => py.at(item, "step_id")), "retries": 0, "runtime_state": {"objective": py.get(plan, "objective", ""), "total_steps": py.len(steps)}, "extraction_outputs": [], "semantic_checkpoints": [], "bounded": true};
}
