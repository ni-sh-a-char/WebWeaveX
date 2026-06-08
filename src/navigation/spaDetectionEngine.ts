/**
 * Converted from Python: core/navigation/spa_detection_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

let _SPA_MARKERS: any = ["react", "vue", "angular", "__NEXT_DATA__", "history.pushState", "hashchange"];
export function detectSinglePageApplication(page: any): any {
  var html: any = "";
  if ((page !== null && page !== undefined)) {
    if ((page !== null && page !== undefined && typeof page === "object" && (String("_test_spa_markers") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_spa_markers")] === "function"))) {
      var markers: any = [...py.iter(page._test_spa_markers)];
      return {"spa": (py.len(markers) > 0), "markers": py.sorted(markers), "history_api": py.contains(markers, "history.pushState"), "hash_routing": py.contains(markers, "hashchange"), "bounded": true};
    }
    if ((page !== null && page !== undefined && typeof page === "object" && (String("_test_html") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_html")] === "function"))) {
      html = String(py.toStr(page._test_html)).toLowerCase();
    }
  }
  markers = [];
  var marker: any;
  for (marker of py.iter(_SPA_MARKERS)) {
    if (py.contains(html, String(marker).toLowerCase())) {
      py.listAppend(markers, marker);
    }
  }
  var history_api: any = py.truthy(py.reSearch("history\\.pushstate", html, "i"));
  var hash_routing: any = py.or2(py.contains(html, "#/"), () => (py.contains(html, "hashchange")));
  return {"spa": py.or2(py.truthy(markers), () => (py.or2(history_api, () => (hash_routing)))), "markers": py.sorted(py.toSet(markers)), "history_api": history_api, "hash_routing": hash_routing, "bounded": true};
}
