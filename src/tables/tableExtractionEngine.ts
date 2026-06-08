/**
 * Converted from Python: core/tables/table_extraction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_ROWS: any = 1000;
export function extractTables(layout_blocks: any): any {
  var tables: any[] = [];
  var current_rows: any[] = [];
  var block: any;
  for (block of py.iter(py.get(layout_blocks, "blocks", []))) {
    var text: any = py.get(block, "text", "");
    if (py.contains(text, "|")) {
      py.listAppend(current_rows, py.iter(py.split(text, "|")).map((x: any) => py.strip(x)));
    }
  }
  if (py.truthy(current_rows)) {
    py.listAppend(tables, {"rows": py.slice(current_rows, null, MAX_ROWS)});
  }
  return {"tables": tables, "bounded": true};
}
