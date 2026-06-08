/**
 * Converted from Python: core/llm/anthropic_adapter.py
 * @generated — WebWeaveX python→javascript library port
 */

import { disabledResult } from "./baseAdapter.js";

export function complete(prompt: any, kwargs: Record<string, any> = {}): any {
  return disabledResult("anthropic", "optional_adapter_not_configured");
}
export { disabledResult };
