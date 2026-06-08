/**
 * Converted from Python: core/documents/intelligence/table_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function extractTables(text: any): any {
  var rows: any = py.reFindall("^\\|.*\\|$", py.or2(text, () => ("")), "m");
  return {"tables": py.sorted(py.toSet(rows))};
}
