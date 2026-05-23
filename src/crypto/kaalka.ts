/** Native Kaalka deterministic encryption (parity with Python core/crypto). */

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
  const enc = new TextEncoder().encode(normalizeRuntimeValue(key));
  return enc.slice(0, MAX_KEY_BYTES);
}

function safeByte(value: number): number {
  return ((value % 256) + 256) % 256;
}

export function kaalkaEncryptBytes(data: Uint8Array, token: Uint8Array): Uint8Array {
  const out = new Uint8Array(data.length);
  const lnMod = data.length % 251;
  for (let i = 0; i < data.length; i++) {
    const tk = token.length ? token[i % token.length]! : 0;
    const plain = data[i]!;
    const value = ((plain ^ tk) + i * 31 + lnMod) % 256;
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
  const norm = normalizeRuntimeValue(plaintext);
  const data = new TextEncoder().encode(norm).slice(0, MAX_VALUE_BYTES);
  const token = deriveToken(key);
  const enc = kaalkaEncryptBytes(data, token);
  const hex = Array.from(enc)
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
  return { encrypted: hex, algorithm: "kaalka", deterministic: true, bounded: true };
}

export function decryptValue(
  ciphertext: string,
  key: string,
): { decrypted: string; algorithm: string; deterministic: boolean; bounded: boolean } {
  const raw = Uint8Array.from(Buffer.from(ciphertext, "hex"));
  const token = deriveToken(key);
  const dec = kaalkaDecryptBytes(raw.slice(0, MAX_VALUE_BYTES), token);
  return {
    decrypted: new TextDecoder().decode(dec),
    algorithm: "kaalka",
    deterministic: true,
    bounded: true,
  };
}
