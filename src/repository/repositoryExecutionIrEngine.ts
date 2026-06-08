/**
 * Converted from Python: core/repository/repository_execution_ir_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { reasonApiContract } from "./apiContractReasoningEngine.js";
import { analyzeDeploymentSemantics } from "./deploymentSemanticsEngine.js";
import { buildRepositorySemanticIr } from "./repositorySemanticIrEngine.js";
import { reasonRuntimeFlow } from "./runtimeFlowReasoner.js";
import { buildServiceRuntimeGraph } from "./serviceRuntimeGraphEngine.js";

export function buildRepositoryExecutionIr(source: any, path: any = "", files: any = null, openapi_spec: any = null): any {
  var base: any = buildRepositorySemanticIr(source, path, files);
  var flow: any = reasonRuntimeFlow(source, path, files);
  var services: any = buildServiceRuntimeGraph(source, path, files);
  var deploy: any = analyzeDeploymentSemantics(py.or2(files, () => ([])));
  var api: any = (py.truthy(openapi_spec) ? reasonApiContract(py.or2(openapi_spec, () => ({}))) : {});
  return {...(base), "execution": flow, "services": services, "deployment": deploy, "api_contracts": api, "evidence": py.sorted(py.toSet(py.iter(py.add([...py.iter(py.or2(py.get(base, "evidence"), () => ([])))], [...py.iter(py.or2(py.get(flow, "evidence"), () => ([])))])).filter((e: any) => py.truthy(e)).map((e: any) => py.toStr(e))))};
}
export { analyzeDeploymentSemantics, buildRepositorySemanticIr, buildServiceRuntimeGraph, reasonApiContract, reasonRuntimeFlow };
