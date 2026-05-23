/**
 * WebWeaveX → Kaalka v5 adapter.
 *
 * Formula (cross-language contract):
 *   normalizeRuntimeValue / stableSerialize → deriveKaalkaTimeKey(key) → kaalka@5 encrypt/decrypt
 *   computeDeterministicHash → stableSerialize → SHA-256 (deterministic digest substrate)
 */
import { createHash } from "node:crypto";
import { normalizeRuntimeValue, stableSerialize } from "../determinism/normalization.js";
import { kaalkaV5DecryptBytes, kaalkaV5EncryptBytes } from "./kaalkaV5Client.js";

export { normalizeRuntimeValue, stableSerialize } from "../determinism/normalization.js";

export const KAALKA_ALGORITHM = "webweavex-formula+kaalka@5.0.0";
export const KAALKA_NPM_VERSION = "5.0.0";

const KAALKA_FALLBACK_TIME_KEY = "12:0:0";

/** Kaalka v5 message crypto is not reversible for every clock tuple; probe before use. */
function kaalkaTimeKeyRoundTrips(timeKey: string): boolean {
  const probe = Buffer.from("\x00\x7f\xff🚀probe", "utf8");
  try {
    const enc = kaalkaV5EncryptBytes(probe, timeKey);
    const dec = kaalkaV5DecryptBytes(enc, timeKey);
    return dec.equals(probe);
  } catch {
    return false;
  }
}

/** Map encryption key → Kaalka v5 `HH:MM:SS` time_key (deterministic, clock-independent). */
export function deriveKaalkaTimeKey(encryptionKey: string): string {
  const digest = createHash("sha256").update(normalizeRuntimeValue(encryptionKey), "utf8").digest();
  for (let i = 0; i <= digest.length - 3; i++) {
    const candidate = `${digest[i]! % 12}:${digest[i + 1]! % 60}:${digest[i + 2]! % 60}`;
    if (kaalkaTimeKeyRoundTrips(candidate)) return candidate;
  }
  if (kaalkaTimeKeyRoundTrips(KAALKA_FALLBACK_TIME_KEY)) return KAALKA_FALLBACK_TIME_KEY;
  return "12:34:56";
}

/** Base64 wrapper for Kaalka v5 byte ciphertext. */
export function encodeKaalkaCiphertext(raw: Buffer): string {
  return raw.toString("base64");
}

export function decodeKaalkaCiphertext(encoded: string): Buffer {
  return Buffer.from(encoded, "base64");
}

export function encryptValue(
  value: unknown,
  key: string,
): { encrypted: string; algorithm: string; deterministic: boolean; bounded: boolean } {
  const payload = stableSerialize(value);
  const timeKey = deriveKaalkaTimeKey(key);
  const raw = kaalkaV5EncryptBytes(Buffer.from(payload, "utf8"), timeKey);
  return {
    encrypted: encodeKaalkaCiphertext(raw),
    algorithm: KAALKA_ALGORITHM,
    deterministic: true,
    bounded: true,
  };
}

export function decryptValue(
  ciphertext: string,
  key: string,
): { decrypted: string; algorithm: string; deterministic: boolean; bounded: boolean } {
  const timeKey = deriveKaalkaTimeKey(key);
  const raw = decodeKaalkaCiphertext(ciphertext);
  const decrypted = kaalkaV5DecryptBytes(raw, timeKey).toString("utf8");
  return {
    decrypted,
    algorithm: KAALKA_ALGORITHM,
    deterministic: true,
    bounded: true,
  };
}

export function computeDeterministicHash(value: unknown): string {
  return createHash("sha256").update(stableSerialize(value), "utf8").digest("hex");
}

export function computeDeterministicHashPayload(payload: unknown): string {
  return computeDeterministicHash(payload);
}

export const computeKaalkaHash = computeDeterministicHash;
export const computeKaalkaHashPayload = computeDeterministicHashPayload;
