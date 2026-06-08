/**
 * Converted from Python: core/graph_partition_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./runtime/pyCompat.js";

export function partitionGraph(graph: any, parts: any = 2): any {
  var nodes: any = py.get(graph, "nodes", []);
  var buckets: any = py.range(py.max([1, parts])).map((_: any) => []);
  var i: any;
  var n: any;
  for ([i, n] of py.enumerate(nodes)) {
    py.listAppend(py.at(buckets, py.mod(i, py.len(buckets))), n);
  }
  return {"partitions": buckets};
}
