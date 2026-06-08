/**
 * Converted from Python: core/internet/authority_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

let _AUTHORITY_DOMAINS: any = ["github.com", "docs.python.org", "kubernetes.io", "pypi.org", "npmjs.com", "stackoverflow.com", "readthedocs.io"];
export function scoreAuthority(url: any): any {
  var u: any = String(py.or2(url, () => (""))).toLowerCase();
  var score: any = py.F(0.4);
  var evidence: any = ["baseline"];
  if (py.truthy(py.startswith(u, "https://"))) {
    score = py.add(score, py.F(0.15));
    py.listAppend(evidence, "tls");
  }
  var matched: any = py.iter(_AUTHORITY_DOMAINS).filter((d: any) => py.contains(u, d)).map((d: any) => d);
  if (py.truthy(matched)) {
    score = py.add(score, py.F(0.35));
    py.listAppend(evidence, "known_authority_domain");
  }
  if ((py.contains(u, "localhost") || py.contains(u, "127.0.0.1"))) {
    score = py.F(0.0);
    evidence = ["blocked_local"];
  }
  var authority_score: any = py.round(py.min([py.F(1.0), py.max([py.F(0.0), score])]), 3);
  return {"url": url, "authority_score": authority_score, "score": authority_score, "evidence": evidence, "basis": {"tls": py.startswith(u, "https://"), "known_domain": py.truthy(matched)}, "deterministic_inputs": py.sorted([`url=${py.toStr(py.slice(u, null, 80))}`, `matched_domains=${py.toStr(matched)}`])};
}
export function rankByAuthority(urls: any): any {
  var scored: any = py.iter(py.or2(urls, () => ([]))).map((u: any) => scoreAuthority(u));
  return py.sorted(scored, {key: ((x: any) => [(-py.at(x, "authority_score")), py.at(x, "url")]) as (item: any) => any});
}
