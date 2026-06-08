/**
 * Converted from Python: core/autonomy/semantic_planning_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { resolveSemanticGoal } from "./semanticGoalEngine.js";
import { decomposeSemanticTask } from "./semanticTaskDecompositionEngine.js";

export let MAX_PLAN_STEPS: any = 1000;
export function planSemanticAutonomy(payload: any): any {
  var goal: any = resolveSemanticGoal(payload);
  var decomposition: any = decomposeSemanticTask(goal);
  var steps: any = py.enumerate(py.slice(py.get(decomposition, "subtasks", []), null, MAX_PLAN_STEPS)).map(([idx, subtask]: any) => ({"step": idx, "action": py.get(subtask, "semantic_unit"), "task_id": py.get(subtask, "id")}));
  return {"goal": goal, "steps": steps, "step_count": py.len(steps), "bounded": true};
}
export { decomposeSemanticTask, resolveSemanticGoal };
