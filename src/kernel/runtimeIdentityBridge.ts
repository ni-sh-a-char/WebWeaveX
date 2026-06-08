/**
 * Converted from Python: core/kernel/runtime_identity_bridge.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildBrowserIdentity } from "../identity/browserIdentityEngine.js";

export function runIdentityPhase(identity: any): any {
  var built: any = buildBrowserIdentity(py.toStr(py.get(identity, "profile", "default")));
  return {"identity": {...(built), ...(identity)}, "bounded": true};
}
export { buildBrowserIdentity };
