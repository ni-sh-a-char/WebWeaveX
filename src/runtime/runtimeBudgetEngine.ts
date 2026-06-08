/**
 * Converted from Python: core/runtime/runtime_budget_engine.py
 * @generated — WebWeaveX python→javascript library port
 */


export let MAX_RUNTIME_TASKS: any = 1000;
export let MAX_RUNTIME_MEMORY_MB: any = 512;
export let MAX_RUNTIME_SECONDS: any = 30;
export class RuntimeBudget {
  declare max_tasks: any;
  declare max_memory_mb: any;
  declare max_runtime_seconds: any;
  constructor(max_tasks: any = MAX_RUNTIME_TASKS, max_memory_mb: any = MAX_RUNTIME_MEMORY_MB, max_runtime_seconds: any = MAX_RUNTIME_SECONDS) {
    this.max_tasks = max_tasks;
    this.max_memory_mb = max_memory_mb;
    this.max_runtime_seconds = max_runtime_seconds;
  }
}
export let DEFAULT_RUNTIME_BUDGET: any = new RuntimeBudget();
