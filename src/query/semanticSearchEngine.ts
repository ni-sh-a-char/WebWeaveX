/**
 * Converted from Python: core/query/semantic_search_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function semanticSearch(haystack: any, needle: any, max_hits: any = 50): any {
  var hits: any[] = [];
  var n: any = String(needle).toLowerCase();
  function walk(obj: any, path: any = ""): any {
    if ((py.len(hits) >= max_hits)) {
      return;
    }
    if (((obj !== null && typeof obj === "object" && !Array.isArray(obj) && !(obj instanceof Set) && !(obj instanceof Map)))) {
      var k: any;
      var v: any;
      for ([k, v] of py.items(obj)) {
        walk(v, (py.truthy(path) ? `${py.toStr(path)}.${py.toStr(k)}` : k));
      }
    } else if ((Array.isArray(obj))) {
      var i: any;
      for ([i, v] of py.enumerate(py.slice(obj, null, max_hits))) {
        walk(v, `${py.toStr(path)}[${py.toStr(i)}]`);
      }
    } else if (((typeof obj === "string") && py.contains(String(obj).toLowerCase(), n))) {
      py.listAppend(hits, {"path": path, "match": py.slice(obj, null, 120)});
    }
  }
  walk(haystack);
  return {"hits": hits, "count": py.len(hits), "bounded": (py.len(hits) <= max_hits)};
}
