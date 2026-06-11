// Million-vector certification — JavaScript runner (mirror of mv_python.py).
// Usage: cp into the materialized javascript branch, then
//   npx tsx mv_js.mjs [count] > mv_js.json
import { createHash } from "node:crypto";
import { extractSemanticHtml } from "./src/browser/htmlSemanticExtractionEngine.ts";
import { computeKaalkaHash as H } from "./src/crypto/kaalkaRuntime.ts";
import { modelUncertainty } from "./src/evidence/uncertaintyEngine.ts";
import { proveTopology } from "./src/graph/topologyProofEngine.ts";
import { reasonApiSurface } from "./src/repository/apiSurfaceReasoningEngine.ts";
import { analyzeDeploymentSemantics } from "./src/repository/deploymentSemanticsEngine.ts";
import { detectInfraSignals } from "./src/repository/infraSemanticEngine.ts";
import { computeAmbiguityPressure } from "./src/semantic/ambiguityPressureEngine.ts";

const MASK = (1n << 64n) - 1n;
const A = 6364136223846793005n;
const C = 1442695040888963407n;
const W = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta"];
const F = ["Dockerfile", "k8s/deploy.yaml", "src/main.py", "README.md",
  "helm/chart.yaml", ".github/workflows/ci.yml", "infra/main.tf",
  "docs/guide.md"];
const METHODS = ["get", "post", "delete"];

const n = process.argv[2] ? parseInt(process.argv[2], 10) : 1000000;
let state = 20260612n;
function rnd() {
  state = (state * A + C) & MASK;
  return Number((state >> 33n) & 0x7fffffffn);
}

const acc = createHash("sha256");
const famNames = ["application", "extraction", "repository", "runtime", "semantic"];
const famAcc = Object.fromEntries(famNames.map((k) => [k, createHash("sha256")]));
const famCounts = Object.fromEntries(famNames.map((k) => [k, 0]));

for (let i = 0; i < n; i++) {
  let fam, out;
  if (i % 20 === 0) {
    fam = "extraction";
    const t = W[rnd() % 8];
    const h1 = W[rnd() % 8];
    const p1 = W[rnd() % 8];
    const p2 = W[rnd() % 8];
    const extra = rnd() % 2;
    const html = `<html><head><title>${t}</title></head><body><h1>${h1}</h1><p>${p1} ${p2}</p>` +
      (extra ? `<ul><li>${W[rnd() % 8]}</li></ul>` : "") + `</body></html>`;
    out = extractSemanticHtml(html);
  } else {
    const k = i % 6;
    if (k === 0) {
      fam = "semantic";
      out = modelUncertainty(rnd() % 8, rnd() % 8, rnd() % 8);
    } else if (k === 1) {
      fam = "semantic";
      const cnt = rnd() % 5;
      const xs = [];
      for (let j = 0; j < cnt; j++) xs.push(W[rnd() % 8]);
      out = computeAmbiguityPressure(xs);
    } else if (k === 2) {
      fam = "repository";
      const cnt = rnd() % 4;
      const paths = {};
      for (let j = 0; j < cnt; j++) paths[`/p${j}_${rnd() % 50}`] = { [METHODS[rnd() % 3]]: {} };
      out = reasonApiSurface({ paths });
    } else if (k === 3) {
      fam = "repository";
      const cnt = rnd() % 6;
      const xs = [];
      for (let j = 0; j < cnt; j++) xs.push(F[rnd() % 8]);
      out = detectInfraSignals(xs);
    } else if (k === 4) {
      fam = "runtime";
      const cnt = rnd() % 6;
      const edges = [];
      for (let j = 0; j < cnt; j++) edges.push({ from: W[rnd() % 8], to: W[rnd() % 8] });
      out = proveTopology({ edges });
    } else {
      fam = "application";
      const cnt = rnd() % 6;
      const xs = [];
      for (let j = 0; j < cnt; j++) xs.push(F[rnd() % 8]);
      out = analyzeDeploymentSemantics(xs);
    }
  }
  const b = H(out) + "\n";
  acc.update(b, "ascii");
  famAcc[fam].update(b, "ascii");
  famCounts[fam] += 1;
  if ((i + 1) % 100000 === 0) process.stderr.write(`  js ${i + 1}\n`);
}

const result = {
  count: n,
  family_counts: famCounts,
  family_digests: Object.fromEntries(famNames.map((k) => [k, famAcc[k].digest("hex")])),
  final_digest: acc.digest("hex"),
};
process.stdout.write(JSON.stringify(result));
