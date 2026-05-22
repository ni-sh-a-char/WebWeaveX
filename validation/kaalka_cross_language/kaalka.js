/**
 * Kaalka reference implementation (must match core/crypto/kaalka_engine.py).
 */
function normalizeRuntimeValue(value) {
  return value.replace(/\r\n/g, "\n").replace(/\r/g, "\n").replace(/\s+$/, "");
}

function deriveToken(key) {
  const enc = new TextEncoder().encode(normalizeRuntimeValue(key));
  return enc.slice(0, 4096);
}

function kaalkaEncryptBytes(data, token) {
  const out = [];
  const lnMod = data.length % 251;
  for (let i = 0; i < data.length; i++) {
    const tk = token.length ? token[i % token.length] : 0;
    const plain = data[i];
    const value = ((plain ^ tk) + (i * 31) + lnMod) % 256;
    out.push(((value % 256) + 256) % 256);
  }
  return Uint8Array.from(out);
}

function encryptValue(plaintext, key) {
  const norm = normalizeRuntimeValue(plaintext);
  const data = new TextEncoder().encode(norm);
  const token = deriveToken(key);
  const enc = kaalkaEncryptBytes(data, token);
  return Array.from(enc)
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

module.exports = { encryptValue, normalizeRuntimeValue };
