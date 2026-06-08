/**
 * Converted from Python: core/knowledge/internet_knowledge_v2_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildInternetKnowledgeV2(sources: any): any {
  var urls: any = py.sorted(py.toSet(py.iter(py.or2(sources, () => ([]))).filter((u: any) => py.truthy(u)).map((u: any) => py.strip(py.toStr(u)))));
  return {"source_count": py.len(urls), "sources": py.slice(urls, null, 100), "evidence": "canonical_urls"};
}
