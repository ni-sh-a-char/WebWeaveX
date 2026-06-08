/**
 * Converted from Python: core/auth/token_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_TOKENS: any = 500;
let _BEARER_RE: any = py.regex("Bearer\\s+([A-Za-z0-9\\-_.]+)", "i");
let _JWT_RE: any = py.regex("eyJ[A-Za-z0-9_-]+\\.[A-Za-z0-9_-]+\\.[A-Za-z0-9_-]+", "");
export function extractAuthTokens(page: any): any {
  var tokens: any[] = [];
  if ((page === null || page === undefined)) {
    return {"tokens": [], "bounded": true};
  }
  if ((page !== null && page !== undefined && typeof page === "object" && (String("_test_tokens") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_tokens")] === "function"))) {
    tokens = py.slice([...py.iter(page._test_tokens)], null, MAX_TOKENS);
    return {"tokens": py.sorted(tokens, {key: ((item: any) => [py.toStr(py.get(item, "type", "")), py.toStr(py.get(item, "value", ""))]) as (item: any) => any}), "bounded": true};
  }
  var headers: Record<string, any> = {};
  if ((page !== null && page !== undefined && typeof page === "object" && (String("_test_headers") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_headers")] === "function"))) {
    headers = py.pyDict(page._test_headers);
  }
  var authorization: any = py.toStr(py.get(headers, "Authorization", ""));
  var bearer_match: any = _BEARER_RE.search(authorization);
  if (py.truthy(bearer_match)) {
    py.listAppend(tokens, {"type": "bearer", "value": py.slice(bearer_match.group(1), null, 5000)});
  }
  var match: any;
  for (match of py.iter(_JWT_RE.findall(authorization))) {
    py.listAppend(tokens, {"type": "jwt", "value": py.slice(match, null, 5000)});
  }
  if ((page !== null && page !== undefined && typeof page === "object" && (String("_test_snapshot") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_snapshot")] === "function"))) {
    var storage: any = py.get(page._test_snapshot, "local_storage", {});
    var key: any;
    for (key of py.iter(py.sorted(py.keys(storage)))) {
      var value: any = py.toStr(py.at(storage, key));
      if (py.truthy(_JWT_RE.search(value))) {
        py.listAppend(tokens, {"type": "local_storage_auth", "name": key, "value": py.slice(value, null, 5000)});
      }
    }
  }
  return {"tokens": py.slice(py.sorted(tokens, {key: ((item: any) => [py.toStr(py.get(item, "type", "")), py.toStr(py.get(item, "name", "")), py.toStr(py.get(item, "value", ""))]) as (item: any) => any}), null, MAX_TOKENS), "bounded": true};
}
export function injectAuthTokens(page: any, tokens: any): any {
  var bounded: any = py.sorted(py.iter(py.slice(tokens, null, MAX_TOKENS)).map((token: any) => py.pyDict(token)), {key: ((item: any) => [py.toStr(py.get(item, "type", "")), py.toStr(py.get(item, "value", ""))]) as (item: any) => any});
  if ((page === null || page === undefined)) {
    return {"injected": false, "token_count": 0, "bounded": true};
  }
  var headers: Record<string, any> = {};
  var token: any;
  for (token of py.iter(bounded)) {
    var token_type: any = py.toStr(py.get(token, "type", ""));
    var value: any = py.toStr(py.get(token, "value", ""));
    if (py.eq(token_type, "bearer")) {
      py.setItem(headers, "Authorization", `Bearer ${py.toStr(value)}`);
    }
  }
  if ((page !== null && page !== undefined && typeof page === "object" && (String("_test_headers") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_headers")] === "function"))) {
    py.update(page._test_headers, headers);
  }
  if ((page !== null && page !== undefined && typeof page === "object" && (String("_test_tokens") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_tokens")] === "function"))) {
    page._test_tokens = bounded;
  }
  return {"injected": true, "token_count": py.len(bounded), "serialized": py.jsonDumps(bounded, {sortKeys: true, separators: [",", ":"] as [string, string]}), "bounded": true};
}
