/**
 * Converted from Python: core/llm/base_adapter.py
 * @generated — WebWeaveX python→javascript library port
 */


export function disabledResult(provider: any, reason: any = "disabled"): any {
  return {"provider": provider, "enabled": false, "ok": false, "reason": reason, "output": ""};
}
