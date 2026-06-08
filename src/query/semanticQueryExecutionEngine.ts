/**
 * Converted from Python: core/query/semantic_query_execution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_RESULTS: any = 1000;
export function executeSemanticQuery(nodes: any, filters: any): any {
  var results: any[] = [];
  var node: any;
  for (node of py.iter(nodes)) {
    var match: any = true;
    var key: any;
    var value: any;
    for ([key, value] of py.items(filters)) {
      if (!py.eq(py.get(node, key), value)) {
        match = false;
        break;
      }
    }
    if (py.truthy(match)) {
      py.listAppend(results, node);
    }
    if ((py.len(results) >= MAX_RESULTS)) {
      break;
    }
  }
  return {"results": results, "count": py.len(results)};
}
