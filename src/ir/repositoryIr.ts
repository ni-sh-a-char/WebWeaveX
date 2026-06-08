/**
 * Converted from Python: core/ir/repository_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { emptyConfidence, emptyLineage, mergeEvidence } from "./_base.js";
import { compileSemanticAstIr } from "../ast/index.js";
import { buildRepositoryExecutionIr } from "../repository/repositoryExecutionIrEngine.js";

export let RepositoryIR: any = py.at(Object, [py.toStr, Object]);
export function emptyRepositoryIr(): any {
  return {"services": [], "runtimes": [], "dependencies": [], "events": [], "queues": [], "apis": [], "deployments": [], "infra": [], "execution_flows": [], "topology": [], "runtime_constraints": [], "semantic_evidence": {}, "graph": {}, "lineage": emptyLineage("repository_ir"), "confidence": emptyConfidence()};
}
export function compileRepositoryIr(source: any = "", path: any = "", files: any = null, openapi_spec: any = null): any {
  var raw: any = buildRepositoryExecutionIr(source, path, files, openapi_spec);
  var deps: any = py.or2(py.get(raw, "runtime_dependencies", {}), () => ({}));
  var flow: any = py.or2(py.get(raw, "execution", {}), () => ({}));
  var services: any = py.or2(py.get(raw, "services", {}), () => ({}));
  var deploy: any = py.or2(py.get(raw, "deployment", {}), () => ({}));
  var api: any = py.or2(py.get(raw, "api_contracts", {}), () => ({}));
  var ir: any = emptyRepositoryIr();
  py.setItem(ir, "dependencies", py.get(deps, "dependencies", []));
  py.setItem(ir, "runtimes", [{"language": py.get(raw, "language", "text"), "evidence": py.get(deps, "evidence", [])}]);
  py.setItem(ir, "execution_flows", py.get(py.get(flow, "execution_flow", {}), "flow", []));
  py.setItem(ir, "services", py.get(services, "nodes", []));
  py.setItem(ir, "topology", py.get(py.get(flow, "topology", {}), "edges", []));
  py.setItem(ir, "deployments", py.get(deploy, "deployment_artifacts", []));
  py.setItem(ir, "infra", py.iter(py.get(py.get(deploy, "infra", {}), "signals", [])).filter((s: any) => ((s !== null && typeof s === "object" && !Array.isArray(s) && !(s instanceof Set) && !(s instanceof Map)))).map((s: any) => py.get(s, "file")));
  py.setItem(ir, "apis", py.get(api, "contracts", []));
  py.setItem(ir, "graph", {"nodes": py.get(services, "nodes", []), "edges": py.get(services, "edges", [])});
  py.setItem(ir, "semantic_evidence", mergeEvidence(py.get(raw, "evidence", [])));
  py.setItem(ir, "lineage", emptyLineage("repository_execution_ir"));
  py.setItem(ir, "confidence", {"score": (py.truthy(py.get(deps, "parser_first")) ? py.F(0.8) : py.F(0.4)), "basis": py.get(raw, "evidence", []), "deterministic": true});
  try {
    var semantic_ast: any = compileSemanticAstIr(py.or2(source, () => ("")));
  } catch (_e: any) {
    semantic_ast = {"semantic_grounded": false, "deterministic": true};
  }
  py.setItem(ir, "semantic_ast", semantic_ast);
  py.setItem(ir, "_raw", raw);
  return ir;
}
export { buildRepositoryExecutionIr, compileSemanticAstIr, emptyConfidence, emptyLineage, mergeEvidence };
