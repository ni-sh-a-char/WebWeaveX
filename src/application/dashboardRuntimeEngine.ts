/**
 * Converted from Python: core/application/dashboard_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_WIDGETS: any = 1000;
export function buildDashboardRuntime(html: any): any {
  var soup: any = py.soup(py.or2(html, () => ("")), "html.parser");
  var widgets: any[] = [];
  var tables: any[] = [];
  var filters: any[] = [];
  var charts: any[] = [];
  var node: any;
  for (node of py.iter(py.slice(soup.find_all(py.regex("widget|card|metric|kpi", "i")), null, MAX_WIDGETS))) {
    py.listAppend(widgets, {"text": py.slice(node.get_text(true), null, 500), "tag": node.name});
  }
  var table: any;
  for (table of py.iter(py.slice(soup.find_all("table"), null, MAX_WIDGETS))) {
    py.listAppend(tables, {"rows": py.len(table.find_all("tr")), "columns": py.len(table.find_all("th"))});
  }
  var select: any;
  for (select of py.iter(py.slice(soup.find_all("select"), null, MAX_WIDGETS))) {
    py.listAppend(filters, {"name": py.slice(py.toStr(py.get(select, "name", "")), null, 200)});
  }
  var canvas: any;
  for (canvas of py.iter(py.slice(soup.find_all("canvas"), null, MAX_WIDGETS))) {
    py.listAppend(charts, {"type": "canvas", "live": canvas.has_attr("data-live")});
  }
  return {"widgets": widgets, "metrics": py.iter(widgets).filter((w: any) => py.truthy(py.get(w, "text"))).map((w: any) => w), "tables": tables, "filters": filters, "charts": charts, "update_interval": 30, "bounded": true};
}
