/**
 * Converted from Python: core/world_model/repository_semantic_search_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_RESULTS: any = 1000;
export function semanticRepositorySearch(query: any, repository_irs: any): any {
  var results: any[] = [];
  var lowered: any = String(query).toLowerCase();
  var ir: any;
  for (ir of py.iter(repository_irs)) {
    var path: any = String(py.toStr(py.get(ir, "path", ""))).toLowerCase();
    if (py.contains(path, lowered)) {
      py.listAppend(results, {"path": py.get(ir, "path")});
    }
  }
  return {"results": py.slice(results, null, MAX_RESULTS), "count": py.len(py.slice(results, null, MAX_RESULTS))};
}
