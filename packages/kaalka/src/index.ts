/**
 * Kaalka deterministic runtime cryptography — canonical cross-language implementation.
 * Used by WebWeaveX Python/JS/Rust/Go for identical encrypt/hash output.
 */

import { createHash } from "node:crypto";

const MAX_VALUE_BYTES = 10_000_000;
const MAX_KEY_BYTES = 4096;

export function normalizeRuntimeValue(value: string): string {
  return value
    .normalize("NFKC")
    .replace(/\r\n/g, "\n")
    .replace(/\r/g, "\n")
    .replace(/\s+$/, "");
}

function deriveToken(key: string): Uint8Array {
  return new TextEncoder().encode(normalizeRuntimeValue(key)).slice(0, MAX_KEY_BYTES);
}

function safeByte(value: number): number {
  return ((value % 256) + 256) % 256;
}

export function kaalkaEncryptBytes(data: Uint8Array, token: Uint8Array): Uint8Array {
  const out = new Uint8Array(data.length);
  const lnMod = data.length % 251;
  for (let i = 0; i < data.length; i++) {
    const tk = token.length ? token[i % token.length]! : 0;
    const value = ((data[i]! ^ tk) + i * 31 + lnMod) % 256;
    out[i] = safeByte(value);
  }
  return out;
}

export function kaalkaDecryptBytes(data: Uint8Array, token: Uint8Array): Uint8Array {
  const out = new Uint8Array(data.length);
  const lnMod = data.length % 251;
  for (let i = 0; i < data.length; i++) {
    const tk = token.length ? token[i % token.length]! : 0;
    const n = data[i]!;
    const plain = (n - i * 31 - lnMod) % 256;
    out[i] = safeByte(plain ^ tk);
  }
  return out;
}

export function encryptValue(
  plaintext: string,
  key: string,
): { encrypted: string; algorithm: string; deterministic: boolean; bounded: boolean } {
  const data = new TextEncoder().encode(normalizeRuntimeValue(plaintext)).slice(0, MAX_VALUE_BYTES);
  const enc = kaalkaEncryptBytes(data, deriveToken(key));
  return {
    encrypted: Array.from(enc)
      .map((b) => b.toString(16).padStart(2, "0"))
      .join(""),
    algorithm: "kaalka",
    deterministic: true,
    bounded: true,
  };
}

export function decryptValue(
  ciphertext: string,
  key: string,
): { decrypted: string; algorithm: string; deterministic: boolean; bounded: boolean } {
  const raw = Uint8Array.from(Buffer.from(ciphertext, "hex"));
  const dec = kaalkaDecryptBytes(raw.slice(0, MAX_VALUE_BYTES), deriveToken(key));
  return {
    decrypted: new TextDecoder().decode(dec),
    algorithm: "kaalka",
    deterministic: true,
    bounded: true,
  };
}

export function computeDeterministicHash(value: string): string {
  const normalized = normalizeRuntimeValue(value);
  return createHash("sha256")
    .update(Buffer.from(normalized, "utf-8").subarray(0, MAX_VALUE_BYTES))
    .digest("hex");
}

export function computeDeterministicHashPayload(payload: unknown): string {
  const keys = (obj: Record<string, unknown>): Record<string, unknown> => {
    const sorted: Record<string, unknown> = {};
    for (const k of Object.keys(obj).sort()) {
      const v = obj[k];
      sorted[k] =
        v && typeof v === "object" && !Array.isArray(v)
          ? keys(v as Record<string, unknown>)
          : v;
    }
    return sorted;
  };
  const body =
    payload && typeof payload === "object"
      ? JSON.stringify(keys(payload as Record<string, unknown>))
      : JSON.stringify(payload);
  return computeDeterministicHash(body);
}
