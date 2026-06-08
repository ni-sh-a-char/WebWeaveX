/**
 * Converted from Python: core/graph/graph_partition_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function partitionGraph(graph: any, parts: any = 2): any {
  var nodes: any = (((graph !== null && typeof graph === "object" && !Array.isArray(graph) && !(graph instanceof Set) && !(graph instanceof Map))) ? py.get(graph, "nodes", []) : []);
  var buckets: any = py.range(py.max([1, parts])).map((_: any) => []);
  var i: any;
  var node: any;
  for ([i, node] of py.enumerate(nodes)) {
    if (((node !== null && typeof node === "object" && !Array.isArray(node) && !(node instanceof Set) && !(node instanceof Map)))) {
      py.listAppend(py.at(buckets, py.mod(i, py.len(buckets))), node);
    }
  }
  return {"partitions": buckets, "partition_count": py.len(buckets)};
}
