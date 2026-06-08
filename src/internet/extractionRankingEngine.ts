/**
 * Converted from Python: core/internet/extraction_ranking_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function rankExtractions(results: any): any {
  function score(r: any): any {
    var txt: any = py.or2(py.get(r, "raw_text", ""), () => (""));
    var g: any = (((r !== null && typeof r === "object" && !Array.isArray(r) && !(r instanceof Set) && !(r instanceof Map))) ? py.get(py.get(r, "relationships", {}), "execution_graph", {}) : {});
    return [(-py.len(txt)), (-py.len(py.get(g, "edges", []))), py.toStr(py.get(r, "source_url", ""))];
  }
  return py.sorted(py.or2(results, () => ([])), {key: (score) as (item: any) => any});
}
