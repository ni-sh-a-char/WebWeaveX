import { buildRuntimeGraph } from "../graph/runtimeGraph.js";
import { computeGlobalRuntimeFingerprint } from "../determinism/globalRuntimeFingerprint.js";
import { computeKaalkaHashPayload } from "../crypto/kaalkaRuntime.js";
import type { ExtractionEnvelope } from "../contracts/runtimeContracts.js";
import { buildBrowserIdentity } from "./browserIdentity.js";
import { captureDom } from "./captureRuntime.js";
import { captureRuntimeSnapshot } from "./runtimeSnapshot.js";
import { restoreRuntimeSession, type RuntimeSessionEnvelope } from "./runtimeSession.js";
import { stabilizeSpaDom } from "./spaStabilizer.js";

export type ContinuationOptions = {
  sessionPath: string;
  encryptionKey: string;
  tick?: number;
};

export async function continueAuthenticatedRuntime(
  url: string,
  options: ContinuationOptions,
): Promise<ExtractionEnvelope> {
  const session = restoreRuntimeSession(options.sessionPath, options.encryptionKey);
  return extractWithSession(url, session, options.tick ?? 0);
}

export async function extractWithSession(
  url: string,
  session: RuntimeSessionEnvelope,
  tick = 0,
): Promise<ExtractionEnvelope> {
  const snapshot = await captureRuntimeSnapshot(url, tick, session);
  const identity = buildBrowserIdentity(snapshot);
  const dom = await captureDom(url);
  const spa = stabilizeSpaDom(dom.html, snapshot.routes[0] ?? "/");

  let playwrightApplied = false;
  try {
    const { chromium } = await import("playwright");
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
      extraHTTPHeaders: session.headers ?? {},
    });
    if (Array.isArray(session.cookies) && session.cookies.length > 0) {
      await context.addCookies(session.cookies as Parameters<typeof context.addCookies>[0]);
    }
    const page = await context.newPage();
    if (session.localStorage && Object.keys(session.localStorage).length > 0) {
      await page.addInitScript((storage) => {
        for (const [k, v] of Object.entries(storage as Record<string, string>)) {
          localStorage.setItem(k, v);
        }
      }, session.localStorage);
    }
    await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30_000 });
    playwrightApplied = true;
    await browser.close();
  } catch {
    playwrightApplied = false;
  }

  const graph = buildRuntimeGraph({
    browser: { url: snapshot.url, dom_hash: snapshot.dom_hash, identity: identity.runtime_identity },
    session: { session_id: session.session_id, continued: playwrightApplied },
    network: snapshot.network.slice(0, 50),
  });

  const envelope: ExtractionEnvelope = {
    bounded: true,
    runtime: {
      available: snapshot.available,
      dom_stabilization: { stabilized_hash: snapshot.dom_hash },
      spa_stabilization: spa,
      session: { session_id: session.session_id, continuation: playwrightApplied },
    },
    browser_ir: {
      runtime_identity: identity.runtime_identity,
      storage: snapshot.storage,
      profile_hash: identity.profile_hash,
    },
    unified_runtime_graph: graph,
    pipeline_hash: computeKaalkaHashPayload({ url, kind: "continuation", tick }),
  };
  envelope.global_runtime_fingerprint = computeGlobalRuntimeFingerprint(envelope, graph);
  return envelope;
}
