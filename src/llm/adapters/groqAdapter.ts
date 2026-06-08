/**
 * Converted from Python: core/llm/adapters/groq_adapter.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";
import { disabledResult } from "../baseAdapter.js";

export function complete(prompt: any, kwargs: Record<string, any> = {}): any {
  return disabledResult(py.replace(py.at(py.split("core.llm.adapters.groq_adapter", "."), (-1)), "_adapter", ""), "optional_adapter_not_configured");
}
export { disabledResult };
