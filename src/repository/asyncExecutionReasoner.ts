/**
 * Converted from Python: core/repository/async_execution_reasoner.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { detectAsyncRuntime } from "./asyncRuntimeEngine.js";

export function reasonAsyncExecution(source: any, path: any = ""): any {
  var async_r: any = detectAsyncRuntime(source, path);
  return {"async": async_r, "propagation": [{"kind": "await", "count": py.get(async_r, "await_count", 0)}], "evidence": py.get(async_r, "evidence", []), "parser_backed": py.get(async_r, "parser_backed", false)};
}
export { detectAsyncRuntime };
