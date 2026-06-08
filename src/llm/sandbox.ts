/**
 * Converted from Python: core/llm/sandbox.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function isolateLlm(core_result: any, llm_output: any): any {
  var base: any = py.deepcopy(core_result);
  return {"structured_data": base, "llm": llm_output};
}
