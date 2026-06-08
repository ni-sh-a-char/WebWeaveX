/**
 * Converted from Python: core/llm/adapters/adapter_sandbox.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function sandboxOutput(core_result: any, llm_output: any): any {
  var out: any = py.pyDict(core_result);
  var meta: any = py.pyDict(py.get(out, "metadata", {}));
  py.setItem(meta, "llm", llm_output);
  py.setItem(out, "metadata", meta);
  return out;
}
