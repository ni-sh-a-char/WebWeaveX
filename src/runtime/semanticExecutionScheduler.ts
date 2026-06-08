/**
 * Converted from Python: core/runtime/semantic_execution_scheduler.py
 * @generated — WebWeaveX python→javascript library port
 */

import { scheduleSemanticTasks } from "./semanticScheduler.js";

export function scheduleExecution(tasks: any, max_tasks: any = 32): any {
  return scheduleSemanticTasks(tasks, max_tasks);
}
export { scheduleSemanticTasks };
