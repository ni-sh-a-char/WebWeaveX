/**
 * Converted from Python: core/distributed/distributed_work_stealing_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function balanceSemanticWorkloads(workloads: any): any {
  var ordered_nodes: any = py.sorted(py.keys(workloads));
  var total: any = py.sum(py.values(workloads).map((v: any) => py.len(v)));
  var target: any = py.max([1, py.floordiv(total, py.max([1, py.len(ordered_nodes)]))]);
  var balanced: Record<string, any> = {};
  var overflow: any[] = [];
  var node: any;
  for (node of py.iter(ordered_nodes)) {
    var tasks: any = [...py.iter(py.at(workloads, node))];
    while ((py.len(tasks) > target)) {
      py.listAppend(overflow, py.pop(tasks));
    }
    py.setItem(balanced, node, tasks);
  }
  for (node of py.iter(ordered_nodes)) {
    while (((py.len(py.at(balanced, node)) < target) && py.truthy(overflow))) {
      py.listAppend(py.at(balanced, node), py.pop(overflow));
    }
  }
  return {"balanced": balanced, "deterministic": true};
}
