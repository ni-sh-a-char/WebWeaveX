/**
 * Converted from Python: core/agents/traversal_query_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function tracePaths(graph: any, start: any): any {
  return py.iter(py.get(graph, "edges", [])).filter((e: any) => py.eq(py.get(e, "from"), start)).map((e: any) => e);
}
