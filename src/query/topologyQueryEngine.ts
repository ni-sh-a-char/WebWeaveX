/**
 * Converted from Python: core/query/topology_query_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { traverseGraph } from "./semanticTraversalEngine.js";

export function queryTopology(adjacency: any, start: any): any {
  var order: any = traverseGraph(adjacency, start);
  return {"order": order, "count": py.len(order), "deterministic": true, "bounded": true};
}
export { traverseGraph };
