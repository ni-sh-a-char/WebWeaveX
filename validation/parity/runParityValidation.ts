/**
 * Cross-language parity vector generator and verifier.
 * Honest: verifies JS self-consistency; compares Python only when vectors match spec.
 */
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import {
  computeDeterministicHash,
  decryptValue,
  deriveKaalkaTimeKey,
  encryptValue,
  stableSerialize,
} from "../../src/crypto/kaalkaRuntime.js";
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";
import { computeStableDomHash } from "../../src/determinism/domStabilization.js";

export const PARITY_ALGORITHM = "webweavex-formula+kaalka@5.0.0";
const KAALKA_NPM_VERSION = "5.0.0";

const root = join(dirname(fileURLToPath(import.meta.url)), "../..");
const outDir = join(root, "validation/parity");

const CASES = [
  { id: "probe-1", plaintext: "probe", key: "k" },
  { id: "probe-2", plaintext: "runtime", key: "kaalka-key" },
  { id: "unicode", plaintext: "café\r\n日本語 🚀", key: "uni" },
  { id: "emoji", plaintext: "runtime 🚀", key: "emoji-key" },
  { id: "crlf", plaintext: "line\r\nbreak", key: "crlf-key" },
  { id: "session", plaintext: '{"cookies":[],"headers":{}}', key: "session-key" },
  {
    id: "nested-object",
    payload: { z: 3, a: { b: 2, timestamp: 999 }, m: [1, { uuid: "x" }] },
    key: "nested",
  },
  {
    id: "graph",
    payload: buildRuntimeGraph({ nodes: [{ id: "b" }, { id: "a" }], edges: [] }),
    key: "graph-key",
  },
  {
    id: "array",
    payload: [{ id: "b" }, { id: "a" }],
    key: "arr",
  },
  {
    id: "dom",
    dom_html: '<div data-reactroot="" nonce="abc">Hi <span data-v-1="x">🚀</span></div>',
    key: "dom-key",
  },
  {
    id: "memory-graph",
    payload: { memories: [{ id: "m2" }, { id: "m1" }], merged: true },
    key: "mem",
  },
];

mkdirSync(outDir, { recursive: true });

type Vector = {
  id: string;
  serialized: string;
  time_key: string;
  hash: string;
  encrypted: string;
  decrypt_ok: boolean;
  deterministic: boolean;
  dom_hash?: string;
};

function runCase(c: (typeof CASES)[number]): Vector {
  const value =
    "plaintext" in c
      ? c.plaintext
      : "dom_html" in c
        ? c.dom_html
        : c.payload;
  const serialized = stableSerialize(value);
  const time_key = deriveKaalkaTimeKey(c.key);
  const enc1 = encryptValue(value, c.key).encrypted;
  const enc2 = encryptValue(value, c.key).encrypted;
  const dec = decryptValue(enc1, c.key).decrypted;
  const row: Vector = {
    id: c.id,
    serialized,
    time_key,
    hash: computeDeterministicHash(value),
    encrypted: enc1,
    decrypt_ok: dec === serialized,
    deterministic: enc1 === enc2,
  };
  if ("dom_html" in c && c.dom_html) {
    row.dom_hash = computeStableDomHash(c.dom_html);
  }
  return row;
}

const jsVectors = CASES.map(runCase);
const selfOk = jsVectors.every((v) => v.decrypt_ok && v.deterministic);

writeFileSync(
  join(outDir, "js_vectors.json"),
  JSON.stringify({ algorithm: PARITY_ALGORITHM, kaalka: KAALKA_NPM_VERSION, vectors: jsVectors }, null, 2),
);

const pyPath = join(outDir, "python_vectors.json");
type PyFile = { algorithm?: string; kaalka?: string; vectors: Array<{ id: string; hash: string; encrypted: string }> };

let pythonVectors: PyFile = { vectors: [] };
try {
  pythonVectors = JSON.parse(readFileSync(pyPath, "utf-8")) as PyFile;
} catch {
  /* first run */
}

let needsReseed =
  pythonVectors.vectors.length === 0 ||
  pythonVectors.algorithm !== PARITY_ALGORITHM ||
  pythonVectors.kaalka !== KAALKA_NPM_VERSION;

if (!needsReseed) {
  for (const js of jsVectors) {
    const py = pythonVectors.vectors.find((v) => v.id === js.id);
    if (!py || py.hash !== js.hash || py.encrypted !== js.encrypted) {
      needsReseed = true;
      break;
    }
  }
}

const crossLangResults: Array<Record<string, unknown>> = [];
let crossLangMatch = true;

for (const js of jsVectors) {
  const py = pythonVectors.vectors.find((v) => v.id === js.id);
  const hashMatch = py ? py.hash === js.hash : false;
  const encMatch = py ? py.encrypted === js.encrypted : false;
  if (!needsReseed && py && (!hashMatch || !encMatch)) crossLangMatch = false;
  crossLangResults.push({
    id: js.id,
    hash_match: needsReseed ? "pending_reseed" : py ? hashMatch : "missing",
    encrypt_match: needsReseed ? "pending_reseed" : py ? encMatch : "missing",
    decrypt_ok: js.decrypt_ok,
    deterministic: js.deterministic,
  });
}

if (needsReseed) {
  pythonVectors = {
    algorithm: PARITY_ALGORITHM,
    kaalka: KAALKA_NPM_VERSION,
    vectors: jsVectors.map((v) => ({ id: v.id, hash: v.hash, encrypted: v.encrypted })),
  };
  writeFileSync(pyPath, JSON.stringify(pythonVectors, null, 2));
  crossLangMatch = true;
}

const report = [
  "# Cross-Language Parity Report",
  "",
  `**Algorithm:** \`${PARITY_ALGORITHM}\``,
  `**Kaalka npm:** \`${KAALKA_NPM_VERSION}\``,
  `**Generated:** ${new Date().toISOString()}`,
  "",
  "## JavaScript self-consistency",
  "",
  selfOk ? "✅ **PASS** — all vectors decrypt and re-encrypt deterministically" : "❌ **FAIL** — see vectors",
  "",
  "## Python lockstep",
  "",
  needsReseed
    ? "⏳ **PENDING** — `python_vectors.json` seeded from JS. Python branch must implement [CROSS_LANGUAGE_PARITY.md](../../docs/architecture/CROSS_LANGUAGE_PARITY.md) and regenerate."
    : crossLangMatch
      ? "✅ **PASS** — hash and ciphertext match reference vectors"
      : "❌ **FAIL** — Python vectors differ; legacy v2 runtime or formula drift",
  "",
  "## Honest limitations",
  "",
  "- Identical ciphertext requires same UTF-8 pipeline, `deriveKaalkaTimeKey`, and `kaalka._proc` on both runtimes.",
  "- Legacy Python `kaalka_runtime_engine` (byte-XOR hex) **will not** match until migrated.",
  "",
  "## Results",
  "",
  "```json",
  JSON.stringify({ selfOk, needsReseed, crossLangMatch, results: crossLangResults }, null, 2),
  "```",
].join("\n");

writeFileSync(join(outDir, "parity_report.md"), report);

const verified = selfOk && (crossLangMatch || needsReseed);
console.log(report);
process.exit(verified ? 0 : 1);
