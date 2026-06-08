/**
 * Converted from Python: core/spreadsheets/spreadsheet_extraction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_SHEETS: any = 500;
export let MAX_ROWS: any = 10000;
export function extractSpreadsheetStructure(workbook: any): any {
  var sheets: any[] = [];
  var name: any;
  var rows: any;
  for ([name, rows] of py.iter(py.slice([...py.iter(py.items(workbook))], null, MAX_SHEETS))) {
    py.listAppend(sheets, {"sheet": name, "rows": py.slice(rows, null, MAX_ROWS)});
  }
  return {"worksheets": sheets, "bounded": true};
}
