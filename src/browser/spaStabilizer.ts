import {
  computeSpaFingerprint,
  computeStableDomHash,
  stabilizeDomHtml,
} from "../determinism/domStabilization.js";
import { computeKaalkaHashPayload } from "../crypto/kaalkaRuntime.js";

const FRAMEWORK_MARKERS = [
  { name: "react", pattern: /data-reactroot|__REACT_DEVTOOLS/i },
  { name: "vue", pattern: /data-v-[a-z0-9]+|__VUE__/i },
  { name: "angular", pattern: /ng-version|_ngcontent/i },
  { name: "svelte", pattern: /svelte-[a-z0-9-]+/i },
];

export type SpaStabilizationResult = {
  framework: string | null;
  stabilized_html: string;
  stable_dom_hash: string;
  spa_fingerprint: string;
  route_hash: string;
  bounded: boolean;
};

export function detectSpaFramework(html: string): string | null {
  for (const marker of FRAMEWORK_MARKERS) {
    if (marker.pattern.test(html)) return marker.name;
  }
  return null;
}

export function stabilizeSpaDom(html: string, route = "/"): SpaStabilizationResult {
  const stabilized_html = stabilizeDomHtml(html);
  const stable_dom_hash = computeStableDomHash(html);
  const spa_fingerprint = computeSpaFingerprint(html);
  const route_hash = computeKaalkaHashPayload({ route, stable_dom_hash });
  return {
    framework: detectSpaFramework(html),
    stabilized_html,
    stable_dom_hash,
    spa_fingerprint,
    route_hash,
    bounded: true,
  };
}
