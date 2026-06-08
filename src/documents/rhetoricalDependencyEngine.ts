/**
 * Converted from Python: core/documents/rhetorical_dependency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { parseRhetoricalStructure } from "./rhetoricalParserEngine.js";

export function buildRhetoricalDependencies(text: any): any {
  var rhet: any = parseRhetoricalStructure(text);
  var units: any = py.get(rhet, "units", []);
  var deps: any[] = [];
  var i: any;
  for (i = 0; i < py.sub(py.len(units), 1); i++) {
    py.listAppend(deps, {"from": py.get(py.at(units, i), "title", `u${py.toStr(i)}`), "to": py.get(py.at(units, py.add(i, 1)), "title", `u${py.toStr(py.add(i, 1))}`), "relation": "elaborates"});
  }
  return {"dependencies": deps, "units": units, "evidence": ["discourse:rhetorical"]};
}
export { parseRhetoricalStructure };
