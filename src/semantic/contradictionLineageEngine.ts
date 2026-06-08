/**
 * Converted from Python: core/semantic/contradiction_lineage_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildLineage } from "../evidence/lineageEngine.js";
import { detectContradictionEvidence } from "../evidence/contradictionEvidenceEngine.js";

export function traceContradictionLineage(snippets: any): any {
  var detection: any = detectContradictionEvidence(snippets);
  var lineage: any = buildLineage([{"stage": "collect_snippets", "inputs": [], "outputs": py.range(py.len(py.or2(snippets, () => ([])))).map((i: any) => `snippet:${py.toStr(i)}`)}, {"stage": "detect_polarity", "inputs": ["snippets"], "outputs": py.iter(py.get(detection, "contradiction_pairs", [])).map((p: any) => py.toStr(p))}]);
  return {...(detection), "lineage": lineage};
}
export { buildLineage, detectContradictionEvidence };
