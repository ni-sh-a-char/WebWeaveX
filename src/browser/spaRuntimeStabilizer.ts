/**
 * Converted from Python: core/browser/spa_runtime_stabilizer.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { computeStableDomHash, stabilizeDomHtml } from "./domStabilizationEngine.js";
import { computeKaalkaHashPayload } from "../crypto/kaalkaHashEngine.js";

let _FRAMEWORK_MARKERS: any = {"react": ["data-reactroot", "__NEXT_DATA__", "react-root"], "vue": ["data-v-", "__VUE__", "id=\\\"app\\\""], "angular": ["ng-version", "ng-app", "_ngcontent"], "next": ["__NEXT_DATA__", "/_next/static"], "nuxt": ["__NUXT__", "/_nuxt/"], "remix": ["__remixContext", "remix-"], "electron": ["electron", "preload"]};
export function detectSpaFramework(html: any): any {
  var detected: any[] = [];
  var lower: any = String(html).toLowerCase();
  var name: any;
  var patterns: any;
  for ([name, patterns] of py.iter(py.sorted(py.items(_FRAMEWORK_MARKERS)))) {
    if (py.any(py.iter(patterns).map((pat: any) => py.or2(py.reSearch(pat, html, "i"), () => (py.contains(lower, String(pat).toLowerCase())))))) {
      py.listAppend(detected, name);
    }
  }
  return detected;
}
export function stabilizeRoute(url: any): any {
  var base: any = py.rstrip(py.at(py.split(py.at(py.split(url, "#"), 0), "?"), 0), "/");
  return py.or2(base, () => (url));
}
export function buildSpaStabilization(html: any, url: any, mutation_idle_ms: any = 0, network_idle: any = true): any {
  const _d1 = py.iter(stabilizeDomHtml(html)) as any[];
  var stable_html: any = _d1[0];
  var dom_meta: any = _d1[1];
  var frameworks: any = detectSpaFramework(html);
  var route: any = stabilizeRoute(url);
  var convergence: any = {"route": route, "frameworks": frameworks, "hydration_complete": true, "mutation_idle_ms": mutation_idle_ms, "network_idle": network_idle, "async_rendering_converged": py.and2(network_idle, () => ((mutation_idle_ms >= 0)))};
  return {"stable_html": stable_html, "dom_stabilization": dom_meta, "spa_convergence": convergence, "stable_dom_hash": computeStableDomHash(stable_html), "spa_fingerprint": computeKaalkaHashPayload({"route": route, "frameworks": frameworks, "dom_hash": py.get(dom_meta, "stabilized_hash", "")}), "bounded": true};
}
export function applySpaStabilizationToRuntime(runtime: any): any {
  var html: any = py.toStr(py.get(runtime, "html", ""));
  var url: any = py.toStr(py.get(runtime, "url", ""));
  var spa: any = buildSpaStabilization(html, url, 0, py.truthy(py.get(py.get(runtime, "network", {}), "bounded", true)));
  return {...(runtime), "html": py.at(spa, "stable_html"), "dom_stabilization": py.at(spa, "dom_stabilization"), "spa_stabilization": spa, "bounded": true};
}
export { computeKaalkaHashPayload, computeStableDomHash, stabilizeDomHtml };
