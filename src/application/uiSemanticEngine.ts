/**
 * Converted from Python: core/application/ui_semantic_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_ITEMS: any = 1000;
export function extractUiSemantics(html: any): any {
  var soup: any = py.soup(py.or2(html, () => ("")), "html.parser");
  var semantics: any = {"dashboards": [], "forms": [], "navigation_menus": [], "tables": [], "charts": [], "filters": [], "search_bars": [], "sidebars": [], "tabs": []};
  var form: any;
  for (form of py.iter(py.slice(soup.find_all("form"), null, MAX_ITEMS))) {
    py.listAppend(py.at(semantics, "forms"), {"action": py.slice(py.toStr(py.get(form, "action", "")), null, 500), "id": py.slice(py.toStr(py.get(form, "id", "")), null, 200)});
  }
  var nav: any;
  for (nav of py.iter(py.slice(soup.find_all(["nav", "header"]), null, MAX_ITEMS))) {
    py.listAppend(py.at(semantics, "navigation_menus"), {"tag": nav.name, "links": py.len(nav.find_all("a"))});
  }
  var table: any;
  for (table of py.iter(py.slice(soup.find_all("table"), null, MAX_ITEMS))) {
    py.listAppend(py.at(semantics, "tables"), {"rows": py.len(table.find_all("tr"))});
  }
  if (py.truthy(py.reSearch("dashboard|metrics|kpi", html, "i"))) {
    py.listAppend(py.at(semantics, "dashboards"), {"detected": true});
  }
  var canvas: any;
  for (canvas of py.iter(py.slice(soup.find_all("canvas"), null, MAX_ITEMS))) {
    py.listAppend(py.at(semantics, "charts"), {"type": "canvas"});
  }
  var node: any;
  for (node of py.iter(py.slice(soup.find_all(["input", "select"]), null, MAX_ITEMS))) {
    var node_type: any = String(py.toStr(py.get(node, "type", ""))).toLowerCase();
    if ((py.contains(new Set(["search", "text"]), node_type) && py.contains(String(py.toStr(py.get(node, "name", ""))).toLowerCase(), "search"))) {
      py.listAppend(py.at(semantics, "search_bars"), {"name": py.slice(py.toStr(py.get(node, "name", "")), null, 200)});
    } else if (py.contains(new Set(["select", "checkbox", "radio"]), node_type)) {
      py.listAppend(py.at(semantics, "filters"), {"type": node_type, "name": py.slice(py.toStr(py.get(node, "name", "")), null, 200)});
    }
  }
  var aside: any;
  for (aside of py.iter(py.slice(soup.find_all("aside"), null, MAX_ITEMS))) {
    py.listAppend(py.at(semantics, "sidebars"), {"tag": "aside"});
  }
  var tab: any;
  for (tab of py.iter(py.slice(soup.find_all({"role": "tab"}), null, MAX_ITEMS))) {
    py.listAppend(py.at(semantics, "tabs"), {"label": py.slice(tab.get_text(true), null, 200)});
  }
  return {"semantics": semantics, "bounded": true};
}
