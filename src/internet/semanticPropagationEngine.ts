/**
 * Converted from Python: core/internet/semantic_propagation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function modelSemanticPropagation(seed: any, edges: any, max_hops: any = 5): any {
  var visited: any = new Set([seed]);
  var frontier: any = [seed];
  var hops: any = 0;
  while ((py.truthy(frontier) && py.lt(hops, max_hops))) {
    var next_f: any[] = [];
    var e: any;
    for (e of py.iter(edges)) {
      if ((py.contains(frontier, py.get(e, "from")) && !py.contains(visited, py.get(e, "to")))) {
        py.setAdd(visited, py.toStr(py.at(e, "to")));
        py.listAppend(next_f, py.toStr(py.at(e, "to")));
      }
    }
    frontier = next_f;
    hops = py.add(hops, 1);
  }
  return {"visited": py.sorted(visited), "hops": hops, "bounded": py.le(hops, max_hops)};
}
