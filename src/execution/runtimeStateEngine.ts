/**
 * Converted from Python: core/execution/runtime_state_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildExecutionState(runtime: any = "browser", active_actions: any = null, queue: any = null, mutations: any = null, checkpoint: any = null, transaction: any = null, federation: any = null): any {
  return {"current_runtime": runtime, "active_actions": [...py.iter(py.or2(active_actions, () => ([])))], "pending_queues": [...py.iter(py.or2(queue, () => ([])))], "mutations": [...py.iter(py.or2(mutations, () => ([])))], "checkpoint": py.pyDict(py.or2(checkpoint, () => ({}))), "transaction": py.pyDict(py.or2(transaction, () => ({}))), "federation_state": py.pyDict(py.or2(federation, () => ({}))), "bounded": true};
}
