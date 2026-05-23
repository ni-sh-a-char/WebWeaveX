import { writeFileSync } from "node:fs";
import { encryptValue } from "kaalka";

const vectors = [
  { id: "probe-1", plaintext: "probe", key: "k" },
  { id: "probe-2", plaintext: "runtime", key: "kaalka-key" },
  { id: "session", plaintext: '{"cookies":[],"headers":{}}', key: "session-key" },
].map((v) => ({
  ...v,
  encrypted: encryptValue(v.plaintext, v.key).encrypted,
}));

writeFileSync(
  "validation/kaalka/reference_vectors.json",
  JSON.stringify({ language: "javascript", algorithm: "kaalka", vectors }, null, 2),
);
console.log("wrote vectors");
