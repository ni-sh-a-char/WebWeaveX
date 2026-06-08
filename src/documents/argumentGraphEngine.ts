/**
 * Converted from Python: core/documents/argument_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractRhetoricalStructure } from "./rhetoricalStructureEngine.js";

export function buildArgumentGraph(text: any): any {
  var rhet: any = extractRhetoricalStructure(text);
  var headings: any = py.iter(py.at(rhet, "units")).filter((u: any) => py.eq(py.get(u, "type"), "heading")).map((u: any) => u);
  var nodes: any = py.enumerate(headings).map(([i, h]: any) => ({"id": `h${py.toStr(i)}`, "role": (py.eq(i, 0) ? "claim" : "support"), "title": py.get(h, "title", "")}));
  var edges: any = py.range(py.sub(py.len(nodes), 1)).map((i: any) => ({"from": py.at(py.at(nodes, i), "id"), "to": py.at(py.at(nodes, py.add(i, 1)), "id")}));
  return {"nodes": nodes, "edges": edges, "deterministic_inputs": [`nodes=${py.toStr(py.len(nodes))}`]};
}
export { extractRhetoricalStructure };
