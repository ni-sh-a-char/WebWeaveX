/**
 * Converted from Python: core/workflows/workflow_dependency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildWorkflowDependencies(plan: any): any {
  var ordering: any[] = [];
  var prerequisites: any[] = [];
  var runtime_deps: any[] = [];
  var chains: any[] = [];
  var steps: any = [...py.iter(py.get(plan, "steps", []))];
  var index: any;
  var step: any;
  for ([index, step] of py.enumerate(py.slice(steps, null, 10000))) {
    var depends_on: any = py.toStr(py.get(step, "depends_on", ""));
    if (py.truthy(depends_on)) {
      py.listAppend(ordering, {"step": py.toStr(py.get(step, "id", "")), "depends_on": depends_on});
      py.listAppend(prerequisites, {"step": py.toStr(py.get(step, "id", "")), "requires": depends_on});
    }
    if ((index > 0)) {
      var prev_runtime: any = py.toStr(py.get(py.at(steps, py.sub(index, 1)), "runtime", ""));
      var curr_runtime: any = py.toStr(py.get(step, "runtime", ""));
      if (!py.eq(prev_runtime, curr_runtime)) {
        py.listAppend(runtime_deps, {"from": prev_runtime, "to": curr_runtime});
      }
    }
    py.listAppend(chains, {"step": py.toStr(py.get(step, "id", "")), "action": py.toStr(py.get(step, "action", ""))});
  }
  return {"execution_ordering": ordering, "semantic_prerequisites": prerequisites, "runtime_dependencies": runtime_deps, "extraction_chains": chains, "bounded": true};
}
