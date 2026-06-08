/**
 * Converted from Python: core/llm/vllm_adapter.py
 * @generated — WebWeaveX python→javascript library port
 */

import { disabledResult } from "./baseAdapter.js";

export function complete(prompt: any, kwargs: Record<string, any> = {}): any {
  return disabledResult("vllm", "optional_adapter_not_configured");
}
export { disabledResult };
