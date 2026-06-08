/**
 * Converted from Python: core/autonomy/semantic_goal_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_GOAL_SIZE: any = 4096;
export function resolveSemanticGoal(payload: any): any {
  var goal: any = py.slice(py.toStr(py.get(payload, "goal", "")), null, MAX_GOAL_SIZE);
  return {"goal": goal, "resolved": py.truthy(goal), "priority": py.toInt(py.get(payload, "priority", 1))};
}
