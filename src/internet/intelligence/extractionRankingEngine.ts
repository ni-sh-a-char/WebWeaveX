/**
 * Converted from Python: core/internet/intelligence/extraction_ranking_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function rankExtractionResults(results: any): any {
  function key(r: any): any {
    var txt: any = py.len(py.get(py.or2(r, () => ({})), "raw_text", ""));
    var edges: any = py.len(py.get(py.get(py.get(py.or2(r, () => ({})), "relationships", {}), "execution_graph", {}), "edges", []));
    return [(-txt), (-edges), py.toStr(py.get(py.or2(r, () => ({})), "source_url", ""))];
  }
  return py.sorted(py.or2(results, () => ([])), {key: (key) as (item: any) => any});
}
