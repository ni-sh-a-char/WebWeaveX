/**
 * Converted from Python: core/interaction/pagination_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_PAGES: any = 100;
export function extractPaginatedContent(page: any, next_selector: any): any {
  var visited: Set<any> = new Set();
  var pages: any[] = [];
  var current_url: any = "";
  if ((page !== null && page !== undefined)) {
    current_url = py.toStr((((page ?? {}) as Record<string, any>)[String("_test_url")] ?? (((page ?? {}) as Record<string, any>)[String("url")] ?? "")));
  }
  while ((py.len(pages) < MAX_PAGES)) {
    if (py.contains(visited, current_url)) {
      break;
    }
    py.setAdd(visited, current_url);
    py.listAppend(pages, {"url": current_url, "order": py.len(pages)});
    if (!py.truthy(next_selector)) {
      break;
    }
    if (((page !== null && page !== undefined) && (page !== null && page !== undefined && typeof page === "object" && (String("click") in (page as object) || typeof (page as Record<string, unknown>)[String("click")] === "function")))) {
      try {
        page.click(next_selector);
      } catch (_e: any) {
        break;
      }
    }
    var next_url: any = py.toStr((((page ?? {}) as Record<string, any>)[String("_test_next_url")] ?? ""));
    if ((!py.truthy(next_url) || py.eq(next_url, current_url))) {
      if ((page !== null && page !== undefined && typeof page === "object" && (String("_test_paginate") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_paginate")] === "function"))) {
        next_url = page._test_paginate(current_url);
      }
    }
    if ((!py.truthy(next_url) || py.contains(visited, next_url))) {
      break;
    }
    current_url = next_url;
    if ((page !== null && page !== undefined && typeof page === "object" && (String("_test_url") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_url")] === "function"))) {
      page._test_url = current_url;
    }
  }
  return {"pages": pages, "visited_count": py.len(visited), "loop_prevented": (py.len(pages) < MAX_PAGES), "bounded": true};
}
