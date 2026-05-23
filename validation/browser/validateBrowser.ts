import {
  buildBrowserIdentity,
  compareBrowserIdentity,
} from "../../src/browser/browserIdentity.js";
import { createRuntimeSession, persistRuntimeSession, restoreRuntimeSession } from "../../src/browser/runtimeSession.js";
import { captureRuntimeSnapshot } from "../../src/browser/runtimeSnapshot.js";
import { stabilizeSpaDom } from "../../src/browser/spaStabilizer.js";

async function main(): Promise<void> {
  const session = createRuntimeSession({ cookies: [], headers: { "x-test": "1" } });
  const tmp = `${process.cwd()}/validation/browser/.session-test.kaalka`;
  persistRuntimeSession(tmp, session, "browser-test-key");
  const restored = restoreRuntimeSession(tmp, "browser-test-key");

  const snapshot = await captureRuntimeSnapshot("https://example.com", 0, session);
  const identity = buildBrowserIdentity(snapshot);
  const identity2 = buildBrowserIdentity(snapshot);
  const spa = stabilizeSpaDom("<div data-reactroot>hello</div>", "/");

  const results = {
    session_roundtrip: restored.session_id === session.session_id,
    snapshot_bounded: snapshot.bounded === true,
    identity_stable: compareBrowserIdentity(identity, identity2).equivalent,
    spa_framework: spa.framework === "react",
    spa_hash: spa.stable_dom_hash.length > 0,
  };

  console.log("PASS", results);
  if (!Object.values(results).every(Boolean)) process.exit(1);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
