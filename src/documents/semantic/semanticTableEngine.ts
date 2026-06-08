/**
 * Converted from Python: core/documents/semantic/semantic_table_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractSemanticTables(text: any): any {
  var source: any = py.or2(text, () => (""));
  var rows: any[] = [];
  var line: any;
  for (line of py.iter(py.splitlines(source))) {
    if ((py.count(line, "|") >= 2)) {
      py.listAppend(rows, py.strip(line));
    }
  }
  var markdown_tables: any = py.sorted(py.toSet(rows));
  var html_tables: any = py.len(py.reFindall("<table\\b", source, "i"));
  return {"markdown_rows": markdown_tables, "html_table_count": html_tables};
}
