/**
 * Converted from Python: core/internet/intelligence/trust_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";
import { computeTrust } from "../trustEngine.js";
import { reconstructCitationLineage } from "../citationLineageEngine.js";

export function scoreTrust(url: any, corroboration_count: any = 0, html_text: any = ""): any {
  var result: any = computeTrust(url, corroboration_count);
  if (py.truthy(html_text)) {
    var cites: any = reconstructCitationLineage(html_text);
    py.setItem(result, "citation_lineage", cites);
    py.setItem(result, "evidence", py.sorted(py.add(py.toSet(py.get(result, "evidence", [])), py.get(cites, "evidence", []))));
    py.setItem(result, "deterministic_inputs", py.sorted(py.add(py.toSet(py.get(result, "deterministic_inputs", [])), [`citations=${py.toStr(py.at(cites, "citation_count"))}`])));
  }
  return result;
}
export { computeTrust, reconstructCitationLineage };
