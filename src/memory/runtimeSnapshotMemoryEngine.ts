/**
 * Converted from Python: core/memory/runtime_snapshot_memory_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function captureMemorySnapshot(state: any, tick: any = 0): any {
  return {"snapshot_id": `memory_snapshot:${py.toStr(tick)}`, "tick": tick, "state": py.pyDict(state), "bounded": true};
}
