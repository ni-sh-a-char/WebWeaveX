/**
 * Converted from Python: core/repository/infra_execution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let INFRA_KEYWORDS: any = py.toSet(new Set(["docker", "kubernetes", "terraform", "helm", "compose"]));
export function inferInfraExecution(dependencies: any, parser_evidence: any): any {
  var observed: any = py.sorted(py.iter(dependencies).filter((dep: any) => py.contains(INFRA_KEYWORDS, String(dep).toLowerCase())).map((dep: any) => dep));
  return {"infra": observed, "evidence": py.sorted(py.toSet(parser_evidence)), "grounded": py.truthy(parser_evidence), "deterministic": true};
}
