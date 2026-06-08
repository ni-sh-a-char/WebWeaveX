/**
 * Converted from Python: core/ir/execution_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { compileRepositoryIr } from "./repositoryIr.js";

export let ExecutionIR: any = py.at(Object, [py.toStr, Object]);
export function compileExecutionIr(source: any, path: any = ""): any {
  var repo: any = compileRepositoryIr(source, path);
  return {"flows": py.get(repo, "execution_flows", []), "topology": py.get(repo, "topology", []), "services": py.get(repo, "services", []), "evidence": py.get(repo, "semantic_evidence", {}), "lineage": py.get(repo, "lineage", {}), "confidence": py.get(repo, "confidence", {})};
}
export { compileRepositoryIr };
