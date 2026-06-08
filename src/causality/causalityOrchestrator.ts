/**
 * Converted from Python: core/causality/causality_orchestrator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { bridgeBrowserNativeRuntime } from "./browserNativeBridgeEngine.js";
import { buildCausalGraph } from "./causalGraphEngine.js";
import { loadCausalMemory } from "./causalMemoryEngine.js";
import { rememberCausalRuntime } from "./causalMemoryEngine.js";
import { saveCausalMemory } from "./causalMemoryEngine.js";
import { recoverCausalRuntime } from "./causalRecoveryEngine.js";
import { replayCausalRuntime } from "./causalReplayEngine.js";
import { alignCrossRuntimeEvents } from "./crossRuntimeAlignmentEngine.js";
import { buildDistributedCausality } from "./distributedCausalityEngine.js";
import { bridgeElectronTerminalRuntime } from "./electronTerminalBridgeEngine.js";
import { buildEventChain } from "./eventChainEngine.js";
import { trackNotificationCausality } from "./notificationCausalityEngine.js";
import { trackProcessCausality } from "./processCausalityEngine.js";
import { buildRuntimeCausality } from "./runtimeCausalityEngine.js";
import { correlateRuntimeMutations } from "./runtimeCorrelationEngine.js";
import { buildRuntimeDependencies } from "./runtimeDependencyEngine.js";
import { buildRuntimeSequence } from "./runtimeSequenceEngine.js";
import { buildRuntimeTimeline } from "./runtimeTimelineEngine.js";
import { buildStateTransitions } from "./stateTransitionEngine.js";
import { buildWorkflowPropagation } from "./workflowPropagationEngine.js";
import { causalRuntimeIrToGraph, compileCausalRuntimeIr } from "../ir/causalRuntimeIr.js";
import { buildRuntimeGraph } from "../runtime_graph/runtimeGraphEngine.js";

export function _normalizeInteractionEvents(interactions: any, runtime: any = "browser"): any {
  var events: any[] = [];
  var index: any;
  var interaction: any;
  for ([index, interaction] of py.enumerate(py.slice(interactions, null, 10000))) {
    py.listAppend(events, {"id": `${py.toStr(runtime)}:evt:${py.toStr(index)}`, "runtime": runtime, "type": py.toStr(py.get(interaction, "action", py.get(interaction, "type", "mutation"))), "step": index, "source": py.toStr(py.get(interaction, "from", py.get(interaction, "selector", ""))), "target": py.toStr(py.get(interaction, "to", "")), "state": py.toStr(py.get(interaction, "state", ""))});
  }
  return events;
}
export function _eventsFromNativeCognition(cognition: any): any {
  var events: any[] = [];
  var step: any = 0;
  var interaction: any;
  for (interaction of py.iter(py.get(cognition, "interactions", []))) {
    py.listAppend(events, {"id": `native:evt:${py.toStr(step)}`, "runtime": py.get(cognition, "runtime", "desktop"), "type": py.toStr(py.get(interaction, "action", "interaction")), "step": step});
    step = py.add(step, 1);
  }
  var terminal: any = py.get(cognition, "terminal", {});
  var line: any;
  for (line of py.iter(py.slice(py.get(terminal, "output", []), null, 1000))) {
    py.listAppend(events, {"id": `terminal:evt:${py.toStr(step)}`, "runtime": "terminal", "type": "log", "step": step, "state": line});
    step = py.add(step, 1);
  }
  var electron: any = py.get(cognition, "electron", {});
  var route: any;
  for (route of py.iter(py.get(electron, "routes", []))) {
    py.listAppend(events, {"id": `electron:evt:${py.toStr(step)}`, "runtime": "electron", "type": "route", "step": step, "state": route});
    step = py.add(step, 1);
  }
  var notification: any;
  for (notification of py.iter(py.get(py.get(cognition, "desktop", {}), "notifications", []))) {
    py.listAppend(events, {"id": `desktop:notif:${py.toStr(step)}`, "runtime": "desktop", "type": "notification", "step": step, "state": py.toStr(notification)});
    step = py.add(step, 1);
  }
  return events;
}
export function runCausalityRuntime(browser_events: any = null, native_cognition: any = null, application_result: any = null, distributed_result: any = null, memory: any = null, interactions: any = null): any {
  memory = py.pyDict(py.or2(memory, () => ({})));
  browser_events = [...py.iter(py.or2(browser_events, () => (_normalizeInteractionEvents(py.or2(interactions, () => ([])), "browser"))))];
  var native_events: any = _eventsFromNativeCognition(py.or2(native_cognition, () => ({})));
  if (py.truthy(application_result)) {
    var index: any;
    var _: any;
    for ([index, _] of py.enumerate(py.slice(py.get(py.get(application_result, "workflow", {}), "nodes", []), null, 100))) {
      py.listAppend(browser_events, {"id": `application:evt:${py.toStr(index)}`, "runtime": "application", "type": "workflow", "step": py.add(py.len(browser_events), index)});
    }
  }
  var all_events: any = py.add(browser_events, native_events);
  all_events = py.sorted(all_events, {key: ((item: any) => py.toInt(py.get(item, "step", 0))) as (item: any) => any});
  var origins: any = {"browser": py.len(browser_events), "native": py.len(native_events), "distributed": py.truthy(distributed_result)};
  var causality: any = buildRuntimeCausality(all_events, origins);
  var event_chain: any = buildEventChain(all_events);
  var alignment: any = alignCrossRuntimeEvents(all_events);
  var dependencies: any = buildRuntimeDependencies(all_events, {"synchronization_chains": []});
  var propagation: any = buildWorkflowPropagation(alignment, dependencies);
  dependencies = buildRuntimeDependencies(all_events, propagation);
  var causal_graph: any = buildCausalGraph(all_events, causality);
  var transitions: any = buildStateTransitions(all_events);
  var sequence: any = buildRuntimeSequence(all_events);
  var timeline: any = buildRuntimeTimeline(all_events, propagation);
  var correlation: any = correlateRuntimeMutations(browser_events, native_events, py.get(py.get(py.or2(native_cognition, () => ({})), "desktop", {}), "notifications", []), py.get(py.get(py.or2(native_cognition, () => ({})), "terminal", {}), "output", []), py.get(py.get(py.or2(native_cognition, () => ({})), "processes", {}), "processes", []));
  var distributed: any = buildDistributedCausality(distributed_result);
  var browser_bridge: any = bridgeBrowserNativeRuntime(browser_events, native_events);
  var electron_events: any = py.iter(native_events).filter((e: any) => py.eq(py.get(e, "runtime"), "electron")).map((e: any) => e);
  var terminal_events: any = py.iter(native_events).filter((e: any) => py.eq(py.get(e, "runtime"), "terminal")).map((e: any) => e);
  var electron_bridge: any = bridgeElectronTerminalRuntime(electron_events, terminal_events);
  var notification_causality: any = trackNotificationCausality(py.get(py.get(py.or2(native_cognition, () => ({})), "desktop", {}), "notifications", []), all_events);
  var process_causality: any = trackProcessCausality(py.get(py.get(py.or2(native_cognition, () => ({})), "processes", {}), "processes", []), all_events);
  var recovery: any = recoverCausalRuntime(causality, all_events);
  var payload: any = {"causality": causality, "event_chain": event_chain, "alignment": alignment, "propagation": propagation, "dependencies": dependencies, "causal_graph": causal_graph, "transitions": transitions, "sequence": sequence, "timeline": timeline, "correlation": correlation, "distributed": distributed, "browser_bridge": browser_bridge, "electron_bridge": electron_bridge, "notification_causality": notification_causality, "process_causality": process_causality, "recovery": recovery, "bounded": true};
  var updated_memory: any = rememberCausalRuntime(memory, {"event_chains": event_chain, "runtime_propagation": causality, "causal_graphs": causal_graph, "distributed_workflows": distributed, "synchronization_state": alignment, "alignment": alignment, "timeline": timeline});
  py.setItem(payload, "memory", updated_memory);
  py.setItem(payload, "replay", replayCausalRuntime(updated_memory));
  py.setItem(payload, "causal_ir", compileCausalRuntimeIr(payload));
  return payload;
}
export function runCausalityForExtraction(causality_runtime: any = true, memory_path: any = "", memory_key: any = "", browser_events: any = null, native_cognition: any = null, application_result: any = null, distributed_result: any = null, interactions: any = null, merge_graph: any = true): any {
  if (!py.truthy(causality_runtime)) {
    return {"enabled": false, "bounded": true};
  }
  var memory: Record<string, any> = {};
  if ((py.truthy(memory_path) && py.truthy(memory_key))) {
    var loaded: any = loadCausalMemory(memory_path, memory_key);
    if (py.truthy(py.get(loaded, "available"))) {
      memory = py.get(loaded, "memory", memory);
    }
  }
  var result: any = runCausalityRuntime(browser_events, native_cognition, application_result, distributed_result, memory, interactions);
  var persisted: any = false;
  if ((py.truthy(memory_path) && py.truthy(memory_key))) {
    saveCausalMemory(memory_path, py.get(result, "memory", {}), memory_key);
    persisted = true;
  }
  var graph_ir: any = causalRuntimeIrToGraph(py.get(result, "causal_ir", {}));
  var unified_graph: Record<string, any> = {};
  if (py.truthy(merge_graph)) {
    unified_graph = buildRuntimeGraph([graph_ir]);
  }
  return {"enabled": true, "causality": result, "causal_ir": py.get(result, "causal_ir", {}), "causal_graph_ir": graph_ir, "unified_graph": unified_graph, "replay": py.get(result, "replay", {}), "memory_persisted": persisted, "bounded": true};
}
export { alignCrossRuntimeEvents, bridgeBrowserNativeRuntime, bridgeElectronTerminalRuntime, buildCausalGraph, buildDistributedCausality, buildEventChain, buildRuntimeCausality, buildRuntimeDependencies, buildRuntimeGraph, buildRuntimeSequence, buildRuntimeTimeline, buildStateTransitions, buildWorkflowPropagation, causalRuntimeIrToGraph, compileCausalRuntimeIr, correlateRuntimeMutations, loadCausalMemory, recoverCausalRuntime, rememberCausalRuntime, replayCausalRuntime, saveCausalMemory, trackNotificationCausality, trackProcessCausality };
