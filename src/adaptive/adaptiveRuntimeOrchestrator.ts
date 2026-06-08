/**
 * Converted from Python: core/adaptive/adaptive_runtime_orchestrator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildAdaptiveRuntimeGraph } from "./adaptiveRuntimeGraphEngine.js";
import { buildAdaptiveSnapshot } from "./adaptiveSnapshotEngine.js";
import { rememberExtractionRuntime } from "./extractionMemoryEngine.js";
import { runRuntimeAdaptation } from "./runtimeAdaptationEngine.js";
import { reconcileRuntimeState } from "./runtimeReconciliationEngine.js";
import { stabilizeExtractionSchema } from "./schemaStabilityEngine.js";

export function runAdaptiveExtraction(url: any, dom: any, html: any, extraction: any, interactions: any = null, memory: any = null, primary_selector: any = "body", page: any = null, stream_state: any = null, identity_state: any = null, pagination_state: any = null): any {
  var dom_nodes: any = [...py.iter(py.get(dom, "nodes", []))];
  interactions = [...py.iter(py.or2(interactions, () => ([])))];
  memory = py.pyDict(py.or2(memory, () => ({})));
  var adaptation: any = runRuntimeAdaptation(url, dom_nodes, html, interactions, primary_selector, page);
  var schema: any = stabilizeExtractionSchema(extraction);
  var reconciliation: any = reconcileRuntimeState({"available": true, "url": url}, py.or2(stream_state, () => ({})), py.get(adaptation, "interaction_recovery", {}), schema);
  var snapshot: any = buildAdaptiveSnapshot(dom, py.get(memory, "selectors", {}), {"interactions": interactions}, py.or2(stream_state, () => ({})), py.or2(identity_state, () => ({})), py.or2(pagination_state, () => (py.get(adaptation, "pagination_recovery", {}))));
  var updated_memory: any = rememberExtractionRuntime(memory, {"selectors": {[py.toStr(primary_selector)]: py.at(py.at(py.at(adaptation, "fallback"), "active"), "selector")}, "healed_selectors": {[py.toStr(primary_selector)]: py.at(py.at(py.at(py.at(adaptation, "fallback"), "chain"), 1), "selector")}, "pagination_patterns": [py.get(py.at(adaptation, "pagination_recovery"), "recovered_selector", "")], "modal_solutions": py.get(py.at(adaptation, "modal_recovery"), "recovered", []), "interaction_chains": py.get(py.at(adaptation, "interaction_recovery"), "interactions", [])});
  var graph: any = buildAdaptiveRuntimeGraph(adaptation);
  return {"adaptation": adaptation, "schema": schema, "reconciliation": reconciliation, "snapshot": snapshot, "memory": updated_memory, "graph": graph, "bounded": true};
}
export { buildAdaptiveRuntimeGraph, buildAdaptiveSnapshot, reconcileRuntimeState, rememberExtractionRuntime, runRuntimeAdaptation, stabilizeExtractionSchema };
