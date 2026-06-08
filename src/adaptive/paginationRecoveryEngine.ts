/**
 * Converted from Python: core/adaptive/pagination_recovery_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

let _NEXT_PATTERNS: any = ["a.next", "button.next", "[aria-label='Next']", "a:has-text('Next')"];
export function recoverPaginationFlow(broken_selector: any, html: any = ""): any {
  var candidates: any[] = [];
  var index: any;
  var selector: any;
  for ([index, selector] of py.enumerate(_NEXT_PATTERNS)) {
    if (py.truthy(_patternMatches(selector, html))) {
      py.listAppend(candidates, {"selector": selector, "priority": index});
    }
  }
  if (!py.truthy(candidates)) {
    py.listAppend(candidates, {"selector": broken_selector, "priority": 99});
  }
  var active: any = py.at(py.sorted(candidates, {key: ((item: any) => py.at(item, "priority")) as (item: any) => any}), 0);
  return {"original": broken_selector, "recovered_selector": py.at(active, "selector"), "candidates": candidates, "bounded": true};
}
export function _patternMatches(selector: any, html: any): any {
  var lowered: any = String(html).toLowerCase();
  if (py.contains(String(selector).toLowerCase(), "next")) {
    return py.contains(lowered, "next");
  }
  return py.contains(lowered, py.strip(selector, "#."));
}
