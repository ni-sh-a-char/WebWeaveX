/**
 * Converted from Python: core/repository/deployment_semantics_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { modelInfraRelationships } from "./infraRelationshipEngine.js";

export function analyzeDeploymentSemantics(files: any): any {
  var infra: any = modelInfraRelationships(files);
  var deploy_files: any = py.iter(files).filter((f: any) => py.any(py.iter(["docker", "k8s", "helm", "deploy", "workflow"]).map((k: any) => py.contains(String(py.replace(f, "\\", "/")).toLowerCase(), k)))).map((f: any) => f);
  return {"deployment_artifacts": deploy_files, "infra": infra, "semantics": (py.truthy(deploy_files) ? "container_orchestration" : "unknown"), "evidence": py.add(py.get(infra, "evidence", []), [`deploy:${py.toStr(py.len(deploy_files))}`])};
}
export { modelInfraRelationships };
