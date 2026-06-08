/**
 * Converted from Python: core/interaction/tab_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_TABS: any = 50;
export function captureTabs(context: any): any {
  var tabs: any[] = [];
  if ((context === null || context === undefined)) {
    return {"tabs": [], "bounded": true};
  }
  if ((context !== null && context !== undefined && typeof context === "object" && (String("_test_tabs") in (context as object) || typeof (context as Record<string, unknown>)[String("_test_tabs")] === "function"))) {
    return {"tabs": py.slice([...py.iter(context._test_tabs)], null, MAX_TABS), "bounded": true};
  }
  if ((context !== null && context !== undefined && typeof context === "object" && (String("pages") in (context as object) || typeof (context as Record<string, unknown>)[String("pages")] === "function"))) {
    var index: any;
    var page: any;
    for ([index, page] of py.enumerate(py.slice(context.pages(), null, MAX_TABS))) {
      var url: any = "";
      if ((page !== null && page !== undefined && typeof page === "object" && (String("url") in (page as object) || typeof (page as Record<string, unknown>)[String("url")] === "function"))) {
        try {
          url = py.toStr(page.url);
        } catch (_e: any) {
          url = "";
        }
      }
      py.listAppend(tabs, {"index": index, "url": py.slice(url, null, 2000)});
    }
  }
  return {"tabs": tabs, "bounded": true};
}
export function switchTab(context: any, index: any): any {
  var bounded_index: any = py.min([py.max([py.toInt(index), 0]), py.sub(MAX_TABS, 1)]);
  if (((context !== null && context !== undefined) && (context !== null && context !== undefined && typeof context === "object" && (String("_test_active_tab") in (context as object) || typeof (context as Record<string, unknown>)[String("_test_active_tab")] === "function")))) {
    context._test_active_tab = bounded_index;
  }
  var pages: any[] = [];
  if (((context !== null && context !== undefined) && (context !== null && context !== undefined && typeof context === "object" && (String("pages") in (context as object) || typeof (context as Record<string, unknown>)[String("pages")] === "function")))) {
    try {
      pages = [...py.iter(context.pages())];
    } catch (_e: any) {
      pages = [];
    }
  }
  if ((py.truthy(pages) && (bounded_index < py.len(pages)))) {
    var page: any = py.at(pages, bounded_index);
    if ((page !== null && page !== undefined && typeof page === "object" && (String("bring_to_front") in (page as object) || typeof (page as Record<string, unknown>)[String("bring_to_front")] === "function"))) {
      page.bring_to_front();
    }
  }
  return {"active_tab": bounded_index, "bounded": true};
}
