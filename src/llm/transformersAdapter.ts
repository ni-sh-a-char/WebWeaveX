/**
 * Converted from Python: core/llm/transformers_adapter.py
 * @generated — WebWeaveX python→javascript library port
 */

import { disabledResult } from "./baseAdapter.js";

export function complete(prompt: any, kwargs: Record<string, any> = {}): any {
  return disabledResult("transformers", "optional_adapter_not_configured");
}
export { disabledResult };
