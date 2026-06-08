/**
 * Converted from Python: core/autonomy/semantic_task_decomposition_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_TASKS: any = 1000;
export function decomposeSemanticTask(task: any): any {
  var goal: any = py.toStr(py.get(task, "goal", ""));
  var words: any = py.iter(py.split(goal)).filter((w: any) => py.truthy(py.strip(w))).map((w: any) => py.strip(w));
  var subtasks: any[] = [];
  var idx: any;
  var word: any;
  for ([idx, word] of py.enumerate(py.slice(words, null, MAX_TASKS))) {
    py.listAppend(subtasks, {"id": `task_${py.toStr(idx)}`, "semantic_unit": word});
  }
  return {"subtasks": subtasks, "count": py.len(subtasks), "bounded": true};
}
