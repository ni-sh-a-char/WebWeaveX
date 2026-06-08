/**
 * Converted from Python: core/llm/adapters/adapter_timeout_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function timeoutConfig(timeout: any = py.F(10.0)): any {
  return {"timeout": py.toFloat(timeout)};
}
