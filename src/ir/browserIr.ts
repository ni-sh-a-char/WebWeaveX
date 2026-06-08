/**
 * Converted from Python: core/ir/browser_ir.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { extractCsrfTokens } from "../auth/csrfRuntimeEngine.js";
import { computeKaalkaHashPayload } from "../crypto/kaalkaHashEngine.js";

export function _sessionFingerprint(session: any): any {
  var payload: any = py.or2(session, () => ({"cookies": [], "headers": {}, "auth_tokens": []}));
  return computeKaalkaHashPayload({"cookies": py.get(payload, "cookies", []), "headers": py.get(payload, "headers", {}), "auth_tokens": py.get(payload, "auth_tokens", []), "local_storage": py.get(payload, "local_storage", {}), "session_storage": py.get(payload, "session_storage", {})});
}
export function compileBrowserIr(runtime: any, dom: any, extraction: any, network: any, session: any = null, authenticated: any = false, page: any = null): any {
  session = py.or2(session, () => (py.get(runtime, "session", {})));
  var csrf: any = ((page !== null && page !== undefined) ? extractCsrfTokens(page) : {"tokens": []});
  var cookie_count: any = py.len(py.get(session, "cookies", []));
  var token_count: any = py.len(py.get(session, "auth_tokens", []));
  var csrf_detected: any = (py.len(py.get(csrf, "tokens", [])) > 0);
  var dom_stab: any = py.get(runtime, "dom_stabilization", {});
  var spa: any = py.get(runtime, "spa_stabilization", {});
  var requests: any = (((network !== null && typeof network === "object" && !Array.isArray(network) && !(network instanceof Set) && !(network instanceof Map))) ? py.get(network, "requests", []) : []);
  var network_fingerprint: any = computeKaalkaHashPayload({"count": py.len(requests), "types": py.sorted(py.toSet(py.iter(requests).filter((r: any) => ((r !== null && typeof r === "object" && !Array.isArray(r) && !(r instanceof Set) && !(r instanceof Map)))).map((r: any) => py.toStr(py.get(r, "resource_type", "")))))});
  var extraction_fp: any = computeKaalkaHashPayload({"links": ((Array.isArray(py.get(extraction, "links"))) ? py.slice(py.get(extraction, "links", []), null, 100) : []), "headings": ((Array.isArray(py.get(extraction, "headings"))) ? py.slice(py.get(extraction, "headings", []), null, 50) : [])});
  var runtime_identity: any = computeKaalkaHashPayload({"url": py.get(runtime, "url", ""), "title": py.get(runtime, "title", ""), "authenticated": authenticated, "dom_hash": py.get(dom_stab, "stabilized_hash", py.get(spa, "stable_dom_hash", "")), "spa_fingerprint": py.get(spa, "spa_fingerprint", ""), "network_fingerprint": network_fingerprint, "extraction_fingerprint": extraction_fp});
  var runtime_snapshot: any = {"url": py.get(runtime, "url", ""), "title": py.get(runtime, "title", ""), "authenticated": authenticated, "dom_stabilization": dom_stab, "spa_stabilization": {"spa_fingerprint": py.get(spa, "spa_fingerprint", ""), "frameworks": py.get(py.get(spa, "spa_convergence", {}), "frameworks", [])}, "network_fingerprint": network_fingerprint, "bounded": true};
  return {"ir": "browser", "runtime": runtime_snapshot, "runtime_full": runtime, "dom": dom, "extraction": extraction, "network": network, "authenticated": authenticated, "session_fingerprint": _sessionFingerprint(session), "cookie_count": cookie_count, "token_count": token_count, "csrf_detected": csrf_detected, "runtime_identity": runtime_identity, "bounded": true};
}
export { computeKaalkaHashPayload, extractCsrfTokens };
