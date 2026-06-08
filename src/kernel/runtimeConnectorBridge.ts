/**
 * Converted from Python: core/kernel/runtime_connector_bridge.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { runLiveForExtraction } from "../connectors/liveRuntimeOrchestrator.js";

export function runConnectorPhase(sources: any = null, tick: any = 0, kwargs: Record<string, any> = {}): any {
  return py.callKw(runLiveForExtraction as (...a: any[]) => any, ["live_runtime", "memory_path", "memory_key", "config", "snapshot", "tick", "merge_graph"], {"live_runtime": true, "tick": tick, "merge_graph": false}, Object.fromEntries(py.items(kwargs).filter(([k, v]: any) => py.contains(["memory_path", "memory_key", "snapshot"], k)).map(([k, v]: any) => ([k, v] as [any, any]))));
}
export { runLiveForExtraction };
