/**
 * Converted from Python: core/knowledge/repository_knowledge_v2_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRepositoryKnowledgeV2(repo: any): any {
  var symbols: any = (((repo !== null && typeof repo === "object" && !Array.isArray(repo) && !(repo instanceof Set) && !(repo instanceof Map))) ? py.get(repo, "symbols", []) : []);
  var deps: any = (((repo !== null && typeof repo === "object" && !Array.isArray(repo) && !(repo instanceof Set) && !(repo instanceof Map))) ? py.get(repo, "dependencies", []) : []);
  var frameworks: any = (((repo !== null && typeof repo === "object" && !Array.isArray(repo) && !(repo instanceof Set) && !(repo instanceof Map))) ? py.get(repo, "frameworks", []) : []);
  return {"symbol_count": ((Array.isArray(symbols)) ? py.len(symbols) : 0), "dependency_count": ((Array.isArray(deps)) ? py.len(deps) : 0), "frameworks": ((Array.isArray(frameworks)) ? py.sorted(frameworks) : []), "evidence": "repository_payload"};
}
