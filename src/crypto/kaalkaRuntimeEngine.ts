/**
 * Behavioral parity with core/crypto/kaalka_runtime_engine.py
 * Re-exports hand-written Kaalka adapter surface.
 */
export {
  KAALKA_ALGORITHM,
  KAALKA_NPM_VERSION,
  computeDeterministicHash,
  computeDeterministicHashPayload,
  computeKaalkaHash,
  computeKaalkaHashPayload,
  decryptValue,
  deriveKaalkaTimeKey,
  encryptValue,
  normalizeRuntimeValue,
  stableSerialize,
} from "./kaalkaRuntime.js";

import { decryptValue as _decryptValue, encryptValue as _encryptValue } from "./kaalkaRuntime.js";

export function encryptBytes(data: Uint8Array, key: string): Record<string, unknown> {
  const encoded = Buffer.from(data).toString("utf8");
  return _encryptValue(encoded, key) as Record<string, unknown>;
}

export function decryptBytes(data: Uint8Array, key: string): Record<string, unknown> {
  const encoded = Buffer.from(data).toString("utf8");
  return _decryptValue(encoded, key) as Record<string, unknown>;
}
