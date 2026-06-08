/**
 * Converted from Python: core/documents/semantic_discourse_parser.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractRhetoricalStructure } from "./rhetoricalStructureEngine.js";
import { buildArgumentGraph } from "./argumentGraphEngine.js";

export function parseSemanticDiscourse(text: any): any {
  var rhet: any = extractRhetoricalStructure(text);
  var arg: any = buildArgumentGraph(text);
  return {"rhetorical": rhet, "argument": arg, "transitions": py.get(arg, "edges", []), "deterministic_inputs": py.add(py.get(rhet, "deterministic_inputs", []), [`args=${py.toStr(py.len(py.get(arg, "nodes", [])))}`])};
}
export { buildArgumentGraph, extractRhetoricalStructure };
