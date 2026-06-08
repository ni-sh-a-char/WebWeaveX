/**
 * Converted from Python: core/kernel/runtime_execution_bridge.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { runExecutionForExtraction } from "../execution/runtimeExecutionOrchestrator.js";

export function runExecutionPhase(sources: any = null, runtime: any = "browser", tick: any = 0, kwargs: Record<string, any> = {}): any {
  return py.callKw(runExecutionForExtraction as (...a: any[]) => any, ["execution_runtime", "memory_path", "memory_key", "sources", "workers", "runtime", "tick", "simulate_execution", "rollback_enabled", "merge_graph"], {"execution_runtime": true, "sources": sources, "runtime": runtime, "tick": tick, "merge_graph": false}, Object.fromEntries(py.items(kwargs).filter(([k, v]: any) => py.contains(["memory_path", "memory_key", "simulate_execution", "rollback_enabled"], k)).map(([k, v]: any) => ([k, v] as [any, any]))));
}
export { runExecutionForExtraction };
