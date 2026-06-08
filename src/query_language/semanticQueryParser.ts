/**
 * Converted from Python: core/query_language/semantic_query_parser.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let SUPPORTED_KEYWORDS: any = new Set(["SELECT", "WHERE", "LIMIT"]);
export function parseSemanticQuery(query: any): any {
  var tokens: any = py.split(py.strip(query));
  var parsed: any = {"select": [], "where": {}, "limit": 100};
  var idx: any = 0;
  while ((idx < py.len(tokens))) {
    var token: any = String(py.at(tokens, idx)).toUpperCase();
    if (py.eq(token, "SELECT")) {
      idx = py.add(idx, 1);
      while ((idx < py.len(tokens))) {
        var current: any = py.at(tokens, idx);
        if (py.contains(SUPPORTED_KEYWORDS, String(current).toUpperCase())) {
          idx = py.sub(idx, 1);
          break;
        }
        py.listAppend(py.at(parsed, "select"), py.rstrip(current, ","));
        idx = py.add(idx, 1);
      }
    } else if (py.eq(token, "WHERE")) {
      idx = py.add(idx, 1);
      if ((py.add(idx, 2) < py.len(tokens))) {
        var field: any = py.at(tokens, idx);
        var operator: any = py.at(tokens, py.add(idx, 1));
        var value: any = py.at(tokens, py.add(idx, 2));
        if (py.eq(operator, "=")) {
          py.setItem(py.at(parsed, "where"), field, value);
        }
        idx = py.add(idx, 2);
      }
    } else if (py.eq(token, "LIMIT")) {
      idx = py.add(idx, 1);
      if ((idx < py.len(tokens))) {
        py.setItem(parsed, "limit", py.min([1000, py.max([1, py.toInt(py.at(tokens, idx))])]));
      }
    }
    idx = py.add(idx, 1);
  }
  return parsed;
}
