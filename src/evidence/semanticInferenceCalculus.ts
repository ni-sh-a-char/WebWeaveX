/**
 * Formal inference calculus — faithful port of core/evidence/semantic_inference_calculus.py.
 * Hand-written production module (protected).
 */
import * as py from "../runtime/pyCompat.js";

/** Formal inference: inferred keys only when evidence threshold met. */
export function inferFromEvidence(
  observed: Record<string, unknown>,
  evidence: unknown[],
  min_evidence = 1,
): Record<string, unknown> {
  const ev = py.sorted(
    new Set(py.iter(evidence).filter((e) => py.truthy(e)).map((e) => py.toStr(e))),
  );
  const allowed = py.len(ev) >= min_evidence;
  const inferred = allowed ? { ...(observed ?? {}) } : {};
  return {
    inferred,
    allowed,
    evidence_count: py.len(ev),
    rule: "inference_requires_evidence",
    deterministic_inputs: [`evidence_count=${py.len(ev)}`, `min=${min_evidence}`],
  };
}
