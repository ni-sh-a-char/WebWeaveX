/**
 * Converted from Python: core/session/browser_session_snapshot_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_COOKIES: any = 1000;
export let MAX_STORAGE_ITEMS: any = 1000;
export let MAX_HEADERS: any = 200;
export let MAX_TOKENS: any = 500;
let _LOCAL_STORAGE_SCRIPT: any = "\n() => {\n  const items = {};\n  const limit = Math.min(localStorage.length, 1000);\n  for (let i = 0; i < limit; i++) {\n    const key = localStorage.key(i);\n    if (key) {\n      items[key] = localStorage.getItem(key);\n    }\n  }\n  return items;\n}\n";
let _SESSION_STORAGE_SCRIPT: any = "\n() => {\n  const items = {};\n  const limit = Math.min(sessionStorage.length, 1000);\n  for (let i = 0; i < limit; i++) {\n    const key = sessionStorage.key(i);\n    if (key) {\n      items[key] = sessionStorage.getItem(key);\n    }\n  }\n  return items;\n}\n";
export function _emptySnapshot(): any {
  return {"cookies": [], "local_storage": {}, "session_storage": {}, "headers": {}, "auth_tokens": [], "origin": "", "bounded": true};
}
export function captureBrowserSession(page: any, context: any): any {
  if (((page === null || page === undefined) && (context === null || context === undefined))) {
    return _emptySnapshot();
  }
  if ((page !== null && page !== undefined && typeof page === "object" && (String("_test_snapshot") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_snapshot")] === "function"))) {
    var snapshot: any = py.pyDict(page._test_snapshot);
    py.setItem(snapshot, "bounded", true);
    return snapshot;
  }
  var cookies: any[] = [];
  var local_storage: Record<string, any> = {};
  var session_storage: Record<string, any> = {};
  var origin: any = "";
  if (((context !== null && context !== undefined) && (context !== null && context !== undefined && typeof context === "object" && (String("cookies") in (context as object) || typeof (context as Record<string, unknown>)[String("cookies")] === "function")))) {
    try {
      cookies = py.slice([...py.iter(context.cookies())], null, MAX_COOKIES);
    } catch (_e: any) {
      cookies = [];
    }
  }
  if ((page !== null && page !== undefined)) {
    try {
      origin = py.toStr(py.or2(page.url, () => ("")));
    } catch (_e: any) {
      origin = "";
    }
    if ((page !== null && page !== undefined && typeof page === "object" && (String("evaluate") in (page as object) || typeof (page as Record<string, unknown>)[String("evaluate")] === "function"))) {
      try {
        local_storage = py.pyDict(py.or2(page.evaluate(_LOCAL_STORAGE_SCRIPT), () => ({})));
      } catch (_e: any) {
        local_storage = {};
      }
      try {
        session_storage = py.pyDict(py.or2(page.evaluate(_SESSION_STORAGE_SCRIPT), () => ({})));
      } catch (_e: any) {
        session_storage = {};
      }
    }
  }
  local_storage = Object.fromEntries(py.iter(py.slice(py.sorted(py.items(local_storage)), null, MAX_STORAGE_ITEMS)).map(([k, v]: any) => ([py.toStr(k), py.slice(py.toStr(v), null, 5000)] as [any, any])));
  session_storage = Object.fromEntries(py.iter(py.slice(py.sorted(py.items(session_storage)), null, MAX_STORAGE_ITEMS)).map(([k, v]: any) => ([py.toStr(k), py.slice(py.toStr(v), null, 5000)] as [any, any])));
  return {"cookies": py.slice(py.sorted(py.iter(cookies).map((cookie: any) => py.pyDict(cookie)), {key: ((item: any) => [py.toStr(py.get(item, "name", "")), py.toStr(py.get(item, "domain", ""))]) as (item: any) => any}), null, MAX_COOKIES), "local_storage": local_storage, "session_storage": session_storage, "headers": {}, "auth_tokens": [], "origin": py.slice(origin, null, 2000), "bounded": true};
}
export function restoreBrowserSession(context: any, snapshot: any): any {
  if ((context === null || context === undefined)) {
    return {"restored": false, "reason": "missing_context", "bounded": true};
  }
  var cookies: any = py.slice([...py.iter(py.get(snapshot, "cookies", []))], null, MAX_COOKIES);
  if (((context !== null && context !== undefined && typeof context === "object" && (String("add_cookies") in (context as object) || typeof (context as Record<string, unknown>)[String("add_cookies")] === "function")) && py.truthy(cookies))) {
    try {
      context.add_cookies(cookies);
    } catch (exc: any) {
      return {"restored": false, "reason": py.slice(py.toStr(exc), null, 200), "bounded": true};
    }
  }
  if ((context !== null && context !== undefined && typeof context === "object" && (String("_test_pages") in (context as object) || typeof (context as Record<string, unknown>)[String("_test_pages")] === "function"))) {
    var page: any;
    for (page of py.iter(context._test_pages)) {
      if ((page !== null && page !== undefined && typeof page === "object" && (String("_test_snapshot") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_snapshot")] === "function"))) {
        page._test_snapshot = py.pyDict(snapshot);
      }
    }
  }
  return {"restored": true, "cookie_count": py.len(cookies), "bounded": true};
}
