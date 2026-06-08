/**
 * Converted from Python: core/identity/runtime_identity_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { fingerprintBrowserIdentity } from "./browserFingerprintEngine.js";

export function buildRuntimeIdentity(identity: any): any {
  return {"runtime_identity": fingerprintBrowserIdentity(identity), "profile_id": py.get(identity, "profile_id", "default"), "bounded": true};
}
export { fingerprintBrowserIdentity };
