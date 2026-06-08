/**
 * Converted from Python: core/auth/session_restoration_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { injectCookies } from "./cookieRuntimeEngine.js";
import { injectAuthTokens } from "./tokenRuntimeEngine.js";
import { restoreBrowserSession } from "../session/browserSessionSnapshotEngine.js";

export function restoreAuthenticatedSession(context: any, page: any, session: any): any {
  var snapshot: any = {"cookies": [...py.iter(py.get(session, "cookies", []))], "local_storage": py.pyDict(py.get(session, "local_storage", {})), "session_storage": py.pyDict(py.get(session, "session_storage", {})), "headers": py.pyDict(py.get(session, "headers", {})), "auth_tokens": [...py.iter(py.get(session, "auth_tokens", []))], "origin": py.toStr(py.get(session, "origin", "")), "bounded": true};
  var restored: any = restoreBrowserSession(context, snapshot);
  injectCookies(context, py.at(snapshot, "cookies"));
  injectAuthTokens(page, [...py.iter(py.get(session, "auth_tokens", []))]);
  if (((page !== null && page !== undefined) && (page !== null && page !== undefined && typeof page === "object" && (String("_test_headers") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_headers")] === "function")))) {
    py.update(page._test_headers, py.pyDict(py.get(session, "headers", {})));
  }
  return {...(restored), "headers_applied": py.len(py.get(session, "headers", {})), "bounded": true};
}
export { injectAuthTokens, injectCookies, restoreBrowserSession };
