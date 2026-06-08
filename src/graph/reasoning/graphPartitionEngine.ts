/**
 * Converted from Python: core/graph/reasoning/graph_partition_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";
import { nodeIds } from "./_helpers.js";

export function graphPartition(graph: any, partitions: any = 4): any {
  var p: any = py.max([1, py.toInt(partitions)]);
  var nodes: any = nodeIds(graph);
  var out: any = Object.fromEntries(py.range(p).map((i: any) => ([py.toStr(i), []] as [any, any])));
  var i: any;
  var n: any;
  for ([i, n] of py.enumerate(nodes)) {
    py.listAppend(py.at(out, py.toStr(py.mod(i, p))), n);
  }
  return out;
}
export { nodeIds };
