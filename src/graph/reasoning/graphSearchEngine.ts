/**
 * Converted from Python: core/graph/reasoning/graph_search_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";
import { nodeIds } from "./_helpers.js";

export function graphSearch(graph: any, query: any): any {
  var q: any = String(py.or2(query, () => (""))).toLowerCase();
  var nodes: any = py.iter(nodeIds(graph)).filter((n: any) => py.contains(String(n).toLowerCase(), q)).map((n: any) => n);
  var edges: any = py.iter(py.get(py.or2(graph, () => ({})), "edges", [])).filter((e: any) => (((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map))) && py.contains(String(`${py.toStr(py.get(e, "from", ""))}${py.toStr(py.get(e, "to", ""))}`).toLowerCase(), q))).map((e: any) => e);
  return {"nodes": py.sorted(py.toSet(nodes)), "edges": py.sorted(edges, {key: ((e: any) => [py.get(e, "from", ""), py.get(e, "to", "")]) as (item: any) => any})};
}
export { nodeIds };
