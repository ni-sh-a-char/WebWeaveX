/**
 * Replay equivalence — typed facade over the certified engine
 * (see specification/replay for the authoritative contract).
 *
 * The specification defines exactly three replay checks: graph_hash,
 * global_fingerprint and browser_identity. Earlier hand-written revisions
 * added extra checks (dom/semantic/memory) — removed as spec drift.
 */
import { validateReplayEquivalence as engineValidate } from "./replayEquivalenceEngine.js";
import type { ExtractionEnvelope } from "../contracts/runtimeContracts.js";

export function validateReplayEquivalence(
  original: ExtractionEnvelope,
  replayed: ExtractionEnvelope,
): { equivalent: boolean; checks: Array<Record<string, unknown>>; bounded: boolean } {
  return engineValidate(original, replayed) as {
    equivalent: boolean;
    checks: Array<Record<string, unknown>>;
    bounded: boolean;
  };
}
