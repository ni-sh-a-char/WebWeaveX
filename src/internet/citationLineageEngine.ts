/**
 * Converted from Python: core/internet/citation_lineage_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildLineage } from "../evidence/lineageEngine.js";

let _CITATION_RE: any = py.regex("\\[([^\\]]+)\\]\\(([^)]+)\\)|https?://[^\\s\\)>]+", "");
export function reconstructCitationLineage(text: any): any {
  var citations: any[] = [];
  var m: any;
  for (m of py.iter(_CITATION_RE.finditer(py.or2(text, () => (""))))) {
    if (py.eq(m.lastindex, 2)) {
      py.listAppend(citations, {"label": m.group(1), "target": m.group(2)});
    } else {
      py.listAppend(citations, {"label": "", "target": m.group(0)});
    }
  }
  citations = py.slice(py.sorted(citations, {key: ((c: any) => py.at(c, "target")) as (item: any) => any}), null, 100);
  var lineage: any = buildLineage([{"stage": "citation_scan", "inputs": [], "outputs": py.iter(citations).map((c: any) => py.at(c, "target"))}]);
  return {"citations": citations, "citation_count": py.len(citations), "evidence": ["citation_lineage"], "lineage": lineage};
}
export { buildLineage };
