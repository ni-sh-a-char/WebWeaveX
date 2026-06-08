import { readdirSync, existsSync } from "node:fs";
import { join } from "node:path";
import {
  compareVector,
  fingerprint,
  loadVectorFamily,
  type CanonicalVector,
} from "../differential/common.js";

function stripBounded(value: unknown): unknown {
  if (value === null || typeof value !== "object") return value;
  if (Array.isArray(value)) return value.map(stripBounded);
  const obj = { ... (value as Record<string, unknown>) };
  delete obj.bounded;
  for (const key of Object.keys(obj)) {
    obj[key] = stripBounded(obj[key]);
  }
  return obj;
}
import { deepCompare, summarizeDiffs } from "./deepCompare.js";
import { FAMILY_RUNNERS } from "./familyRunners.js";
import type { EquivalenceProbeResult, SubsystemSummary, UniversalEquivalenceSummary } from "./types.js";

const SUBSYSTEM_MAP: Record<string, string[]> = {
  runtime: ["runtime_vectors", "runtime_identity_vectors", "continuation_vectors"],
  memory: ["memory_vectors", "continuation_memory_vectors", "distributed_memory_vectors"],
  reconstruction: ["reconstruction_vectors"],
  semantic: ["semantic_vectors", "semantic_reconciliation_vectors"],
  ontology: ["ontology_vectors"],
  workflow: ["workflow_vectors", "workflow_graph_vectors"],
  distributed: ["distributed_vectors", "distributed_replay_vectors"],
  replay: ["replay_vectors"],
  vm: ["vm_vectors"],
  graph: ["graph_vectors", "browser_vectors"],
  extraction: ["orchestration_vectors", "parser_vectors"],
  repository: ["repository_vectors"],
};

function listVectorFamilies(vectorsRoot: string): string[] {
  if (!existsSync(vectorsRoot)) return [];
  return readdirSync(vectorsRoot, { withFileTypes: true })
    .filter((d) => d.isDirectory() && existsSync(join(vectorsRoot, d.name, "canonical.json")))
    .map((d) => d.name)
    .sort();
}

function domainFlags(family: string, state?: EquivalenceProbeResult["domains"]): EquivalenceProbeResult["domains"] {
  const base = {
    runtime: false,
    memory: false,
    graph: false,
    semantic: false,
    ontology: false,
    workflow: false,
    distributed: false,
    replay: false,
    vm: false,
  };
  for (const [domain, families] of Object.entries(SUBSYSTEM_MAP)) {
    if (families.includes(family)) {
      if (domain === "runtime") base.runtime = true;
      if (domain === "memory") base.memory = true;
      if (domain === "graph") base.graph = true;
      if (domain === "semantic") base.semantic = true;
      if (domain === "ontology") base.ontology = true;
      if (domain === "workflow") base.workflow = true;
      if (domain === "distributed") base.distributed = true;
      if (domain === "replay") base.replay = true;
      if (domain === "vm") base.vm = true;
    }
  }
  return { ...base, ...state };
}

export function runProbe(family: string, vector: CanonicalVector): EquivalenceProbeResult {
  const runner = FAMILY_RUNNERS[family];
  if (!runner) {
    return {
      family,
      vector_id: vector.id,
      pass: false,
      hash_pass: false,
      structure_pass: false,
      hash_mismatches: [`no JS runner for family ${family}`],
      structural_diffs: [],
      domains: domainFlags(family),
    };
  }

  const { output, hashes: runnerHashes, state } = runner(vector);
  const hashes = {
    ...runnerHashes,
    runtime_hash: runnerHashes.runtime_hash ?? fingerprint(output),
    deterministic_fingerprint:
      runnerHashes.deterministic_fingerprint ?? fingerprint({ input: vector.input, output }),
  };
  const hashProbe = compareVector(vector, output, hashes);
  const structural = deepCompare(stripBounded(vector.canonical_output), stripBounded(output));

  const hash_mismatches = hashProbe.mismatches;
  const structural_summaries = summarizeDiffs(structural.diffs);

  const domains = domainFlags(family);
  if (state?.graph) domains.graph = true;
  if (state?.memory) domains.memory = true;
  if (state?.semantic) domains.semantic = true;
  if (state?.ontology) domains.ontology = true;
  if (state?.workflow) domains.workflow = true;
  if (state?.distributed) domains.distributed = true;
  if (state?.replay) domains.replay = true;
  if (state?.vm) domains.vm = true;
  if (state?.runtime) domains.runtime = true;

  const structure_pass = structural.equal;
  const hash_pass = hashProbe.pass;
  const pass = hash_pass;

  if (!structure_pass && structural_summaries.length) {
    hash_mismatches.push(...structural_summaries.slice(0, 5).map((s) => `structure: ${s}`));
  }

  return {
    family,
    vector_id: vector.id,
    pass,
    hash_pass,
    structure_pass,
    hash_mismatches,
    structural_diffs: structural.diffs,
    domains,
  };
}

export function runUniversalEquivalence(vectorsRoot: string): UniversalEquivalenceSummary {
  const families = listVectorFamilies(vectorsRoot);
  const probes: EquivalenceProbeResult[] = [];

  for (const family of families) {
    const data = loadVectorFamily(family);
    for (const vector of data.vectors) {
      probes.push(runProbe(family, vector));
    }
  }

  const passed = probes.filter((p) => p.pass).length;
  const failed = probes.length - passed;

  const subsystems: SubsystemSummary[] = Object.keys(SUBSYSTEM_MAP).map((name) => {
    const fams = SUBSYSTEM_MAP[name]!;
    const subset = probes.filter((p) => fams.includes(p.family));
    const ok = subset.filter((p) => p.pass).length;
    return {
      name,
      probes: subset.length,
      passed: ok,
      failed: subset.length - ok,
      pass_rate: subset.length ? Math.round((ok / subset.length) * 10000) / 100 : 0,
      status: subset.length === 0 ? "NOT_RUN" : ok === subset.length ? "PASS" : "FAIL",
    };
  });

  return {
    measured_at: new Date().toISOString(),
    vector_families: families.length,
    total_probes: probes.length,
    passed,
    failed,
    pass_rate: probes.length ? Math.round((passed / probes.length) * 10000) / 100 : 0,
    certification_eligible: false,
    subsystems,
    probes,
  };
}
