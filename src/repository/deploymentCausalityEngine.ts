/**
 * Converted from Python: core/repository/deployment_causality_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { analyzeDeploymentSemantics } from "./deploymentSemanticsEngine.js";

export function modelDeploymentCausality(files: any): any {
  var deploy: any = analyzeDeploymentSemantics(files);
  var causal: any = py.iter(py.slice(py.get(deploy, "deployment_artifacts", []), null, 30)).map((a: any) => ({"artifact": a, "causes": "deploy"}));
  return {"causal": causal, "semantics": py.get(deploy, "semantics"), "evidence": py.get(py.get(deploy, "infra", {}), "evidence", [])};
}
export { analyzeDeploymentSemantics };
