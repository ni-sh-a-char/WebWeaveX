/**
 * Converted from Python: core/identity/identity_replay_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { normalizeBrowserFingerprint } from "./browserEntropyEngine.js";
import { buildNavigatorRuntime } from "./navigatorRuntimeEngine.js";

export function replayBrowserIdentity(identity: any): any {
  var profile_id: any = py.toStr(py.get(identity, "profile_id", "default"));
  var navigator: any = buildNavigatorRuntime(profile_id);
  var restored: any = {...(identity), "navigator": navigator, "user_agent": py.get(identity, "user_agent", py.at(navigator, "user_agent")), "platform": py.get(identity, "platform", py.at(navigator, "platform")), "languages": py.get(identity, "languages", py.at(navigator, "languages")), "timezone": py.get(identity, "timezone", py.get(identity, "timezone", "UTC")), "canvas_fingerprint": py.get(identity, "canvas_fingerprint", ""), "entropy_profile": py.get(identity, "entropy_profile", "")};
  return {"identity": restored, "normalized": normalizeBrowserFingerprint(restored), "replayed": true, "bounded": true};
}
export { buildNavigatorRuntime, normalizeBrowserFingerprint };
