/**
 * Converted from Python: core/crypto/kaalka_key_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { normalizeRuntimeValue } from "./kaalkaRuntimeEngine.js";

export let MAX_KEY_BYTES: any = 4096;
export function deriveKaalkaKeyBytes(key: any): any {
  var normalized: any = normalizeRuntimeValue(key);
  return py.slice(py.encode(normalized, "utf-8"), null, MAX_KEY_BYTES);
}
export { normalizeRuntimeValue };
