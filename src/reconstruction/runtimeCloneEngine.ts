/**
 * Converted from Python: core/reconstruction/runtime_clone_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function cloneRuntimeEnvironment(source: any, include_graph: any = true, include_queues: any = true): any {
  var cloned: any = {"runtime_graph": (py.truthy(include_graph) ? py.deepcopy(py.get(source, "runtime_graph", {})) : {}), "browser_state": py.deepcopy(py.get(source, "browser", py.get(source, "browser_state", {}))), "application_state": py.deepcopy(py.get(source, "application", py.get(source, "application_state", {}))), "execution_queues": (py.truthy(include_queues) ? py.deepcopy(py.get(source, "queues", py.get(source, "execution_queues", []))) : []), "synchronization_state": py.deepcopy(py.get(source, "synchronization", py.get(source, "sync", {}))), "workflows": py.deepcopy(py.get(source, "workflows", [])), "source_mutated": false, "cloned": true, "bounded": true};
  return cloned;
}
