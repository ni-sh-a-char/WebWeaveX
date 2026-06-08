/**
 * Converted from Python: core/execution/runtime_execution_orchestrator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { compileExecutionRuntimeIr, executionRuntimeIrToGraph } from "../ir/executionRuntimeIr.js";
import { loadExecutionCheckpoint, saveExecutionCheckpoint } from "./runtimeCheckpointEngine.js";
import { coordinateRuntimeExecution } from "./runtimeCoordinationEngine.js";
import { executeRuntimeAction } from "./runtimeExecutionEngine.js";
import { federateRuntimeExecution } from "./runtimeFederationEngine.js";
import { trackRuntimeMutations } from "./runtimeMutationEngine.js";
import { buildRuntimePolicy, enforceRuntimePolicy } from "./runtimePolicyEngine.js";
import { buildRuntimePermissions } from "./runtimePermissionsEngine.js";
import { dequeueRuntimeAction, enqueueRuntimeAction } from "./runtimeQueueEngine.js";
import { recoverRuntimeExecution } from "./runtimeRecoveryEngine.js";
import { replayRuntimeExecution } from "./runtimeReplayEngine.js";
import { rollbackRuntimeState } from "./runtimeRollbackEngine.js";
import { buildRuntimeSandbox } from "./runtimeSandboxEngine.js";
import { scheduleRuntimeExecution } from "./runtimeSchedulerEngine.js";
import { simulateRuntimeExecution } from "./runtimeSimulationEngine.js";
import { buildExecutionState } from "./runtimeStateEngine.js";
import { beginRuntimeTransaction, commitRuntimeTransaction } from "./runtimeTransactionEngine.js";
import { applyRuntimeTransition } from "./runtimeTransitionEngine.js";
import { buildRuntimeGraph } from "../runtime_graph/runtimeGraphEngine.js";

export function _defaultActions(runtime: any): any {
  if (py.eq(runtime, "native")) {
    return [{"type": "native_focus", "window": "application"}];
  }
  if (py.eq(runtime, "terminal")) {
    return [{"type": "terminal_command", "command": "pwd"}];
  }
  return [{"type": "browser_click", "selector": "#submit"}];
}
export function runExecutionRuntime(sources: any = null, stored: any = null, workers: any = null, runtime: any = "browser", tick: any = 0, simulate: any = false, rollback_enabled: any = true): any {
  sources = py.or2(sources, () => ({}));
  stored = py.pyDict(py.or2(stored, () => ({})));
  workers = [...py.iter(py.or2(workers, () => ([{"worker_id": "primary", "runtime": runtime, "synced": true}])))];
  var sandbox: any = buildRuntimeSandbox(runtime);
  var policy: any = buildRuntimePolicy(py.eq(runtime, "terminal"));
  var permissions: any = buildRuntimePermissions((py.eq(runtime, "browser") ? ["browser", "native", "terminal", "connector", "vm"] : [runtime]));
  var prior_checkpoint: any = py.get(stored, "checkpoint", {});
  var checkpoint_body: any = (py.truthy(prior_checkpoint) ? py.get(prior_checkpoint, "state", prior_checkpoint) : {});
  var raw_actions: any = py.or2(py.get(sources, "actions"), () => (_defaultActions(runtime)));
  var executed_actions: any[] = [];
  var mutation_count: any = 0;
  var queue: any[] = [];
  var raw: any;
  for (raw of py.iter(py.slice(raw_actions, null, py.toInt(py.get(sandbox, "max_actions", 1000))))) {
    var enqueue_result: any = enqueueRuntimeAction(queue, raw, 0);
    queue = py.at(enqueue_result, "queue");
  }
  if (py.truthy(simulate)) {
    var simulation: any = simulateRuntimeExecution(raw_actions, sandbox, tick);
    var transition: any = applyRuntimeTransition("idle", "simulate");
    var payload: any = {"simulation": simulation, "transition": transition, "sandbox": sandbox, "bounded": true};
    py.setItem(payload, "execution_ir", compileExecutionRuntimeIr(payload));
    return payload;
  }
  var transaction: any = beginRuntimeTransaction(tick);
  transition = applyRuntimeTransition("idle", "enqueue");
  while (py.truthy(queue)) {
    var dequeue_result: any = dequeueRuntimeAction(queue);
    queue = py.at(dequeue_result, "queue");
    var action_raw: any = py.get(dequeue_result, "action");
    if (!py.truthy(action_raw)) {
      break;
    }
    raw = py.get(action_raw, "action", action_raw);
    var result: any = executeRuntimeAction(raw, sandbox, policy, permissions, tick, mutation_count, py.len(executed_actions));
    if (py.truthy(py.get(result, "executed"))) {
      py.listAppend(executed_actions, py.get(result, "action", {}));
      mutation_count = py.add(mutation_count, 1);
      var track_result: any = trackRuntimeMutations(py.get(transaction, "mutations", []), {"kind": py.toStr(py.get(result, "runtime", "action")), "target": py.toStr(py.get(result, "action_id", "")), "tick": tick});
      py.setItem(transaction, "mutations", py.get(track_result, "mutations", []));
      py.setItem(transaction, "actions", executed_actions);
    }
    transition = applyRuntimeTransition(py.at(transition, "to"), "execute");
  }
  transaction = commitRuntimeTransaction(transaction);
  transition = applyRuntimeTransition(py.at(transition, "to"), "commit");
  var mutations: any = trackRuntimeMutations(py.get(transaction, "mutations", []));
  var federation: any = federateRuntimeExecution(workers, executed_actions);
  var schedule: any = scheduleRuntimeExecution(executed_actions, undefined, undefined, undefined, tick);
  var coordination: any = coordinateRuntimeExecution([], federation, py.get(sources, "workflow"), py.get(sources, "sync"));
  var rollback_result: Record<string, any> = {};
  if ((py.truthy(rollback_enabled) && py.truthy(checkpoint_body))) {
    rollback_result = rollbackRuntimeState(checkpoint_body, buildExecutionState(runtime));
  }
  var recovery: any = recoverRuntimeExecution(py.iter(executed_actions).filter((a: any) => !py.truthy(a)).map((a: any) => a), checkpoint_body, (py.truthy(py.get(sources, "workflow")) ? [py.get(sources, "workflow")] : []));
  var state: any = buildExecutionState(runtime, executed_actions, queue, py.get(mutations, "mutations", []), checkpoint_body, transaction, federation);
  var replay: any = replayRuntimeExecution(executed_actions, [transaction], py.get(mutations, "mutations", []), tick);
  payload = {"actions": executed_actions, "queue": {"queue": queue, "size": py.len(queue)}, "transactions": [transaction], "mutations": mutations, "checkpoints": (py.truthy(checkpoint_body) ? [checkpoint_body] : []), "federation": federation, "synchronization": py.get(sources, "sync", {}), "state": state, "coordination": coordination, "schedule": schedule, "sandbox": sandbox, "policy": policy, "permissions": permissions, "rollback": rollback_result, "recovery": recovery, "replay": replay, "transition": transition, "bounded": true};
  py.setItem(payload, "execution_ir", compileExecutionRuntimeIr(payload));
  return payload;
}
export function runExecutionForExtraction(execution_runtime: any = true, memory_path: any = "", memory_key: any = "", sources: any = null, workers: any = null, runtime: any = "browser", tick: any = 0, simulate_execution: any = false, rollback_enabled: any = true, merge_graph: any = true): any {
  if (!py.truthy(execution_runtime)) {
    return {"enabled": false, "bounded": true};
  }
  var stored: Record<string, any> = {};
  if ((py.truthy(memory_path) && py.truthy(memory_key))) {
    var loaded: any = loadExecutionCheckpoint(memory_path, memory_key);
    if (py.truthy(py.get(loaded, "available"))) {
      stored = py.get(loaded, "checkpoint", stored);
    }
  }
  var result: any = runExecutionRuntime(sources, stored, workers, runtime, tick, simulate_execution, rollback_enabled);
  var store: any = {"checkpoint": {"state": py.get(result, "state", {}), "transactions": py.get(result, "transactions", []), "mutations": py.get(result, "mutations", {}), "workflows": (py.truthy(sources) ? py.get(sources, "workflow", {}) : {}), "synchronization": py.get(result, "synchronization", {}), "queues": [py.get(result, "queue", {})]}, "bounded": true};
  var persisted: any = false;
  if ((py.truthy(memory_path) && py.truthy(memory_key) && !py.truthy(simulate_execution))) {
    saveExecutionCheckpoint(memory_path, store, memory_key);
    persisted = true;
  }
  var graph_ir: any = executionRuntimeIrToGraph(py.get(result, "execution_ir", {}));
  var unified_graph: Record<string, any> = {};
  if (py.truthy(merge_graph)) {
    unified_graph = buildRuntimeGraph([graph_ir]);
  }
  return {"enabled": true, "execution": result, "execution_ir": py.get(result, "execution_ir", {}), "execution_graph_ir": graph_ir, "unified_graph": unified_graph, "replay": py.get(result, "replay", {}), "simulation": py.get(result, "simulation", {}), "execution_persisted": persisted, "bounded": true};
}
export { applyRuntimeTransition, beginRuntimeTransaction, buildExecutionState, buildRuntimeGraph, buildRuntimePermissions, buildRuntimePolicy, buildRuntimeSandbox, commitRuntimeTransaction, compileExecutionRuntimeIr, coordinateRuntimeExecution, dequeueRuntimeAction, enforceRuntimePolicy, enqueueRuntimeAction, executeRuntimeAction, executionRuntimeIrToGraph, federateRuntimeExecution, loadExecutionCheckpoint, recoverRuntimeExecution, replayRuntimeExecution, rollbackRuntimeState, saveExecutionCheckpoint, scheduleRuntimeExecution, simulateRuntimeExecution, trackRuntimeMutations };
