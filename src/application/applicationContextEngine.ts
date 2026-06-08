/**
 * Converted from Python: core/application/application_context_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildApplicationContext(url: any, state: any, identity: any): any {
  return {"url": url, "route": py.get(state, "route", url), "authenticated": py.get(state, "authenticated", false), "identity_profile": py.get(identity, "profile_id", "default"), "bounded": true};
}
