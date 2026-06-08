/**
 * Converted from Python: core/memory/semantic_replay_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function replaySemanticHistory(checkpoints: any): any {
  var ordered: any = py.sorted(checkpoints, {key: ((c: any) => py.toStr(py.get(c, "fingerprint", ""))) as (item: any) => any});
  var states: any = py.iter(ordered).map((c: any) => py.get(c, "state", {}));
  return {"states": states, "count": py.len(states), "deterministic": true};
}
