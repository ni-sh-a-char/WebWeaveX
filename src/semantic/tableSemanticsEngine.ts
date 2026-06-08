/**
 * Converted from Python: core/semantic/table_semantics_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let TABLE_KIND_RULES: any = [["invoice", py.regex("invoice|amount due|billing", "i")], ["ledger", py.regex("ledger|debit|credit|balance", "i")], ["analytics", py.regex("metric|kpi|conversion|funnel", "i")], ["transaction_log", py.regex("transaction|payment id|order id", "i")], ["audit_trail", py.regex("audit|actor|timestamp|change", "i")], ["monitoring_metrics", py.regex("cpu|memory|latency|uptime", "i")], ["user_list", py.regex("user|email|role|status", "i")], ["infrastructure_status", py.regex("host|node|cluster|health", "i")]];
export function extractTableSemantics(html: any = "", headers: any = null): any {
  var soup: any = py.soup(py.or2(html, () => ("")), "html.parser");
  headers = py.or2(headers, () => ([]));
  var tables: any[] = [];
  var index: any;
  var table: any;
  for ([index, table] of py.enumerate(py.slice(soup.find_all("table"), null, 1000))) {
    var header_cells: any = py.iter(py.slice(table.find_all("th"), null, 50)).map((cell: any) => cell.get_text(true));
    var context: any = py.slice(py.join(" ", py.add(header_cells, headers)), null, 2000);
    var kinds: any = py.iter(TABLE_KIND_RULES).filter(([kind, pattern]: any) => py.truthy(pattern.search(context))).map(([kind, pattern]: any) => kind);
    if (!py.truthy(kinds)) {
      kinds = ["generic_table"];
    }
    py.listAppend(tables, {"id": `table:${py.toStr(index)}`, "kinds": py.sorted(kinds), "rows": py.len(table.find_all("tr")), "columns": py.len(header_cells)});
  }
  return {"tables": tables, "primary_kind": (py.truthy(tables) ? py.at(py.at(py.at(tables, 0), "kinds"), 0) : "none"), "bounded": true};
}
