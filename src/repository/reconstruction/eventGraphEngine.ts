/**
 * Converted from Python: core/repository/reconstruction/event_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function buildEventGraph(text: any): any {
  var src: any = String(py.or2(text, () => (""))).toLowerCase();
  var producers: any = py.sorted(py.toSet(py.iter(["publish", "emit", "producer", "kafka", "sns"]).filter((k: any) => py.contains(src, k)).map((k: any) => k)));
  var consumers: any = py.sorted(py.toSet(py.iter(["consume", "subscriber", "handler", "worker", "sqs"]).filter((k: any) => py.contains(src, k)).map((k: any) => k)));
  var nodes: any = py.sorted(py.toSet(py.add(producers, consumers)));
  var edges: any = py.iter(producers).flatMap((p: any) => py.iter(py.slice(consumers, null, 5)).map((c: any) => ({"from": p, "to": c})));
  return {"nodes": nodes, "edges": py.sorted(edges, {key: ((e: any) => [py.at(e, "from"), py.at(e, "to")]) as (item: any) => any})};
}
