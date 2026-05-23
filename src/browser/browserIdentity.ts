import { computeKaalkaHashPayload } from "../crypto/kaalkaRuntime.js";
import type { ExtractionEnvelope } from "../contracts/runtimeContracts.js";
import type { CapturedRuntime } from "./captureRuntime.js";
import type { RuntimeSnapshot } from "./runtimeSnapshot.js";

export type BrowserIdentity = {
  runtime_identity: string;
  profile_hash: string;
  storage_hash: string;
  route_fingerprint: string;
  bounded: boolean;
};

export function buildBrowserIdentity(
  captured: CapturedRuntime | RuntimeSnapshot,
): BrowserIdentity {
  const storage_hash = computeKaalkaHashPayload(captured.storage);
  const route_fingerprint = computeKaalkaHashPayload({ routes: captured.routes });
  const runtime_identity = computeKaalkaHashPayload({
    url: captured.url,
    dom_hash: captured.dom_hash,
    storage_hash,
    route_fingerprint,
  });
  return {
    runtime_identity,
    profile_hash: computeKaalkaHashPayload({ url: captured.url, network_len: captured.network.length }),
    storage_hash,
    route_fingerprint,
    bounded: true,
  };
}

export function identityFromExtraction(envelope: ExtractionEnvelope): BrowserIdentity {
  const ir = (envelope.browser_ir ?? {}) as Record<string, unknown>;
  const runtime = (envelope.runtime ?? {}) as Record<string, unknown>;
  const dom = (runtime.dom_stabilization as Record<string, unknown> | undefined)?.stabilized_hash ?? "";
  return {
    runtime_identity: String(ir.runtime_identity ?? ""),
    profile_hash: computeKaalkaHashPayload({ storage: ir.storage ?? {} }),
    storage_hash: computeKaalkaHashPayload(ir.storage ?? {}),
    route_fingerprint: computeKaalkaHashPayload({ dom }),
    bounded: true,
  };
}

export function compareBrowserIdentity(
  a: BrowserIdentity,
  b: BrowserIdentity,
): { equivalent: boolean; checks: Record<string, boolean>; bounded: boolean } {
  const checks = {
    runtime_identity: a.runtime_identity === b.runtime_identity,
    profile_hash: a.profile_hash === b.profile_hash,
    storage_hash: a.storage_hash === b.storage_hash,
    route_fingerprint: a.route_fingerprint === b.route_fingerprint,
  };
  return { equivalent: Object.values(checks).every(Boolean), checks, bounded: true };
}
