/**
 * Converted from Python: core/query_language/semantic_query_ast.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildQueryAst(parsed: any): any {
  return {"type": "semantic_query", "select": py.get(parsed, "select", []), "where": py.get(parsed, "where", {}), "limit": py.get(parsed, "limit", 100)};
}
