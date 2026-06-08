/**
 * Converted from Python: core/auth/csrf_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_CSRF: any = 200;
let _META_RE: any = py.regex("<meta[^>]+name=[\"\\']csrf-token[\"\\'][^>]+content=[\"\\']([^\"\\']+)[\"\\']", "i");
let _INPUT_RE: any = py.regex("<input[^>]+name=[\"\\']([^\"\\']*csrf[^\"\\']*)[\"\\'][^>]+value=[\"\\']([^\"\\']+)[\"\\']", "i");
export function extractCsrfTokens(page: any): any {
  var tokens: any[] = [];
  var html: any = "";
  if ((page === null || page === undefined)) {
    return {"tokens": [], "bounded": true};
  }
  if ((page !== null && page !== undefined && typeof page === "object" && (String("_test_html") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_html")] === "function"))) {
    html = py.toStr(page._test_html);
  } else if ((page !== null && page !== undefined && typeof page === "object" && (String("_test_snapshot") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_snapshot")] === "function"))) {
    html = py.toStr(py.get(page._test_snapshot, "html", ""));
  }
  var match: any;
  for (match of py.iter(py.slice(_META_RE.findall(html), null, MAX_CSRF))) {
    py.listAppend(tokens, {"source": "meta", "value": py.slice(match, null, 2000)});
  }
  var name: any;
  var value: any;
  for ([name, value] of py.iter(py.slice(_INPUT_RE.findall(html), null, MAX_CSRF))) {
    py.listAppend(tokens, {"source": "hidden_input", "name": py.slice(name, null, 200), "value": py.slice(value, null, 2000)});
  }
  var headers: any = (((page ?? {}) as Record<string, any>)[String("_test_headers")] ?? {});
  var header_name: any;
  for (header_name of py.iter(py.sorted(py.keys(headers)))) {
    if (py.contains(String(header_name).toLowerCase(), "csrf")) {
      py.listAppend(tokens, {"source": "header", "name": header_name, "value": py.slice(py.toStr(py.at(headers, header_name)), null, 2000)});
    }
  }
  return {"tokens": py.slice(py.sorted(tokens, {key: ((item: any) => [py.toStr(py.get(item, "source", "")), py.toStr(py.get(item, "name", "")), py.toStr(py.get(item, "value", ""))]) as (item: any) => any}), null, MAX_CSRF), "bounded": true};
}
