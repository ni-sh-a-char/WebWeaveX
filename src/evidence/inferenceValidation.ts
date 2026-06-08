export function validateInference(
  claim: Record<string, unknown>,
  evidenceIds: string[],
): Record<string, unknown> {
  const valid = evidenceIds.length > 0 && Object.keys(claim).length > 0;
  return {
    valid,
    evidence_count: evidenceIds.length,
    bounded: true,
    reason: valid ? "evidence_bound" : "missing_evidence",
  };
}
