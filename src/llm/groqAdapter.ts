/**
 * Converted from Python: core/llm/groq_adapter.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { disabledResult } from "./baseAdapter.js";

export function complete(prompt: any, timeout: any = py.F(10.0), task: any = "completion"): any {
  if (py.eq((py.environ[String("WEBWEAVEX_DISABLE_LLM")] ?? "0"), "1")) {
    return disabledResult("groq", "llm_disabled");
  }
  var api_key: any = (py.environ[String("GROQ_API_KEY")] ?? "");
  if (!py.truthy(api_key)) {
    return disabledResult("groq", "missing_api_key");
  }
  var Groq: any = null;
  var exc: any = py.err("ImportError", "module not available");
  return disabledResult("groq", `failure:${py.toStr(exc)}`);
}
export { disabledResult };
