/**
 * Converted from Python: core/interaction/infinite_scroll_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { computeKaalkaHash } from "../crypto/kaalkaHashEngine.js";

export let MAX_SCROLLS: any = 100;
export function _domHash(page: any): any {
  if (((page !== null && page !== undefined && typeof page === "object" && (String("_test_dom_hash") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_dom_hash")] === "function")) && py.truthy(page._test_dom_hash))) {
    return py.toStr(page._test_dom_hash);
  }
  var html: any = "";
  if ((page !== null && page !== undefined && typeof page === "object" && (String("_test_html") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_html")] === "function"))) {
    html = py.toStr(page._test_html);
  } else if (((page !== null && page !== undefined && typeof page === "object" && (String("content") in (page as object) || typeof (page as Record<string, unknown>)[String("content")] === "function")) && (typeof page.content === "function"))) {
    try {
      html = py.toStr(page.content());
    } catch (_e: any) {
      html = "";
    }
  }
  return computeKaalkaHash(py.slice(html, null, 1000000));
}
export function extractInfiniteScroll(page: any): any {
  var scrolls: any = 0;
  var chunks: any[] = [];
  var previous_hash: any = _domHash(page);
  var stable_rounds: any = 0;
  while (py.lt(scrolls, MAX_SCROLLS)) {
    if (((page !== null && page !== undefined) && (page !== null && page !== undefined && typeof page === "object" && (String("evaluate") in (page as object) || typeof (page as Record<string, unknown>)[String("evaluate")] === "function")))) {
      try {
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)");
      } catch (_e: any) {
      }
    }
    if ((page !== null && page !== undefined && typeof page === "object" && (String("_test_scroll") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_scroll")] === "function"))) {
      page._test_scroll();
    }
    scrolls = py.add(scrolls, 1);
    var current_hash: any = _domHash(page);
    py.listAppend(chunks, {"scroll": scrolls, "dom_hash": current_hash});
    if (py.eq(current_hash, previous_hash)) {
      stable_rounds = py.add(stable_rounds, 1);
    } else {
      stable_rounds = 0;
    }
    if ((stable_rounds >= 2)) {
      break;
    }
    previous_hash = current_hash;
  }
  return {"scrolls": scrolls, "chunks": chunks, "stopped_on_stable_dom": (stable_rounds >= 2), "bounded": true};
}
export { computeKaalkaHash };
