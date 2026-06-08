/**
 * Converted from Python: core/synchronization/runtime_merge_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function mergeRuntimeRealities(realities: any): any {
  var merged_semantic: Record<string, any> = {};
  var merged_workflow: Record<string, any> = {};
  var merged_application: Record<string, any> = {};
  var timelines: any[] = [];
  var reality: any;
  for (reality of py.iter(py.slice(realities, null, 1000))) {
    py.listAppend(timelines, {"reality_id": py.toStr(py.get(reality, "reality_id", "")), "tick": py.toInt(py.get(reality, "tick", 0))});
    py.update(merged_semantic, py.get(reality, "semantic", {}));
    py.update(merged_workflow, py.get(reality, "workflow", {}));
    py.update(merged_application, py.get(reality, "application", {}));
  }
  return {"semantic": merged_semantic, "workflow": merged_workflow, "application": merged_application, "timelines": py.sorted(timelines, {key: ((item: any) => py.at(item, "tick")) as (item: any) => any}), "reality_count": py.len(realities), "bounded": true};
}
