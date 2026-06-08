/**
 * Converted from Python: core/performance/graph_budget_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function enforceGraphBudget(nodes: any, edges: any, max_nodes: any = 5000, max_edges: any = 20000): any {
  return {"nodes_ok": py.le(nodes, max_nodes), "edges_ok": py.le(edges, max_edges)};
}
