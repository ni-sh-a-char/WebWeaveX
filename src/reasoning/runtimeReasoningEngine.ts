/**
 * Converted from Python: core/reasoning/runtime_reasoning_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { compileRepositoryIr } from "../ir/repositoryIr.js";
import { modelRuntimeState } from "../repository/runtimeStateEngine.js";

export function reasonRuntimeSemantic(source: any, path: any = ""): any {
  var ir: any = compileRepositoryIr(source, path);
  var state: any = modelRuntimeState(source, path);
  return {"ir": ir, "state": state, "evidence": py.get(ir, "semantic_evidence", {}), "explainable": true};
}
export { compileRepositoryIr, modelRuntimeState };
