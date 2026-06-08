/**
 * Converted from Python: core/runtime/semantic_dependency_resolver.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export function resolveDependencies(tasks: any): any {
  var resolved: any[] = [];
  var unresolved: any[] = [];
  var indexed: any[] = [];
  var i: any;
  var task: any;
  for ([i, task] of py.enumerate(tasks)) {
    var task_id: any = py.get(task, "id", `task_${py.toStr(i)}`);
    py.listAppend(indexed, {...(task), "id": task_id});
  }
  var known: any = py.toSet(py.iter(indexed).map((t: any) => py.at(t, "id")));
  for (task of py.iter(indexed)) {
    var deps: any = py.get(task, "depends_on", []);
    if (py.all(py.iter(deps).map((dep: any) => py.contains(known, dep)))) {
      py.listAppend(resolved, task);
    } else {
      py.listAppend(unresolved, task);
    }
  }
  return {"resolved": resolved, "unresolved": unresolved};
}
