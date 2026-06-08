import type { DeepDiff } from "./deepCompare.js";

export type EquivalenceProbeResult = {
  family: string;
  vector_id: string;
  pass: boolean;
  hash_pass: boolean;
  structure_pass: boolean;
  hash_mismatches: string[];
  structural_diffs: DeepDiff[];
  domains: {
    runtime: boolean;
    memory: boolean;
    graph: boolean;
    semantic: boolean;
    ontology: boolean;
    workflow: boolean;
    distributed: boolean;
    replay: boolean;
    vm: boolean;
  };
};

export type SubsystemSummary = {
  name: string;
  probes: number;
  passed: number;
  failed: number;
  pass_rate: number;
  status: "PASS" | "FAIL" | "NOT_RUN";
};

export type UniversalEquivalenceSummary = {
  measured_at: string;
  vector_families: number;
  total_probes: number;
  passed: number;
  failed: number;
  pass_rate: number;
  certification_eligible: false;
  subsystems: SubsystemSummary[];
  probes: EquivalenceProbeResult[];
};
