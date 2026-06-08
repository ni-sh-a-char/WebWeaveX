import { computeDeterministicHash } from "../crypto/kaalkaRuntime.js";

export function buildParserCognitionEvidence(
  input: Record<string, unknown> | null = {},
): Record<string, unknown> {
  const src = input ?? {};
  const evidence: string[] = [];
  if (typeof src.evidence === "string") evidence.push(src.evidence);
  if (src.parser_evidence) evidence.push("parser_evidence");
  if (src.symbols) evidence.push("symbols");
  if (src.dependencies) evidence.push("dependencies");
  if (src.semantic_graph) evidence.push("semantic_graph");
  return {
    parser_evidence: evidence,
    cognition_id: computeDeterministicHash({ evidence, input: src }),
    bounded: true,
  };
}

export function orchestrateParserFleet(
  parsers: Array<Record<string, unknown>>,
): Record<string, unknown> {
  return {
    count: parsers.length,
    fleet_id: computeDeterministicHash({ parsers }),
    bounded: true,
    parsers,
  };
}
