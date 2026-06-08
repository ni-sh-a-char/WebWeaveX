/**
 * Converted from Python: core/distributed/distributed_checkpoint_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function createDistributedCheckpoint(state: any): any {
  var serialized: any = py.jsonDumps(state, {sortKeys: true, defaultStr: true});
  var fingerprint: any = py.hashNew("sha256", py.encode(serialized, "utf-8")).hexdigest();
  return {"fingerprint": fingerprint, "state": state};
}
