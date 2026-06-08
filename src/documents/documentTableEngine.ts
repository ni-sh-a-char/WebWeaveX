/**
 * Converted from Python: core/documents/document_table_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_TABLES: any = 1000;
export let MAX_ROWS: any = 10000;
export function extractDocumentTables(text: any): any {
  var tables: any[] = [];
  var rows: any[] = [];
  var line: any;
  for (line of py.iter(py.splitlines(text))) {
    if (py.contains(line, "|")) {
      py.listAppend(rows, py.iter(py.split(line, "|")).map((x: any) => py.strip(x)));
    }
  }
  if (py.truthy(rows)) {
    py.listAppend(tables, {"rows": py.slice(rows, null, MAX_ROWS)});
  }
  return {"tables": py.slice(tables, null, MAX_TABLES), "bounded": true};
}
