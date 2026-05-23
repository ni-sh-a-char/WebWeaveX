import { computeStableDomHash, stabilizeDomHtml } from "../determinism/domStabilization.js";

export function replayDomSnapshot(html: string): {
  stabilized: string;
  hash: string;
  bounded: boolean;
} {
  const stabilized = stabilizeDomHtml(html);
  return { stabilized, hash: computeStableDomHash(html), bounded: true };
}

export function validateDomReplayEquivalence(a: string, b: string): boolean {
  return computeStableDomHash(a) === computeStableDomHash(b);
}
