/**
 * Converted from Python: core/application/navigation_semantic_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_NAV: any = 500;
export function buildNavigationSemantics(html: any, route: any, route_history: any = null): any {
  var soup: any = py.soup(py.or2(html, () => ("")), "html.parser");
  var menus: any[] = [];
  var breadcrumbs: any[] = [];
  var nav: any;
  for (nav of py.iter(py.slice(soup.find_all("nav"), null, MAX_NAV))) {
    var link: any;
    for (link of py.iter(nav.find_all("a"))) {
      var href: any = py.slice(py.toStr(py.get(link, "href", "")), null, 500);
      if (py.truthy(href)) {
        py.listAppend(menus, {"href": href, "text": py.slice(link.get_text(true), null, 200)});
      }
    }
  }
  var crumb: any;
  for (crumb of py.iter(py.slice(soup.find_all((value: any) => py.and2(value, () => (py.contains(value, "breadcrumb")))), null, MAX_NAV))) {
    py.listAppend(breadcrumbs, py.slice(crumb.get_text(true), null, 500));
  }
  var routes: any = [{"path": route, "order": 0}];
  if (py.truthy(route_history)) {
    routes = py.slice([...py.iter(route_history)], null, MAX_NAV);
  }
  var tabs: any[] = [];
  var tab: any;
  for (tab of py.iter(py.slice(soup.find_all({"role": "tab"}), null, MAX_NAV))) {
    py.listAppend(tabs, {"label": py.slice(tab.get_text(true), null, 200)});
  }
  return {"menus": py.sorted(menus, {key: ((item: any) => py.get(item, "href", "")) as (item: any) => any}), "breadcrumbs": breadcrumbs, "routes": routes, "spa_transitions": (py.len(routes) > 1), "tab_hierarchy": tabs, "bounded": true};
}
