/**
 * Converted from Python: core/query_language/semantic_query_planner.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function planSemanticQuery(ast: any): any {
  return {"steps": [{"operation": "scan", "filters": py.get(ast, "where", {})}, {"operation": "project", "fields": py.get(ast, "select", [])}], "limit": py.get(ast, "limit", 100)};
}
