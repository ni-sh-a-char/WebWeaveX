/**
 * Converted from Python: core/query_language/semantic_query_executor.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_RESULTS: any = 1000;
export function executeSemanticPlan(plan: any, dataset: any): any {
  var results: any[] = [];
  var filters: Record<string, any> = {};
  var step: any;
  for (step of py.iter(py.get(plan, "steps", []))) {
    if (py.eq(py.get(step, "operation"), "scan")) {
      filters = py.get(step, "filters", {});
    }
  }
  var limit: any = py.min([py.get(plan, "limit", MAX_RESULTS), MAX_RESULTS]);
  var item: any;
  for (item of py.iter(dataset)) {
    var matched: any = true;
    var key: any;
    var value: any;
    for ([key, value] of py.items(filters)) {
      if (!py.eq(py.toStr(py.get(item, key)), py.toStr(value))) {
        matched = false;
        break;
      }
    }
    if (py.truthy(matched)) {
      py.listAppend(results, item);
    }
    if ((py.len(results) >= limit)) {
      break;
    }
  }
  return {"results": results, "count": py.len(results)};
}
