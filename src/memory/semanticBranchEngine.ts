/**
 * Converted from Python: core/memory/semantic_branch_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_BRANCHES: any = 32;
export function branchSemanticState(state: any, branch_id: any): any {
  return {"branch_id": branch_id, "state": state, "deterministic": true};
}
export function listBranches(branches: any): any {
  return py.slice(py.sorted(branches, {key: ((b: any) => py.toStr(py.get(b, "branch_id", ""))) as (item: any) => any}), null, MAX_BRANCHES);
}
