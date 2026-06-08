/**
 * Converted from Python: core/internet/corroboration_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { corroborateSources } from "./sourceCorroborationEngine.js";

export function buildCorroborationGraph(sources: any): any {
  var corr: any = corroborateSources(sources);
  var nodes: any = py.sorted(py.toSet(py.iter(py.or2(sources, () => ([]))).filter((s: any) => py.truthy(s)).map((s: any) => py.toStr(py.get(s, "url", py.get(s, "id", ""))))));
  var edges: any = py.range(py.max([0, py.sub(py.len(nodes), 1)])).map((i: any) => ({"from": py.at(nodes, i), "to": py.at(nodes, py.add(i, 1)), "relation": "corroborates"}));
  return {"nodes": nodes, "edges": edges, "corroboration": corr, "evidence": ["internet:corroboration"]};
}
export { corroborateSources };
