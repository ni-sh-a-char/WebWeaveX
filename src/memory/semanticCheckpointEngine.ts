/**
 * Converted from Python: core/memory/semantic_checkpoint_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_CHECKPOINT_BYTES: any = 2000000;
export function createSemanticCheckpoint(state: any): any {
  var encoded: any = py.encode(py.jsonDumps(state, {sortKeys: true}), "utf-8");
  var bounded: any = py.slice(encoded, null, MAX_CHECKPOINT_BYTES);
  var fingerprint: any = py.hashNew("sha256", bounded).hexdigest();
  return {"fingerprint": fingerprint, "size": py.len(bounded), "state": state, "deterministic": true};
}
