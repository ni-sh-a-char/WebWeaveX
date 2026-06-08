/**
 * Converted from Python: core/runtime/concurrent_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";
// from concurrent.futures import ... (unmapped)

export let MAX_WORKERS: any = 8;
export function executeConcurrently(tasks: any): any {
  var results: any[] = [];
  var executor: any = py.threadPoolExecutor();
  var futures: any = py.iter(tasks).map((task: any) => executor.submit(task));
  var future: any;
  for (future of py.iter(futures)) {
    py.listAppend(results, future.result());
  }
  return {"results": results, "count": py.len(results)};
}
