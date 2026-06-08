/**
 * Converted from Python: core/query_language/semantic_query_optimizer.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function optimizeSemanticQuery(plan: any): any {
  var optimized_steps: any = py.sorted(py.get(plan, "steps", []), {key: ((x: any) => py.get(x, "operation", "")) as (item: any) => any});
  return {"steps": optimized_steps, "limit": py.get(plan, "limit", 100), "optimized": true};
}
