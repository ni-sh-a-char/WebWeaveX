/**
 * Converted from Python: core/crypto/serializer_v3.py
 * @generated — WebWeaveX python→javascript library port
 */

import { normalizeValue } from "./crossLanguageNormalizer.js";
import { canonicalJson } from "./canonicalJsonEngine.js";

export function serializeV3(payload: any): any {
  return canonicalJson(normalizeValue(payload));
}
export { canonicalJson, normalizeValue };
