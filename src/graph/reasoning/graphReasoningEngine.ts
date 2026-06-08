/**
 * Converted from Python: core/graph/reasoning/graph_reasoning_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function graphReason(graph: any): any {
  var deg: Record<string, any> = {};
  var e: any;
  for (e of py.iter(py.get(py.or2(graph, () => ({})), "edges", []))) {
    if (!((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map)))) {
      continue;
    }
    py.setItem(deg, py.get(e, "from"), py.add(py.get(deg, py.get(e, "from"), 0), 1));
    py.setItem(deg, py.get(e, "to"), py.add(py.get(deg, py.get(e, "to"), 0), 1));
  }
  var hubs: any = py.slice(py.sorted(py.iter(deg).filter((k: any) => py.truthy(k)).map((k: any) => k), {key: ((n: any) => [(-py.at(deg, n)), n]) as (item: any) => any}), null, 20);
  return {"connected": (py.len(py.get(py.or2(graph, () => ({})), "edges", [])) > 0), "hubs": py.iter(hubs).map((h: any) => ({"node": h, "degree": py.at(deg, h)}))};
}
