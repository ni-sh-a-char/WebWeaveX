/**
 * Converted from Python: core/kernel/runtime_sync_bridge.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { runSyncForExtraction } from "../synchronization/runtimeSyncOrchestrator.js";

export function runSyncPhase(sources: any = null, tick: any = 0, kwargs: Record<string, any> = {}): any {
  var extraction: any = py.get(py.or2(sources, () => ({})), "extraction", {});
  return py.callKw(runSyncForExtraction as (...a: any[]) => any, ["synchronized_runtime", "memory_path", "memory_key", "tick", "browser", "native", "semantic_result", "workflow_result", "causality_result", "distributed_result", "session", "identity", "merge_graph"], {"synchronized_runtime": true, "tick": tick, "browser": py.or2(py.get(extraction, "browser_ir"), () => (py.get(extraction, "runtime"))), "merge_graph": false}, Object.fromEntries(py.items(kwargs).filter(([k, v]: any) => py.contains(["memory_path", "memory_key"], k)).map(([k, v]: any) => ([k, v] as [any, any]))));
}
export { runSyncForExtraction };
