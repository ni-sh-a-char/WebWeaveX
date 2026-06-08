/**
 * Converted from Python: core/repository/deployment_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let DEPLOY_KEYWORDS: any = py.toSet(new Set(["dockerfile", "docker-compose", "helm", "k8s", "kubernetes"]));
export function inferDeploymentRuntime(artifacts: any, parser_evidence: any): any {
  var found: any = py.sorted(py.iter(artifacts).filter((a: any) => py.any(py.iter(DEPLOY_KEYWORDS).map((k: any) => py.contains(String(a).toLowerCase(), k)))).map((a: any) => a));
  return {"artifacts": found, "evidence": py.sorted(py.toSet(parser_evidence)), "grounded": py.truthy(parser_evidence), "deterministic": true};
}
