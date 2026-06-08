/**
 * Converted from Python: core/serialize/unicode_normalization_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function normalizeUnicode(value: any): any {
  return py.uniNormalize("NFC", py.or2(value, () => ("")));
}
