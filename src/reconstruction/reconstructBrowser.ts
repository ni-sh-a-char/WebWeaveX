import type { ExtractionEnvelope } from "../contracts/runtimeContracts.js";
import { identityFromExtraction } from "../browser/browserIdentity.js";
import type { RuntimeSessionEnvelope } from "../browser/runtimeSession.js";

export type ReconstructedBrowserState = {
  runtime_identity: string;
  tabs: Array<{ id: string; path: string }>;
  navigation_history: Array<{ path: string; order: number }>;
  session: Record<string, unknown>;
  storage: Record<string, unknown>;
  bounded: boolean;
};

export function reconstructBrowserState(
  extraction: ExtractionEnvelope,
  session?: RuntimeSessionEnvelope,
): ReconstructedBrowserState {
  const ir = (extraction.browser_ir ?? {}) as Record<string, unknown>;
  const identity = identityFromExtraction(extraction);
  const routes =
    ((ir.routes as Record<string, unknown> | undefined)?.history as Array<{ path?: string }>) ?? [];
  const tabs = routes.length
    ? routes.map((r, i) => ({ id: `tab:${i}`, path: String(r.path ?? "/") }))
    : [{ id: "tab:0", path: "/" }];

  return {
    runtime_identity: identity.runtime_identity,
    tabs: tabs.sort((a, b) => a.id.localeCompare(b.id)),
    navigation_history: tabs.map((t, order) => ({ path: t.path, order })),
    session: {
      session_id: session?.session_id ?? (extraction.runtime as Record<string, unknown>)?.session,
      bounded: true,
    },
    storage: (ir.storage as Record<string, unknown>) ?? {},
    bounded: true,
  };
}
