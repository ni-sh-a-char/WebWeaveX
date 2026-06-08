/**
 * Deterministic hashing + authenticated encryption (Kaalka).
 *   npx tsx examples/deterministic-hashing.ts
 */
import { computeKaalkaHash, fingerprint, encryptValue, decryptValue } from "webweavex";

console.log("kaalka hash:", computeKaalkaHash("webweavex"));
console.log("fingerprint:", fingerprint("webweavex"));
const enc = encryptValue({ secret: "value", n: 42 }, "my-key");
console.log("encrypted:", enc.encrypted.slice(0, 24), "…");
console.log("roundtrip:", JSON.parse(decryptValue(enc.encrypted, "my-key").decrypted));
