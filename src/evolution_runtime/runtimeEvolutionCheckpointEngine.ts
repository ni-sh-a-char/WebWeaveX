/**
 * Converted from Python: core/evolution_runtime/runtime_evolution_checkpoint_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { decryptValue, encryptValue } from "../crypto/kaalkaRuntimeEngine.js";

export function saveEvolutionCheckpoint(path: any, checkpoint: any, key: any): any {
  var payload: any = py.jsonDumps(checkpoint, {sortKeys: true});
  var encrypted: any = encryptValue(payload, key);
  var target: any = py.path(path);
  target.parent.mkdir(true, true);
  target.write_text(py.jsonDumps({"encrypted": py.at(encrypted, "encrypted"), "algorithm": "kaalka"}, {sortKeys: true}), "utf-8");
  return {"saved": true, "path": py.toStr(target), "algorithm": "kaalka", "bounded": true};
}
export function loadEvolutionCheckpoint(path: any, key: any): any {
  var target: any = py.path(path);
  if (!py.truthy(target.exists())) {
    return {"available": false, "checkpoint": _emptyCheckpoint(), "bounded": true};
  }
  var wrapper: any = py.jsonLoads(target.read_text("utf-8"));
  var decrypted: any = decryptValue(py.at(wrapper, "encrypted"), key);
  var checkpoint: any = py.jsonLoads(py.at(decrypted, "decrypted"));
  return {"available": true, "checkpoint": checkpoint, "algorithm": "kaalka", "bounded": true};
}
export function _emptyCheckpoint(): any {
  return {"evolution_state": {}, "distributed_histories": [], "lineage_graph": {}, "convergence_state": {}, "bounded": true};
}
export { decryptValue, encryptValue };
