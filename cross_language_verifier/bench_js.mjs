// Phase 13: JS micro-benchmark (run with npx tsx from the js worktree).
import { stableSerialize } from "./src/determinism/normalization.ts";
import { computeDeterministicHash, encryptValue } from "./src/crypto/kaalkaRuntime.ts";

const PAYLOAD = { title: "Benchmark payload — café 中文 \u{1F680}", items: Array.from({ length: 50 }, (_, i) => ({ id: i, score: i / 7.0, tags: ["a", "b", "c"] })), nested: { depth: { x: [1, 2.5, null, true] } } };
const N = 2000;

let t0 = performance.now();
for (let i = 0; i < N; i++) stableSerialize({ ...PAYLOAD, i });
let t1 = performance.now();
for (let i = 0; i < N; i++) computeDeterministicHash({ ...PAYLOAD, i });
let t2 = performance.now();
for (let i = 0; i < N / 10; i++) encryptValue({ ...PAYLOAD, i }, "bench-key");
let t3 = performance.now();

console.log(JSON.stringify({
  language: "javascript",
  serialize_ops_per_s: Math.round(N / ((t1 - t0) / 1000)),
  hash_ops_per_s: Math.round(N / ((t2 - t1) / 1000)),
  encrypt_ops_per_s: Math.round((N / 10) / ((t3 - t2) / 1000)),
}));
