/**
 * Converted from Python: core/browser/playwright_runtime.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractCookies, injectCookies } from "../auth/cookieRuntimeEngine.js";
import { restoreAuthenticatedSession } from "../auth/sessionRestorationEngine.js";
import { extractAuthTokens } from "../auth/tokenRuntimeEngine.js";
import { attachNetworkCapture } from "../network/networkCaptureEngine.js";
import { buildBrowserIdentity } from "../identity/browserIdentityOrchestrator.js";
import { captureBrowserSession } from "../session/browserSessionSnapshotEngine.js";
import { syncPlaywright as sync_playwright } from "./syncPlaywright.js";

export let MAX_HTML_SIZE: any = 10000000;
export let DEFAULT_TIMEOUT_MS: any = 30000;
export function launchAuthenticatedBrowser(session: any = null, identity_profile: any = null, persistent_identity: any = false): any {
  session = py.or2(session, () => ({"cookies": [], "headers": {}, "auth_tokens": [], "bounded": true}));
  var identity: any = py.or2(identity_profile, () => (buildBrowserIdentity("default")));
  if ((sync_playwright === null || sync_playwright === undefined)) {
    return {"available": false, "reason": "playwright_missing", "session": session, "identity": identity, "bounded": true};
  }
  var playwright: any = sync_playwright().start();
  var browser: any = playwright.chromium.launch(true);
  var screen: any = py.get(identity, "screen", {});
  var languages: any = py.get(identity, "languages", ["en-US"]);
  var context: any = browser.new_context(py.toStr(py.get(identity, "user_agent", "")), {"width": py.toInt(py.get(screen, "width", 1280)), "height": py.toInt(py.get(screen, "height", 720))}, (py.truthy(languages) ? py.toStr(py.at(languages, 0)) : "en-US"), py.toStr(py.get(identity, "timezone", "UTC")));
  var page: any = context.new_page();
  restoreAuthenticatedContext(context, page, session);
  return {"available": true, "playwright": playwright, "browser": browser, "context": context, "page": page, "session": session, "identity": identity, "persistent_identity": persistent_identity, "bounded": true};
}
export function restoreAuthenticatedContext(context: any, page: any, session: any): any {
  var headers: any = py.pyDict(py.get(session, "headers", {}));
  if (((page !== null && page !== undefined && typeof page === "object" && (String("set_extra_http_headers") in (page as object) || typeof (page as Record<string, unknown>)[String("set_extra_http_headers")] === "function")) && py.truthy(headers))) {
    page.set_extra_http_headers(Object.fromEntries(py.iter(py.sorted(py.items(headers))).map(([k, v]: any) => ([py.toStr(k), py.toStr(v)] as [any, any]))));
  }
  return restoreAuthenticatedSession(context, page, session);
}
export function persistAuthenticatedContext(context: any, page: any, session: any): any {
  var snapshot: any = captureBrowserSession(page, context);
  var cookies: any = extractCookies(context);
  var tokens: any = extractAuthTokens(page);
  var merged: any = {...(session), "cookies": py.get(cookies, "cookies", []), "auth_tokens": py.get(tokens, "tokens", []), "local_storage": py.get(snapshot, "local_storage", {}), "session_storage": py.get(snapshot, "session_storage", {}), "origin": py.get(snapshot, "origin", py.get(session, "origin", "")), "authenticated": true, "bounded": true};
  return merged;
}
export function renderPage(url: any, session: any = null, authenticated: any = false, identity_profile: any = null, persistent_identity: any = false, adaptive_runtime: any = false, selector_healing: any = false, modal_recovery: any = false, pagination_recovery: any = false): any {
  if ((sync_playwright === null || sync_playwright === undefined)) {
    return {"available": false, "reason": "playwright_missing", "bounded": true};
  }
  session = py.or2(session, () => ({}));
  try {
    var identity: any = py.or2(identity_profile, () => (buildBrowserIdentity("default")));
    if ((py.truthy(authenticated) || py.truthy(persistent_identity))) {
      var launched: any = launchAuthenticatedBrowser(session, identity, persistent_identity);
      if (!py.truthy(py.get(launched, "available"))) {
        return launched;
      }
      var playwright: any = py.at(launched, "playwright");
      var browser: any = py.at(launched, "browser");
      var context: any = py.at(launched, "context");
      var page: any = py.at(launched, "page");
    } else {
      playwright = sync_playwright().start();
      browser = playwright.chromium.launch(true);
      var screen: any = py.get(identity, "screen", {});
      var languages: any = py.get(identity, "languages", ["en-US"]);
      context = browser.new_context(py.toStr(py.get(identity, "user_agent", "")), {"width": py.toInt(py.get(screen, "width", 1280)), "height": py.toInt(py.get(screen, "height", 720))}, (py.truthy(languages) ? py.toStr(py.at(languages, 0)) : "en-US"), py.toStr(py.get(identity, "timezone", "UTC")));
      page = context.new_page();
      var headers: any = py.get(session, "headers", {});
      if ((((headers !== null && typeof headers === "object" && !Array.isArray(headers) && !(headers instanceof Set) && !(headers instanceof Map))) && py.truthy(headers))) {
        page.set_extra_http_headers(Object.fromEntries(py.iter(py.sorted(py.items(headers))).map(([k, v]: any) => ([py.toStr(k), py.toStr(v)] as [any, any]))));
      }
    }
    var network: any = attachNetworkCapture(page);
    page.goto(url, "networkidle", DEFAULT_TIMEOUT_MS);
    var html: any = page.content();
    var title: any = py.title(page);
    var updated_session: any = persistAuthenticatedContext(context, page, session);
    browser.close();
    playwright.stop();
    return {"available": true, "url": url, "title": title, "html": py.slice(html, null, MAX_HTML_SIZE), "network": {"requests": py.sorted(py.get(network, "requests", []), {key: ((item: any) => [py.toStr(py.get(item, "url")), py.toStr(py.get(item, "method"))]) as (item: any) => any}), "bounded": true}, "session": updated_session, "identity": identity, "authenticated": authenticated, "persistent_identity": persistent_identity, "adaptive_runtime": adaptive_runtime, "selector_healing": selector_healing, "modal_recovery": modal_recovery, "pagination_recovery": pagination_recovery, "bounded": true};
  } catch (exc: any) {
    return {"available": false, "reason": py.slice(py.toStr(exc), null, 500), "url": url, "bounded": true};
  }
}
export { attachNetworkCapture, buildBrowserIdentity, captureBrowserSession, extractAuthTokens, extractCookies, injectCookies, restoreAuthenticatedSession, sync_playwright };
