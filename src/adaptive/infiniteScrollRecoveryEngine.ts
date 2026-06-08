/**
 * Converted from Python: core/adaptive/infinite_scroll_recovery_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_SCROLLS: any = 100;
export function recoverInfiniteScroll(page: any, previous_hashes: any = null): any {
  var hashes: any = [...py.iter(py.or2(previous_hashes, () => ([])))];
  var exhausted: any = false;
  var scrolls: any = 0;
  while (py.lt(scrolls, MAX_SCROLLS)) {
    if (((page !== null && page !== undefined) && (page !== null && page !== undefined && typeof page === "object" && (String("_test_scroll") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_scroll")] === "function")))) {
      page._test_scroll();
    }
    var current: any = py.toStr((((page ?? {}) as Record<string, any>)[String("_test_dom_hash")] ?? ""));
    scrolls = py.add(scrolls, 1);
    if ((py.truthy(hashes) && py.eq(current, py.at(hashes, (-1))))) {
      exhausted = true;
      break;
    }
    py.listAppend(hashes, current);
    if (((py.len(hashes) >= 3) && (py.eq(py.at(hashes, (-1)), py.at(hashes, (-2))) && py.eq(py.at(hashes, (-2)), py.at(hashes, (-3)))))) {
      exhausted = true;
      break;
    }
  }
  return {"scrolls": scrolls, "dom_hashes": py.slice(hashes, (-10), null), "exhausted": exhausted, "bounded": true};
}
