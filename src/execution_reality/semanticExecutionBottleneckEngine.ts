/**
 * Converted from Python: core/execution_reality/semantic_execution_bottleneck_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_BOTTLENECKS: any = 1000;
export let BOTTLENECK_THRESHOLD: any = 3;
export function detectExecutionBottlenecks(runtime_ir: any): any {
  var topology: any = py.get(runtime_ir, "distributed_topology", {});
  var edges: any = py.get(topology, "edges", []);
  var inbound: Record<string, any> = {};
  var edge: any;
  for (edge of py.iter(edges)) {
    var target: any = py.toStr(py.get(edge, "to"));
    py.setItem(inbound, target, py.add(py.get(inbound, target, 0), 1));
  }
  var bottlenecks: any[] = [];
  var node: any;
  var degree: any;
  for ([node, degree] of py.items(inbound)) {
    if (py.ge(degree, BOTTLENECK_THRESHOLD)) {
      py.listAppend(bottlenecks, {"node": node, "pressure": degree});
    }
  }
  return {"bottlenecks": py.slice(py.sorted(bottlenecks, {key: ((x: any) => [(-py.at(x, "pressure")), py.at(x, "node")]) as (item: any) => any}), null, MAX_BOTTLENECKS)};
}
