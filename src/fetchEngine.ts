/**
 * Converted from Python: core/fetch_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./runtime/pyCompat.js";
// from concurrent.futures import ... (unmapped)

export let DEFAULT_TIMEOUT: any = 5;
export function _buildUrl(query: any, source: any): any {
  var encoded: any = py.quotePlus(query);
  if (py.eq(source, "github")) {
    return `https://github.com/search?q=${py.toStr(encoded)}`;
  } else if (py.eq(source, "stackoverflow")) {
    return `https://stackoverflow.com/search?q=${py.toStr(encoded)}`;
  } else if (py.eq(source, "codepen")) {
    return `https://codepen.io/search/pens?q=${py.toStr(encoded)}`;
  } else if (py.eq(source, "docs")) {
    return `https://www.google.com/search?q=${py.toStr(encoded)}+documentation`;
  } else if (py.eq(source, "news")) {
    return `https://news.google.com/search?q=${py.toStr(encoded)}`;
  } else if (py.eq(source, "web")) {
    return `https://www.google.com/search?q=${py.toStr(encoded)}`;
  }
  return `https://www.google.com/search?q=${py.toStr(encoded)}`;
}
export function _safeFetch(url: any): any {
  var attempt: any;
  for (attempt = 0; attempt < 3; attempt++) {
    try {
      var req: any = py.urllibRequest(url, {"User-Agent": "Mozilla/5.0"});
      var response: any = py.urllibUrlopen(req, DEFAULT_TIMEOUT);
      var html: any = py.decode(response.read(), "utf-8");
      if (!(typeof html === "string")) {
        html = "";
      }
      if (!py.truthy(py.strip(html))) {
        continue;
      }
      return html;
    } catch (_e: any) {
      continue;
    }
  }
  return "";
}
export function _fetchSingle(item: any): any {
  var query: any = py.get(item, "query");
  var source: any = py.get(item, "source");
  var priority: any = py.get(item, "priority", 0);
  var input_signature: any = py.get(item, "input_signature", "");
  if ((!py.truthy(query) || !py.truthy(source))) {
    return null;
  }
  var url: any = _buildUrl(query, source);
  var html: any = _safeFetch(url);
  if (!(typeof html === "string")) {
    html = "";
  }
  return {"source": source, "query": query, "url": url, "html": html, "html_length": py.len(html), "success": (py.len(html) > 0), "has_content": (py.len(py.strip(html)) > 0), "input_signature": input_signature, "priority": priority};
}
export function fetchAll(query_bundle: any): any {
  if (!((query_bundle !== null && typeof query_bundle === "object" && !Array.isArray(query_bundle) && !(query_bundle instanceof Set) && !(query_bundle instanceof Map)))) {
    throw py.err("TypeError", "query_bundle must be dict");
  }
  if (!py.contains(query_bundle, "queries")) {
    throw py.err("ValueError", "Missing 'queries'");
  }
  var queries: any = py.at(query_bundle, "queries");
  var seen_urls: Set<any> = new Set();
  var executor: any = py.threadPoolExecutor();
  var futures: any = Object.fromEntries(py.iter(queries).map((item: any) => ([executor.submit(_fetchSingle, item), item] as [any, any])));
  var results: any[] = [];
  var future: any;
  for (future of py.iter(py.asCompleted(futures))) {
    var result: any = future.result();
    if ((py.truthy(result) && !py.contains(seen_urls, py.get(result, "url")))) {
      py.setAdd(seen_urls, py.get(result, "url", ""));
      py.listAppend(results, result);
    }
    if ((py.len(results) >= 10)) {
      break;
    }
  }
  py.sortInPlace(results, {key: ((x: any) => py.get(x, "priority", 0)) as (item: any) => any});
  return {"results": results, "total_fetched": py.len(results), "version": "v1_phase_5"};
}
export function validateFetchEngine(): any {
  var test_bundle: any = {"queries": [{"source": "web", "query": "test query", "priority": 1}]};
  var result: any = fetchAll(test_bundle);
  if (!((result !== null && typeof result === "object" && !Array.isArray(result) && !(result instanceof Set) && !(result instanceof Map)))) {
    throw py.err("RuntimeError", "Result is not dict");
  }
  if (!py.contains(result, "results")) {
    throw py.err("RuntimeError", "Missing results");
  }
  if (!(Array.isArray(py.at(result, "results")))) {
    throw py.err("RuntimeError", "Results not list");
  }
  return true;
}
