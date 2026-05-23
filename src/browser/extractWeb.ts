import { computeGlobalRuntimeFingerprint } from "../determinism/globalRuntimeFingerprint.js";
import { computeStableDomHash } from "../determinism/domStabilization.js";
import { buildRuntimeGraph } from "../graph/runtimeGraph.js";
import { computeKaalkaHashPayload } from "../crypto/kaalkaHash.js";
import { captureRuntime } from "./captureRuntime.js";
import { loadAuthenticatedRuntime } from "./authenticatedRuntime.js";
import type { ExtractionEnvelope } from "../contracts/runtimeContracts.js";

export type ExtractWebOptions = {
  authenticated?: boolean;
  sessionPath?: string;
  encryptionKey?: string;
  semanticRuntime?: boolean;
};

export async function extractWeb(
  url: string,
  options: ExtractWebOptions = {},
): Promise<ExtractionEnvelope> {
  const captured = await captureRuntime(url);
  let sessionMeta: Record<string, unknown> = {};
  if (options.authenticated && options.sessionPath && options.encryptionKey) {
    const session = loadAuthenticatedRuntime(options.sessionPath, options.encryptionKey);
    sessionMeta = { session_loaded: true, cookie_count: session.cookies?.length ?? 0 };
  }

  const graph = buildRuntimeGraph({
    browser: { url: captured.url, dom_hash: captured.dom_hash },
    network: captured.network.slice(0, 50),
  });

  const envelope: ExtractionEnvelope = {
    bounded: true,
    runtime: {
      available: captured.available,
      dom_stabilization: { stabilized_hash: captured.dom_hash },
      spa_stabilization: { stable_dom_hash: computeStableDomHash(captured.url) },
      session: sessionMeta,
    },
    browser_ir: {
      runtime_identity: computeKaalkaHashPayload({ url: captured.url, routes: captured.routes }),
      storage: captured.storage,
    },
    unified_runtime_graph: graph,
    pipeline_hash: computeKaalkaHashPayload({ url, kind: "web" }),
  };

  envelope.global_runtime_fingerprint = computeGlobalRuntimeFingerprint(envelope, graph);
  if (options.semanticRuntime) {
    envelope.semantic = { entities: [], bounded: true };
  }
  return envelope;
}
