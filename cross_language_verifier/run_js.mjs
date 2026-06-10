// Cross-language verifier — JavaScript runner.
// Copy into the materialized javascript branch root, then:
//   npx tsx run_js.mjs vectors.json out_js.json
import { readFileSync, writeFileSync } from "node:fs";
import { stableSerialize } from "./src/determinism/normalization.ts";
import {
  computeDeterministicHash,
  deriveKaalkaTimeKey,
  decryptValue,
  encryptValue,
} from "./src/crypto/kaalkaRuntime.ts";
import { hexFingerprint } from "./src/crypto/kaalkaEngine.ts";
import { dumpsDeterministic } from "./src/serialize/deterministicSerializer.ts";

const spec = JSON.parse(readFileSync(process.argv[2], "utf-8"));
const key = spec.key;
const out = { time_key: deriveKaalkaTimeKey(key), vectors: {} };
for (const vid of Object.keys(spec.vectors).sort()) {
  const v = spec.vectors[vid];
  const enc = encryptValue(v, key).encrypted;
  out.vectors[vid] = {
    stable: stableSerialize(v),
    canonical: dumpsDeterministic(v),
    hash: computeDeterministicHash(v),
    encrypted_b64: enc,
    roundtrip_ok: decryptValue(enc, key).decrypted === stableSerialize(v),
    fingerprint_hex: hexFingerprint(v),
  };
}
writeFileSync(process.argv[3], JSON.stringify(out, null, 1));
