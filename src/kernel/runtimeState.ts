/**
 * Converted from Python: core/kernel/runtime_state.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildKernelState(context: any, irs: any = null, graph: any = null): any {
  return {"context": py.pyDict(context), "irs": [...py.iter(py.or2(irs, () => ([])))], "graph": py.pyDict(py.or2(graph, () => ({}))), "tick": py.toInt(py.get(context, "tick", 0)), "bounded": true};
}
export function mergeKernelState(prior: any, update: any): any {
  var merged: any = py.pyDict(prior);
  py.update(merged, update);
  py.setItem(merged, "irs", py.add([...py.iter(py.get(prior, "irs", []))], [...py.iter(py.get(update, "irs", []))]));
  return merged;
}
