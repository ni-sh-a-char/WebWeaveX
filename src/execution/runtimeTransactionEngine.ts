/**
 * Converted from Python: core/execution/runtime_transaction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function beginRuntimeTransaction(tick: any = 0, checkpoint_id: any = ""): any {
  var payload: any = py.jsonDumps({"tick": tick, "checkpoint": checkpoint_id}, {sortKeys: true});
  var transaction_id: any = py.slice(py.hashNew("sha256", py.encode(payload, "utf-8")).hexdigest(), null, 32);
  return {"transaction_id": transaction_id, "actions": [], "mutations": [], "transitions": [], "checkpoints": (py.truthy(checkpoint_id) ? [checkpoint_id] : []), "committed": false, "rolled_back": false, "bounded": true};
}
export function commitRuntimeTransaction(transaction: any): any {
  var updated: any = py.pyDict(transaction);
  py.setItem(updated, "committed", true);
  py.setItem(updated, "rolled_back", false);
  return updated;
}
export function rollbackRuntimeTransaction(transaction: any): any {
  var updated: any = py.pyDict(transaction);
  py.setItem(updated, "committed", false);
  py.setItem(updated, "rolled_back", true);
  py.setItem(updated, "actions", []);
  py.setItem(updated, "mutations", []);
  return updated;
}
