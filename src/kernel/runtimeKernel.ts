/**
 * Converted from Python: core/kernel/runtime_kernel.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { compileUnifiedRuntimeIr, unifiedRuntimeIrToGraph } from "../ir/unifiedRuntimeIr.js";
import { enforceRuntimeBoundary } from "./runtimeBoundary.js";
import { publishRuntimeEvent } from "./runtimeBus.js";
import { coordinateKernelPhases } from "./runtimeCoordination.js";
import { dispatchRuntimePhase } from "./runtimeDispatcher.js";
import { runExecutionPhase } from "./runtimeExecutionBridge.js";
import { mergeRuntimeGraph } from "./runtimeGraphBridge.js";
import { initializeRuntime, shutdownRuntime } from "./runtimeLifecycle.js";
import { runMemoryPhase } from "./runtimeMemoryBridge.js";
import { buildKernelPolicy, enforceKernelPolicy } from "./runtimePolicy.js";
import { listRuntimePhases, registerRuntimePhase } from "./runtimeRegistry.js";
import { replayKernelState } from "./runtimeReplay.js";
import { scheduleKernelPhases } from "./runtimeScheduler.js";
import { runSemanticPhase } from "./runtimeSemanticBridge.js";
import { buildKernelState, mergeKernelState } from "./runtimeState.js";
import { runSyncPhase } from "./runtimeSyncBridge.js";
import { buildKernelTopology } from "./runtimeTopology.js";
import { runReconstructionForExtraction } from "../reconstruction/runtimeReconstructionOrchestrator.js";

export class RuntimeKernel {
  declare runtime_type: any;
  declare _initialized: any;
  declare _bus: any;
  declare _registry: any;
  declare _irs: any;
  constructor(runtime_type: any = "browser") {
    this.runtime_type = runtime_type;
    this._initialized = initializeRuntime(runtime_type);
    this._bus = [];
    this._registry = {"phases": {}};
    this._irs = [];
  }
  run_pipeline(sources: any = null, tick: any = 0, phases: any = null, options: any = null): any {
    sources = py.or2(sources, () => ({}));
    options = py.or2(options, () => ({}));
    var active_phases: any = py.or2(phases, () => (["semantic", "synchronization", "memory", "execution", "reconstruction"]));
    var schedule: any = scheduleKernelPhases(active_phases, tick);
    var policy: any = buildKernelPolicy();
    var phase_results: any[] = [];
    var state: any = py.pyDict(py.get(this._initialized, "state", {}));
    var entry: any;
    for (entry of py.iter(py.at(schedule, "scheduled"))) {
      var phase: any = py.at(entry, "phase");
      if ((py.eq(phase, "semantic") && py.truthy(py.get(options, "semantic", true)))) {
        var result: any = dispatchRuntimePhase(phase, () => py.callKw(runSemanticPhase as (...a: any[]) => any, ["sources", "tick", "**"], {"sources": sources, "tick": tick}, py.get(options, "semantic_opts", {})), py.get(state, "context", {}));
      } else if ((py.eq(phase, "synchronization") && py.truthy(py.get(options, "sync", true)))) {
        result = dispatchRuntimePhase(phase, () => py.callKw(runSyncPhase as (...a: any[]) => any, ["sources", "tick", "**"], {"sources": sources, "tick": tick}, py.get(options, "sync_opts", {})), py.get(state, "context", {}));
      } else if ((py.eq(phase, "memory") && py.truthy(py.get(options, "memory", true)))) {
        result = dispatchRuntimePhase(phase, () => py.callKw(runMemoryPhase as (...a: any[]) => any, ["sources", "tick", "**"], {"sources": sources, "tick": tick}, py.get(options, "memory_opts", {})), py.get(state, "context", {}));
      } else if ((py.eq(phase, "execution") && py.truthy(py.get(options, "execution", true)))) {
        result = dispatchRuntimePhase(phase, () => py.callKw(runExecutionPhase as (...a: any[]) => any, ["sources", "runtime", "tick", "**"], {"sources": sources, "runtime": this.runtime_type, "tick": tick}, py.get(options, "execution_opts", {})), py.get(state, "context", {}));
      } else if ((py.eq(phase, "reconstruction") && py.truthy(py.get(options, "reconstruction", true)))) {
        result = dispatchRuntimePhase(phase, () => py.callKw(runReconstructionForExtraction as (...a: any[]) => any, ["reconstruction_runtime", "memory_path", "memory_key", "sources", "runtime_graph", "runtime_type", "tick", "fabricate_runtime", "clone_runtime", "merge_graph"], {"reconstruction_runtime": true, "sources": sources, "runtime_type": this.runtime_type, "tick": tick, "merge_graph": false}, py.get(options, "reconstruction_opts", {})), py.get(state, "context", {}));
      } else {
        continue;
      }
      py.listAppend(phase_results, result);
      this._registry = registerRuntimePhase(this._registry, phase, py.get(result, "result", {}));
      var bus_update: any = publishRuntimeEvent(this._bus, phase, result, tick);
      this._bus = py.at(bus_update, "bus");
      var ir_key: any = `${py.toStr(phase)}_ir`;
      var ir_payload: any = py.get(py.get(result, "result", {}), ir_key, py.get(py.get(result, "result", {}), "memory_ir"));
      if (py.truthy(ir_payload)) {
        py.listAppend(this._irs, ir_payload);
      }
    }
    var graph: any = (py.truthy(this._irs) ? mergeRuntimeGraph(this._irs) : {});
    var topology: any = buildKernelTopology(graph);
    var enforcement: any = enforceKernelPolicy(policy, py.len(phase_results), py.get(topology, "node_count", 0));
    var boundary: any = enforceRuntimeBoundary({"irs": this._irs, "graph": graph});
    var unified_ir: any = compileUnifiedRuntimeIr(this._registry, graph, this._bus, phase_results);
    var coordination: any = coordinateKernelPhases(phase_results, tick);
    var replay: any = replayKernelState(this._bus);
    var payload: any = {"runtime_type": this.runtime_type, "schedule": schedule, "registry": this._registry, "coordination": coordination, "topology": topology, "graph": graph, "unified_ir": unified_ir, "replay": replay, "policy_enforcement": enforcement, "boundary": boundary, "phases": listRuntimePhases(), "bounded": true};
    state = mergeKernelState(state, {"graph": graph, "irs": this._irs});
    py.setItem(payload, "state", state);
    return payload;
  }
  shutdown(): any {
    return shutdownRuntime(py.get(this._initialized, "state", {}));
  }
}
var _KERNEL: any = null;
export function getRuntimeKernel(runtime_type: any = "browser"): any {
  if (((_KERNEL === null || _KERNEL === undefined) || !py.eq(_KERNEL.runtime_type, runtime_type))) {
    _KERNEL = new RuntimeKernel(runtime_type);
  }
  return _KERNEL;
}
export { buildKernelPolicy, buildKernelState, buildKernelTopology, compileUnifiedRuntimeIr, coordinateKernelPhases, dispatchRuntimePhase, enforceKernelPolicy, enforceRuntimeBoundary, initializeRuntime, listRuntimePhases, mergeKernelState, mergeRuntimeGraph, publishRuntimeEvent, registerRuntimePhase, replayKernelState, runExecutionPhase, runMemoryPhase, runReconstructionForExtraction, runSemanticPhase, runSyncPhase, scheduleKernelPhases, shutdownRuntime, unifiedRuntimeIrToGraph };
