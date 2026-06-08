/**
 * Converted from Python: core/runtime/distributed_partition_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export function partitionRuntimeGraph(nodes: any): any {
  var partitions: Record<string, any> = {};
  var node: any;
  for (node of py.iter(nodes)) {
    var region: any = py.get(node, "region", "default");
    py.listAppend(py.setdefault(partitions, region, []), node);
  }
  return {"partitions": partitions, "count": py.len(partitions)};
}
