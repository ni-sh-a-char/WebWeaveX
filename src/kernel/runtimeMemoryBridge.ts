/**
 * Converted from Python: core/kernel/runtime_memory_bridge.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { runMemoryForExtraction } from "../memory/runtimeMemoryOrchestrator.js";

export function runMemoryPhase(sources: any = null, tick: any = 0, kwargs: Record<string, any> = {}): any {
  return py.callKw(runMemoryForExtraction as (...a: any[]) => any, ["federated_memory", "memory_path", "memory_key", "sources", "nodes", "tick", "merge_graph"], {"federated_memory": true, "sources": sources, "tick": tick, "merge_graph": false}, Object.fromEntries(py.items(kwargs).filter(([k, v]: any) => py.contains(["memory_path", "memory_key"], k)).map(([k, v]: any) => ([k, v] as [any, any]))));
}
export { runMemoryForExtraction };
