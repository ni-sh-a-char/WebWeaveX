/**
 * Converted from Python: core/documents/argument_structure_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { parseDiscourseStructure } from "./discourseParserEngine.js";

export function extractArgumentStructure(text: any): any {
  var structure: any = parseDiscourseStructure(text);
  var headings: any = py.get(py.at(structure, "discourse"), "headings", []);
  var claims: any[] = [];
  var i: any;
  var h: any;
  for ([i, h] of py.enumerate(headings)) {
    var role: any = (py.eq(i, 0) ? "claim" : "support");
    py.listAppend(claims, {"heading": h, "role": role});
  }
  return {"claims": claims, "structure_type": "heading_argument", "deterministic_inputs": [`claims=${py.toStr(py.len(claims))}`]};
}
export { parseDiscourseStructure };
