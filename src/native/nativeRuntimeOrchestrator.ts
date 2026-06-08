/**
 * Converted from Python: core/native/native_runtime_orchestrator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { runApplicationCognition } from "../application/applicationCognitionOrchestrator.js";
import { compileNativeRuntimeIr, nativeRuntimeIrToGraph } from "../ir/nativeRuntimeIr.js";
import { extractAccessibilityTree } from "./accessibilityTreeEngine.js";
import { buildDesktopRuntime } from "./desktopRuntimeEngine.js";
import { extractElectronRuntime } from "./electronRuntimeEngine.js";
import { resolveNativeFocus } from "./nativeFocusEngine.js";
import { buildInteractionSequence } from "./nativeInteractionEngine.js";
import { loadNativeRuntime } from "./nativeMemoryEngine.js";
import { rememberNativeRuntime } from "./nativeMemoryEngine.js";
import { saveNativeRuntime } from "./nativeMemoryEngine.js";
import { buildNativeNavigation } from "./nativeNavigationEngine.js";
import { enumerateNativeProcesses } from "./nativeProcessEngine.js";
import { extractRemoteRuntime } from "./nativeRemoteSessionEngine.js";
import { replayNativeRuntime } from "./nativeReplayEngine.js";
import { buildNativeState } from "./nativeStateEngine.js";
import { captureNativeStreams } from "./nativeStreamEngine.js";
import { captureTerminalRuntime } from "./nativeTerminalEngine.js";
import { buildNativeUiGraph } from "./nativeUiGraphEngine.js";
import { extractVmRuntime } from "./nativeVmEngine.js";
import { extractNativeWindows } from "./nativeWindowEngine.js";
import { alignNativeRuntime } from "./nativeRuntimeAlignmentEngine.js";
import { buildRuntimeGraph } from "../runtime_graph/runtimeGraphEngine.js";
import { runCausalityForExtraction } from "../causality/causalityOrchestrator.js";
import { causalRuntimeIrToGraph } from "../ir/causalRuntimeIr.js";
import { runSemanticForExtraction } from "../semantic/semanticOrchestrator.js";
import { semanticRuntimeIrToGraph } from "../ir/semanticRuntimeIr.js";
import { runWorkflowForExtraction } from "../workflows/workflowOrchestrator.js";
import { workflowRuntimeIrToGraph } from "../ir/workflowRuntimeIr.js";
import { runSyncForExtraction } from "../synchronization/runtimeSyncOrchestrator.js";
import { synchronizationRuntimeIrToGraph } from "../ir/synchronizationRuntimeIr.js";
import { runEvolutionForExtraction } from "../evolution_runtime/runtimeEvolutionOrchestrator.js";
import { evolutionRuntimeIrToGraph } from "../ir/evolutionRuntimeIr.js";
import { runLiveForExtraction } from "../connectors/liveRuntimeOrchestrator.js";
import { liveRuntimeIrToGraph } from "../ir/liveRuntimeIr.js";
import { runMemoryForExtraction } from "../memory/runtimeMemoryOrchestrator.js";
import { runtimeMemoryIrToGraph } from "../ir/runtimeMemoryIr.js";
import { runExecutionForExtraction } from "../execution/runtimeExecutionOrchestrator.js";
import { executionRuntimeIrToGraph } from "../ir/executionRuntimeIr.js";
import { runReconstructionForExtraction } from "../reconstruction/runtimeReconstructionOrchestrator.js";
import { reconstructionRuntimeIrToGraph } from "../ir/reconstructionRuntimeIr.js";
import { extractWindowsUiaSnapshot } from "./platform/windowsUiaRuntime.js";
import { extractMacosAxSnapshot } from "./platform/macosAxRuntime.js";
import { extractLinuxAtspiSnapshot } from "./platform/linuxAtspiRuntime.js";
import { extractElectronCdp, extractElectronIpc, extractElectronRoutes, extractElectronStorage } from "./electron/index.js";
import { stableElectronRuntimeHash } from "./electron/electronHashEngine.js";

export function _fixtureForApplication(application: any): any {
  var app: any = String(application).toLowerCase();
  return {"windows": [{"id": `win:${py.toStr(app)}`, "title": `${py.toStr(py.title(app))} — Main`, "application": app, "bounds": {"x": 0, "y": 0, "width": 1280, "height": 720}, "visible": true, "z_order": 1, "focused": true}], "focused_window": `${py.toStr(py.title(app))} — Main`, "nodes": [{"id": "btn:login", "role": "button", "name": "Login"}, {"id": "input:user", "role": "textbox", "name": "Username"}, {"id": "dlg:settings", "role": "dialog", "name": "Settings"}], "active_apps": [{"name": app}], "routes": ["/"], "output": ["$ echo hello", "hello"], "commands": ["echo hello"], "prompts": ["$"]};
}
export function runNativeCognition(runtime: any = "desktop", application: any = "", snapshot: any = null, memory: any = null, interactions: any = null, application_cognition: any = false, adaptive_runtime: any = null, application_memory: any = null): any {
  memory = py.pyDict(py.or2(memory, () => ({})));
  interactions = [...py.iter(py.or2(interactions, () => ([])))];
  var snap: any = py.pyDict(py.or2(snapshot, () => (_fixtureForApplication(py.or2(application, () => ("desktop"))))));
  var platform_probe: any = {"bounded": true};
  if (py.eq(py.sysShim.platform, "win32")) {
    platform_probe = extractWindowsUiaSnapshot(snap);
  } else if (py.eq(py.sysShim.platform, "darwin")) {
    platform_probe = extractMacosAxSnapshot(snap);
  } else if (py.eq(py.sysShim.platform, "linux")) {
    platform_probe = extractLinuxAtspiSnapshot(snap);
  }
  var windows: any = extractNativeWindows(snap);
  var accessibility: any = extractAccessibilityTree(snap);
  var desktop: any = buildDesktopRuntime(windows, accessibility, snap);
  var electron: any = extractElectronRuntime(application, snap);
  if (py.eq(runtime, "electron")) {
    electron = {...(electron), "cdp": extractElectronCdp(`electron://${py.toStr(application)}`), "storage": extractElectronStorage(snap), "routes": extractElectronRoutes(py.get(snap, "routes")), "ipc": extractElectronIpc(py.get(snap, "ipc_channels")), "bounded": true};
    py.setItem(electron, "runtime_hash", stableElectronRuntimeHash(electron));
  }
  var terminal: any = captureTerminalRuntime(undefined, snap);
  var vm: any = extractVmRuntime(undefined, py.get(snap, "vm"));
  var remote: any = extractRemoteRuntime(py.get(snap, "remote_protocol", "ssh"), py.get(snap, "remote"));
  var processes: any = enumerateNativeProcesses(snap);
  var focus: any = resolveNativeFocus(windows, accessibility);
  var navigation: any = buildNativeNavigation(desktop, electron);
  var ui_graph: any = buildNativeUiGraph(windows, accessibility, interactions);
  var interaction_log: any = buildInteractionSequence(interactions);
  var streams: any = captureNativeStreams(terminal, desktop, electron);
  var state: any = buildNativeState(runtime, windows, desktop, py.get(focus, "control"));
  var app_cognition: Record<string, any> = {};
  if ((py.truthy(application_cognition) && py.truthy(application))) {
    app_cognition = runApplicationCognition(`native://${py.toStr(application)}`, "<html></html>", undefined, application_memory, "extract_dashboard");
  }
  var alignment: any = alignNativeRuntime(state, adaptive_runtime, py.or2(application_memory, () => (py.get(app_cognition, "memory"))));
  var updated_memory: any = rememberNativeRuntime(memory, {"windows": windows, "accessibility_trees": accessibility, "runtime_graphs": ui_graph, "electron_state": electron, "terminal_streams": terminal, "workflows": navigation, "interactions": interaction_log, "vm": vm, "remote": remote, "processes": processes, "streams": streams, "native_state": state});
  var cognition_payload: any = {"runtime": runtime, "application": application, "platform_probe": platform_probe, "windows": windows, "accessibility": accessibility, "desktop": desktop, "electron": electron, "terminal": terminal, "vm": vm, "remote": remote, "processes": processes, "navigation": navigation, "ui_graph": ui_graph, "interactions": interaction_log, "streams": streams, "native_state": state, "application_cognition": app_cognition, "alignment": alignment, "memory": updated_memory, "bounded": true};
  py.setItem(cognition_payload, "native_ir", compileNativeRuntimeIr(cognition_payload));
  return cognition_payload;
}
export function extractNative(runtime: any = "desktop", application: any = "discord", application_cognition: any = true, persistent_runtime: any = true, runtime_path: any = "native.enc", runtime_key: any = "master-key", snapshot: any = null, interactions: any = null, adaptive_runtime: any = null, application_memory: any = null, merge_runtime_graph: any = true, causality_runtime: any = false, causal_memory_path: any = "", causal_memory_key: any = "", semantic_runtime: any = false, semantic_memory_path: any = "", semantic_memory_key: any = "", autonomous_workflow: any = false, workflow_memory_path: any = "", workflow_memory_key: any = "", workflow_objective: any = "capture_notifications", synchronized_runtime: any = false, sync_memory_path: any = "", sync_memory_key: any = "", sync_tick: any = 0, evolving_runtime: any = false, evolution_memory_path: any = "", evolution_memory_key: any = "", live_runtime: any = false, live_memory_path: any = "", live_memory_key: any = "", live_snapshot: any = null, federated_memory: any = false, federated_memory_path: any = "", federated_memory_key: any = "", execution_runtime: any = false, execution_memory_path: any = "", execution_memory_key: any = "", simulate_execution: any = false, rollback_enabled: any = true, reconstruction_runtime: any = false, reconstruction_memory_path: any = "", reconstruction_memory_key: any = "", fabricate_runtime: any = false, clone_runtime: any = false): any {
  var memory: any = {"accessibility_trees": {}, "windows": {}, "workflows": {}, "runtime_graphs": {}, "electron_state": {}, "terminal_streams": {}, "bounded": true};
  if ((py.truthy(persistent_runtime) && py.truthy(runtime_path) && py.truthy(runtime_key))) {
    var loaded: any = loadNativeRuntime(runtime_path, runtime_key);
    if (py.truthy(py.get(loaded, "available"))) {
      memory = py.get(loaded, "runtime", memory);
    }
  }
  var snap: any = snapshot;
  var terminal: any = null;
  var vm: any = null;
  var remote: any = null;
  var electron: any = null;
  if (py.eq(runtime, "terminal")) {
    terminal = captureTerminalRuntime(undefined, snap);
    var cognition: any = runNativeCognition(runtime, application, py.or2(snap, () => ({"output": ["$"], "commands": [], "prompts": ["$"]})), memory, interactions, application_cognition, adaptive_runtime, application_memory);
  } else if (py.eq(runtime, "electron")) {
    cognition = runNativeCognition(runtime, application, snap, memory, interactions, application_cognition, adaptive_runtime, application_memory);
    electron = py.get(cognition, "electron");
  } else if (py.eq(runtime, "vm")) {
    vm = extractVmRuntime(undefined, snap);
    cognition = runNativeCognition(runtime, application, {"vm": py.or2(snap, () => ({}))}, memory, interactions, application_cognition);
  } else if (py.eq(runtime, "remote")) {
    remote = extractRemoteRuntime(py.get(py.or2(snap, () => ({})), "protocol", "ssh"), snap);
    cognition = runNativeCognition(runtime, application, {"remote": py.or2(snap, () => ({})), "remote_protocol": "ssh"}, memory, interactions, application_cognition);
  } else {
    cognition = runNativeCognition("desktop", application, snap, memory, interactions, application_cognition, adaptive_runtime, application_memory);
  }
  var runtime_persisted: any = false;
  if ((py.truthy(persistent_runtime) && py.truthy(runtime_path) && py.truthy(runtime_key))) {
    saveNativeRuntime(runtime_path, py.get(cognition, "memory", {}), runtime_key);
    runtime_persisted = true;
  }
  var native_ir: any = py.get(cognition, "native_ir", {});
  var runtime_irs: any = [nativeRuntimeIrToGraph(native_ir)];
  var causality_result: any = {"enabled": false, "bounded": true};
  var causal_ir: any = {"ir": "causal_runtime", "bounded": true};
  var causal_memory_persisted: any = false;
  var semantic_result: any = {"enabled": false, "bounded": true};
  var semantic_ir: any = {"ir": "semantic_runtime", "bounded": true};
  var semantic_memory_persisted: any = false;
  var workflow_result: any = {"enabled": false, "bounded": true};
  var workflow_ir: any = {"ir": "workflow_runtime", "bounded": true};
  var workflow_memory_persisted: any = false;
  var sync_result: any = {"enabled": false, "bounded": true};
  var sync_ir: any = {"ir": "synchronization_runtime", "bounded": true};
  var sync_memory_persisted: any = false;
  var evolution_result: any = {"enabled": false, "bounded": true};
  var evolution_ir: any = {"ir": "evolution_runtime", "bounded": true};
  var evolution_memory_persisted: any = false;
  var live_result: any = {"enabled": false, "bounded": true};
  var live_ir: any = {"ir": "live_runtime", "bounded": true};
  var live_memory_persisted: any = false;
  var memory_result: any = {"enabled": false, "bounded": true};
  var memory_ir: any = {"ir": "runtime_memory", "bounded": true};
  var federated_memory_persisted: any = false;
  var execution_result: any = {"enabled": false, "bounded": true};
  var execution_ir: any = {"ir": "execution_runtime", "bounded": true};
  var execution_persisted: any = false;
  var reconstruction_result: any = {"enabled": false, "bounded": true};
  var reconstruction_ir: any = {"ir": "reconstruction_runtime", "bounded": true};
  var reconstruction_persisted: any = false;
  if (py.truthy(causality_runtime)) {
    causality_result = runCausalityForExtraction(true, causal_memory_path, causal_memory_key, undefined, cognition, undefined, undefined, interactions, false);
    causal_ir = py.get(causality_result, "causal_ir", causal_ir);
    causal_memory_persisted = py.get(causality_result, "memory_persisted", false);
    py.listAppend(runtime_irs, causalRuntimeIrToGraph(causal_ir));
  }
  if (py.truthy(semantic_runtime)) {
    semantic_result = runSemanticForExtraction(true, semantic_memory_path, semantic_memory_key, undefined, undefined, interactions, undefined, causality_result, cognition, undefined, undefined, false);
    semantic_ir = py.get(semantic_result, "semantic_ir", semantic_ir);
    semantic_memory_persisted = py.get(semantic_result, "memory_persisted", false);
    py.listAppend(runtime_irs, semanticRuntimeIrToGraph(semantic_ir));
  }
  if (py.truthy(autonomous_workflow)) {
    workflow_result = runWorkflowForExtraction(true, workflow_objective, workflow_memory_path, workflow_memory_key, undefined, semantic_result, causality_result, undefined, undefined, cognition, false);
    workflow_ir = py.get(workflow_result, "workflow_ir", workflow_ir);
    workflow_memory_persisted = py.get(workflow_result, "memory_persisted", false);
    py.listAppend(runtime_irs, workflowRuntimeIrToGraph(workflow_ir));
  }
  if (py.truthy(synchronized_runtime)) {
    sync_result = runSyncForExtraction(true, sync_memory_path, sync_memory_key, sync_tick, undefined, cognition, semantic_result, workflow_result, causality_result, undefined, undefined, undefined, false);
    sync_ir = py.get(sync_result, "sync_ir", sync_ir);
    sync_memory_persisted = py.get(sync_result, "memory_persisted", false);
    py.listAppend(runtime_irs, synchronizationRuntimeIrToGraph(sync_ir));
  }
  if (py.truthy(evolving_runtime)) {
    evolution_result = runEvolutionForExtraction(true, evolution_memory_path, evolution_memory_key, undefined, workflow_result, semantic_result, sync_result, undefined, undefined, sync_tick, false);
    evolution_ir = py.get(evolution_result, "evolution_ir", evolution_ir);
    evolution_memory_persisted = py.get(evolution_result, "memory_persisted", false);
    py.listAppend(runtime_irs, evolutionRuntimeIrToGraph(evolution_ir));
  }
  if (py.truthy(live_runtime)) {
    live_result = runLiveForExtraction(true, live_memory_path, live_memory_key, undefined, live_snapshot, sync_tick, false);
    live_ir = py.get(live_result, "live_ir", live_ir);
    live_memory_persisted = py.get(live_result, "memory_persisted", false);
    py.listAppend(runtime_irs, liveRuntimeIrToGraph(live_ir));
  }
  if (py.truthy(federated_memory)) {
    memory_result = runMemoryForExtraction(true, federated_memory_path, federated_memory_key, {"workflow": workflow_result, "semantic": semantic_result, "sync": sync_result, "evolution": evolution_result, "live": live_result}, undefined, sync_tick, false);
    memory_ir = py.get(memory_result, "memory_ir", memory_ir);
    federated_memory_persisted = py.get(memory_result, "memory_persisted", false);
    py.listAppend(runtime_irs, runtimeMemoryIrToGraph(memory_ir));
  }
  if (py.truthy(execution_runtime)) {
    var exec_runtime: any = (py.contains(["terminal", "vm", "remote", "electron"], runtime) ? runtime : "native");
    execution_result = runExecutionForExtraction(true, execution_memory_path, execution_memory_key, {"workflow": workflow_result, "semantic": semantic_result, "sync": sync_result, "evolution": evolution_result, "live": live_result, "memory": memory_result}, undefined, exec_runtime, sync_tick, simulate_execution, rollback_enabled, false);
    execution_ir = py.get(execution_result, "execution_ir", execution_ir);
    execution_persisted = py.get(execution_result, "execution_persisted", false);
    py.listAppend(runtime_irs, executionRuntimeIrToGraph(execution_ir));
  }
  if (py.truthy(reconstruction_runtime)) {
    var recon_type: any = (py.contains(["terminal", "vm", "remote", "electron"], runtime) ? runtime : "native");
    reconstruction_result = runReconstructionForExtraction(true, reconstruction_memory_path, reconstruction_memory_key, {"semantic_ir": semantic_ir, "workflow_ir": workflow_ir, "sync_ir": sync_ir, "execution_ir": execution_ir, "memory_ir": memory_ir, "application": cognition, "native_ir": native_ir}, undefined, recon_type, sync_tick, fabricate_runtime, clone_runtime, false);
    reconstruction_ir = py.get(reconstruction_result, "reconstruction_ir", reconstruction_ir);
    reconstruction_persisted = py.get(reconstruction_result, "reconstruction_persisted", false);
    py.listAppend(runtime_irs, reconstructionRuntimeIrToGraph(reconstruction_ir));
  }
  var unified_graph: Record<string, any> = {};
  if (py.truthy(merge_runtime_graph)) {
    unified_graph = buildRuntimeGraph(runtime_irs);
  }
  var replay: any = replayNativeRuntime(py.get(cognition, "memory", {}));
  return {"runtime": runtime, "application": application, "cognition": cognition, "native_ir": native_ir, "unified_graph": unified_graph, "replay": replay, "terminal": py.or2(terminal, () => (py.get(cognition, "terminal"))), "electron": py.or2(electron, () => (py.get(cognition, "electron"))), "vm": py.or2(vm, () => (py.get(cognition, "vm"))), "remote": py.or2(remote, () => (py.get(cognition, "remote"))), "runtime_persisted": runtime_persisted, "causality_runtime": causality_result, "causal_ir": causal_ir, "causal_memory_persisted": causal_memory_persisted, "semantic_runtime": semantic_result, "semantic_ir": semantic_ir, "semantic_memory_persisted": semantic_memory_persisted, "autonomous_workflow": workflow_result, "workflow_ir": workflow_ir, "workflow_memory_persisted": workflow_memory_persisted, "synchronized_runtime": sync_result, "sync_ir": sync_ir, "sync_memory_persisted": sync_memory_persisted, "evolving_runtime": evolution_result, "evolution_ir": evolution_ir, "evolution_memory_persisted": evolution_memory_persisted, "live_runtime": live_result, "live_ir": live_ir, "live_memory_persisted": live_memory_persisted, "federated_memory": memory_result, "memory_ir": memory_ir, "federated_memory_persisted": federated_memory_persisted, "execution_runtime": execution_result, "execution_ir": execution_ir, "execution_persisted": execution_persisted, "reconstruction_runtime": reconstruction_result, "reconstruction_ir": reconstruction_ir, "reconstruction_persisted": reconstruction_persisted, "bounded": true};
}
export { alignNativeRuntime, buildDesktopRuntime, buildInteractionSequence, buildNativeNavigation, buildNativeState, buildNativeUiGraph, buildRuntimeGraph, captureNativeStreams, captureTerminalRuntime, causalRuntimeIrToGraph, compileNativeRuntimeIr, enumerateNativeProcesses, evolutionRuntimeIrToGraph, executionRuntimeIrToGraph, extractAccessibilityTree, extractElectronCdp, extractElectronIpc, extractElectronRoutes, extractElectronRuntime, extractElectronStorage, extractLinuxAtspiSnapshot, extractMacosAxSnapshot, extractNativeWindows, extractRemoteRuntime, extractVmRuntime, extractWindowsUiaSnapshot, liveRuntimeIrToGraph, loadNativeRuntime, nativeRuntimeIrToGraph, reconstructionRuntimeIrToGraph, rememberNativeRuntime, replayNativeRuntime, resolveNativeFocus, runApplicationCognition, runCausalityForExtraction, runEvolutionForExtraction, runExecutionForExtraction, runLiveForExtraction, runMemoryForExtraction, runReconstructionForExtraction, runSemanticForExtraction, runSyncForExtraction, runWorkflowForExtraction, runtimeMemoryIrToGraph, saveNativeRuntime, semanticRuntimeIrToGraph, stableElectronRuntimeHash, synchronizationRuntimeIrToGraph, workflowRuntimeIrToGraph };
