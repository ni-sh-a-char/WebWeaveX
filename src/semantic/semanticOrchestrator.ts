/**
 * Converted from Python: core/semantic/semantic_orchestrator.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { compileSemanticRuntimeIr, semanticRuntimeIrToGraph } from "../ir/semanticRuntimeIr.js";
import { extractApplicationSemantics } from "./applicationSemanticsEngine.js";
import { extractBrowserSemantics } from "./browserSemanticsEngine.js";
import { extractCausalitySemantics } from "./causalitySemanticsEngine.js";
import { extractDocumentSemantics } from "./documentSemanticsEngine.js";
import { classifySemanticDomain } from "./domainClassificationEngine.js";
import { extractSemanticEntities } from "./entityExtractionEngine.js";
import { resolveSemanticEntities } from "./entityResolutionEngine.js";
import { buildSemanticOntology } from "./ontologyEngine.js";
import { extractRepositorySemantics } from "./repositorySemanticsEngine.js";
import { extractRuntimeSemantics } from "./runtimeSemanticsEngine.js";
import { alignSemanticRuntimes } from "./semanticAlignmentEngine.js";
import { diffSemanticRuntime } from "./semanticDiffEngine.js";
import { buildSemanticGraph } from "./semanticGraphEngine.js";
import { loadSemanticMemory } from "./semanticMemoryEngine.js";
import { rememberSemanticRuntime } from "./semanticMemoryEngine.js";
import { saveSemanticMemory } from "./semanticMemoryEngine.js";
import { replaySemanticRuntime } from "./semanticReplayEngine.js";
import { extractTableSemantics } from "./tableSemanticsEngine.js";
import { extractUiSemantics } from "./uiSemanticsEngine.js";
import { extractWorkflowSemantics } from "./workflowSemanticsEngine.js";
import { buildRuntimeGraph } from "../runtime_graph/runtimeGraphEngine.js";

export function runSemanticRuntime(url: any = "", html: any = "", text: any = "", interactions: any = null, application_result: any = null, causality_result: any = null, native_cognition: any = null, repository_files: any = null, runtime_graph: any = null, memory: any = null, objective: any = ""): any {
  memory = py.pyDict(py.or2(memory, () => ({})));
  interactions = [...py.iter(py.or2(interactions, () => ([])))];
  var combined_text: any = py.slice(`${py.toStr(text)} ${py.toStr(html)}`, null, 100000);
  var structure: any = {"actions": py.iter(interactions).map((ix: any) => ({"label": py.get(ix, "action", ""), "type": py.get(ix, "action", "")})), "artifacts": (py.truthy(native_cognition) ? [py.toStr(py.get(native_cognition, "runtime", ""))] : [])};
  var entities_raw: any = extractSemanticEntities(combined_text, structure);
  var resolved: any = resolveSemanticEntities(py.at(entities_raw, "entities"));
  py.setItem(entities_raw, "entities", py.at(resolved, "entities"));
  var domain: any = classifySemanticDomain(combined_text, (py.truthy(objective) ? [objective] : []));
  var ontology: any = buildSemanticOntology(py.at(entities_raw, "entities"), py.at(domain, "domain"));
  py.setItem(entities_raw, "ontology", ontology);
  var ui: any = extractUiSemantics(html, interactions);
  var tables: any = extractTableSemantics(html);
  var document: any = extractDocumentSemantics(combined_text);
  var repository: any = extractRepositorySemantics(repository_files, combined_text);
  var application: any = extractApplicationSemantics(application_result);
  var causality: any = extractCausalitySemantics(causality_result);
  var workflow: any = extractWorkflowSemantics(py.get(py.or2(application_result, () => ({})), "workflow"), objective);
  var browser: any = extractBrowserSemantics(url, html);
  var runtime: any = extractRuntimeSemantics(runtime_graph, {"browser": py.truthy(browser), "native": py.truthy(native_cognition), "application": py.truthy(application_result)});
  var semantic_graph: any = buildSemanticGraph(py.at(entities_raw, "entities"), py.at(entities_raw, "relations"));
  var alignment: any = alignSemanticRuntimes({...(browser), "domain": py.at(domain, "domain")}, native_cognition, repository, document, undefined, runtime);
  var diff: Record<string, any> = {};
  if (py.truthy(py.get(memory, "entities"))) {
    diff = diffSemanticRuntime(memory, {"entities": entities_raw, "domain": domain, "ontology": ontology, "workflow": workflow});
  }
  var payload: any = {"entities": entities_raw, "domain": domain, "ontology": ontology, "ui": ui, "tables": tables, "document": document, "repository": repository, "application": application, "causality": causality, "workflow": workflow, "browser": browser, "runtime": runtime, "semantic_graph": semantic_graph, "alignment": alignment, "diff": diff, "bounded": true};
  var updated_memory: any = rememberSemanticRuntime(memory, {"ontology": ontology, "semantic_graph": semantic_graph, "entity_mappings": py.get(resolved, "canonical_map", {}), "semantic_workflows": workflow, "runtime_semantics": runtime, "entities": entities_raw, "domain": domain});
  py.setItem(payload, "memory", updated_memory);
  py.setItem(payload, "replay", replaySemanticRuntime(updated_memory));
  py.setItem(payload, "semantic_ir", compileSemanticRuntimeIr(payload));
  return payload;
}
export function runSemanticForExtraction(semantic_runtime: any = true, memory_path: any = "", memory_key: any = "", url: any = "", html: any = "", interactions: any = null, application_result: any = null, causality_result: any = null, native_cognition: any = null, runtime_graph: any = null, objective: any = "", merge_graph: any = true): any {
  if (!py.truthy(semantic_runtime)) {
    return {"enabled": false, "bounded": true};
  }
  var memory: Record<string, any> = {};
  if ((py.truthy(memory_path) && py.truthy(memory_key))) {
    var loaded: any = loadSemanticMemory(memory_path, memory_key);
    if (py.truthy(py.get(loaded, "available"))) {
      memory = py.get(loaded, "memory", memory);
    }
  }
  var result: any = runSemanticRuntime(url, html, undefined, interactions, application_result, causality_result, native_cognition, undefined, runtime_graph, memory, objective);
  var persisted: any = false;
  if ((py.truthy(memory_path) && py.truthy(memory_key))) {
    saveSemanticMemory(memory_path, py.get(result, "memory", {}), memory_key);
    persisted = true;
  }
  var graph_ir: any = semanticRuntimeIrToGraph(py.get(result, "semantic_ir", {}));
  var unified_graph: Record<string, any> = {};
  if (py.truthy(merge_graph)) {
    unified_graph = buildRuntimeGraph([graph_ir]);
  }
  return {"enabled": true, "semantic": result, "semantic_ir": py.get(result, "semantic_ir", {}), "semantic_graph_ir": graph_ir, "unified_graph": unified_graph, "replay": py.get(result, "replay", {}), "memory_persisted": persisted, "bounded": true};
}
export { alignSemanticRuntimes, buildRuntimeGraph, buildSemanticGraph, buildSemanticOntology, classifySemanticDomain, compileSemanticRuntimeIr, diffSemanticRuntime, extractApplicationSemantics, extractBrowserSemantics, extractCausalitySemantics, extractDocumentSemantics, extractRepositorySemantics, extractRuntimeSemantics, extractSemanticEntities, extractTableSemantics, extractUiSemantics, extractWorkflowSemantics, loadSemanticMemory, rememberSemanticRuntime, replaySemanticRuntime, resolveSemanticEntities, saveSemanticMemory, semanticRuntimeIrToGraph };
