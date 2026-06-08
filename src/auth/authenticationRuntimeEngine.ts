/**
 * Converted from Python: core/auth/authentication_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { injectCookies } from "./cookieRuntimeEngine.js";
import { injectAuthTokens } from "./tokenRuntimeEngine.js";

export let MAX_LOGIN_STEPS: any = 100;
export function authenticateRuntime(page: any, credentials: any, config: any): any {
  var method: any = py.strip(py.toStr(py.get(config, "method", "cookie_injection")));
  if ((page === null || page === undefined)) {
    return {"authenticated": false, "method": method, "reason": "missing_page", "bounded": true};
  }
  var context: any = (((page ?? {}) as Record<string, any>)[String("context")] ?? null);
  if (py.eq(method, "form_login")) {
    var username_selector: any = py.toStr(py.get(config, "username_selector", "#username"));
    var password_selector: any = py.toStr(py.get(config, "password_selector", "#password"));
    var submit_selector: any = py.toStr(py.get(config, "submit_selector", "button[type='submit']"));
    if (((page !== null && page !== undefined && typeof page === "object" && (String("fill") in (page as object) || typeof (page as Record<string, unknown>)[String("fill")] === "function")) && (page !== null && page !== undefined && typeof page === "object" && (String("click") in (page as object) || typeof (page as Record<string, unknown>)[String("click")] === "function")))) {
      page.fill(username_selector, py.slice(py.toStr(py.get(credentials, "username", "")), null, 500));
      page.fill(password_selector, py.slice(py.toStr(py.get(credentials, "password", "")), null, 500));
      page.click(submit_selector);
    }
    return {"authenticated": true, "method": method, "bounded": true};
  }
  if (py.eq(method, "cookie_injection")) {
    var cookies: any = [...py.iter(py.get(credentials, "cookies", []))];
    injectCookies(context, cookies);
    return {"authenticated": true, "method": method, "cookie_count": py.len(cookies), "bounded": true};
  }
  if (py.eq(method, "token_injection")) {
    var tokens: any = [...py.iter(py.get(credentials, "tokens", []))];
    injectAuthTokens(page, tokens);
    return {"authenticated": true, "method": method, "token_count": py.len(tokens), "bounded": true};
  }
  if (py.eq(method, "persistent_auth_replay")) {
    var session: any = py.pyDict(py.get(credentials, "session", {}));
    injectCookies(context, [...py.iter(py.get(session, "cookies", []))]);
    injectAuthTokens(page, [...py.iter(py.get(session, "auth_tokens", []))]);
    return {"authenticated": true, "method": method, "bounded": true};
  }
  return {"authenticated": false, "method": method, "reason": "unsupported_method", "bounded": true};
}
export function rotateAuthenticatedSession(session: any): any {
  var rotated: any = py.pyDict(session);
  py.setItem(rotated, "rotation_index", py.add(py.toInt(py.get(session, "rotation_index", 0)), 1));
  py.setItem(rotated, "authenticated", true);
  py.setItem(rotated, "bounded", true);
  return rotated;
}
export { injectAuthTokens, injectCookies };
