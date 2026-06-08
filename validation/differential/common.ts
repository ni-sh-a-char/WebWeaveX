/**
 * Shared differential equivalence utilities.
 * Canonical vectors load from specification/ (authority), with validation/ fallback.
 */
import { readFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";
import { computeKaalkaHash, computeKaalkaHashPayload } from "../../src/crypto/kaalkaRuntime.js";
import { RuntimeGraphContract, type RuntimeGraph } from "../../src/contracts/graphContracts.js";

const root = join(dirname(fileURLToPath(import.meta.url)), "../..");

const SPEC_AUTHORITY = "webweavex-spec";

export type CanonicalVector = {
  id: string;
  input: Record<string, unknown>;
  canonical_output: Record<string, unknown>;
  runtime_hash?: string;
  semantic_hash?: string;
  graph_hash?: string;
  replay_hash?: string;
  vm_hash?: string;
  memory_hash?: string;
  deterministic_fingerprint?: string;
};

export type VectorFamily = {
  family: string;
  generated_at: string;
  source: string;
  algorithm: string;
  vectors: CanonicalVector[];
};

export type ProbeResult = {
  id: string;
  pass: boolean;
  mismatches: string[];
};

export type FamilyReport = {
  family: string;
  pass: boolean;
  probes: ProbeResult[];
  vector_count: number;
};

export function loadVectorFamily(family: string): VectorFamily {
  const specPath = join(root, "specification/vectors", family, "canonical.json");
  const legacyPath = join(root, "validation/vectors", family, "canonical.json");
  const path = existsSync(specPath) ? specPath : legacyPath;
  if (!existsSync(path)) {
    throw new Error(
      `Missing vector family ${family}. Expected ${specPath} or ${legacyPath}. ` +
        "Copy validation/vectors to specification/vectors or run vector sync.",
    );
  }
  const data = JSON.parse(readFileSync(path, "utf-8")) as VectorFamily;
  if (data.source === "origin/python") {
    data.source = SPEC_AUTHORITY;
  }
  return data;
}

export function fingerprint(value: unknown): string {
  return computeKaalkaHashPayload(value);
}

/** Recursive JSON matching Python json.dumps(..., sort_keys=True, separators=(', ', ': '), default=str). */
export function pythonStyleSerialize(value: unknown): string {
  if (value === null || value === undefined) return "null";
  if (typeof value === "boolean") return value ? "true" : "false";
  if (typeof value === "number") return Number.isFinite(value) ? String(value) : "null";
  if (typeof value === "string") return JSON.stringify(value);
  if (Array.isArray(value)) {
    return `[${value.map((v) => pythonStyleSerialize(v)).join(", ")}]`;
  }
  if (typeof value === "object") {
    const obj = value as Record<string, unknown>;
    const keys = Object.keys(obj).sort();
    const pairs = keys.map((k) => `${JSON.stringify(k)}: ${pythonStyleSerialize(obj[k])}`);
    return `{${pairs.join(", ")}}`;
  }
  return JSON.stringify(String(value));
}

/** Match Python replay_equivalence_engine._graph_hash (nodes+edges JSON only). */
export function parityGraphHash(graph: RuntimeGraph | Record<string, unknown>): string {
  const normalized = RuntimeGraphContract.normalize(graph as RuntimeGraph);
  const body = pythonStyleSerialize({ nodes: normalized.nodes, edges: normalized.edges });
  return sha256Hex(body);
}

export function sha256Hex(data: string): string {
  return createHash("sha256").update(data, "utf8").digest("hex");
}

function compareField(
  label: string,
  expected: string | undefined,
  actual: string | undefined,
  mismatches: string[],
): void {
  if (expected == null) return;
  if (actual !== expected) {
    mismatches.push(`${label}: expected ${expected.slice(0, 16)}… got ${(actual ?? "null").slice(0, 16)}…`);
  }
}

export function compareVector(
  vector: CanonicalVector,
  jsOutput: Record<string, unknown>,
  hashes: {
    runtime_hash?: string;
    graph_hash?: string;
    memory_hash?: string;
    replay_hash?: string;
    vm_hash?: string;
    semantic_hash?: string;
    deterministic_fingerprint?: string;
  },
): ProbeResult {
  const mismatches: string[] = [];
  compareField("runtime_hash", vector.runtime_hash, hashes.runtime_hash, mismatches);
  compareField("graph_hash", vector.graph_hash, hashes.graph_hash, mismatches);
  compareField("memory_hash", vector.memory_hash, hashes.memory_hash, mismatches);
  compareField("replay_hash", vector.replay_hash, hashes.replay_hash, mismatches);
  compareField("vm_hash", vector.vm_hash, hashes.vm_hash, mismatches);
  compareField("semantic_hash", vector.semantic_hash, hashes.semantic_hash, mismatches);
  compareField(
    "deterministic_fingerprint",
    vector.deterministic_fingerprint,
    hashes.deterministic_fingerprint,
    mismatches,
  );

  const canonicalBounded = (vector.canonical_output as Record<string, unknown>).bounded;
  if (canonicalBounded === true && jsOutput.bounded !== true) {
    mismatches.push("bounded: expected true");
  }

  return { id: vector.id, pass: mismatches.length === 0, mismatches };
}

export function runFamily(
  family: string,
  runner: (vector: CanonicalVector) => {
    output: Record<string, unknown>;
    hashes: Parameters<typeof compareVector>[2];
  },
): FamilyReport {
  const data = loadVectorFamily(family);
  const probes: ProbeResult[] = [];
  for (const vector of data.vectors) {
    const { output, hashes } = runner(vector);
    probes.push(compareVector(vector, output, hashes));
  }
  const pass = probes.every((p) => p.pass);
  return { family, pass, probes, vector_count: data.vectors.length };
}

export function printFamilyReport(report: FamilyReport, label: string): void {
  const status = report.pass ? "PASS" : "FAIL";
  console.log(`\n## ${label} [${status}] (${report.vector_count} vectors)`);
  for (const p of report.probes) {
    if (!p.pass) {
      console.log(`  ❌ ${p.id}:`, p.mismatches.join("; "));
    } else {
      console.log(`  ✅ ${p.id}`);
    }
  }
}

export function exitOnReports(reports: FamilyReport[]): void {
  const pass = reports.every((r) => r.pass);
  if (!pass) process.exit(1);
}
