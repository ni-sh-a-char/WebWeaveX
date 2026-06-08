/**
 * Converted from Python: core/documents/instructional_flow_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractRhetoricalStructure } from "./rhetoricalStructureEngine.js";

export function extractInstructionalFlow(text: any): any {
  var rhet: any = extractRhetoricalStructure(text);
  var steps: any[] = [];
  var u: any;
  for (u of py.iter(py.at(rhet, "units"))) {
    if (py.eq(py.get(u, "type"), "heading")) {
      var title: any = String(py.toStr(py.get(u, "title", ""))).toLowerCase();
      if (py.any(py.iter(["step", "tutorial", "install", "setup", "prerequisite"]).map((k: any) => py.contains(title, k)))) {
        py.listAppend(steps, {"title": py.get(u, "title"), "line": py.get(u, "line")});
      } else if ((py.get(u, "level", 9) <= 2)) {
        py.listAppend(steps, {"title": py.get(u, "title"), "line": py.get(u, "line"), "implicit": true});
      }
    }
  }
  return {"steps": steps, "prerequisites": py.iter(py.slice(steps, null, (-1))).map((s: any) => py.at(s, "title")), "deterministic_inputs": [`steps=${py.toStr(py.len(steps))}`]};
}
export { extractRhetoricalStructure };
