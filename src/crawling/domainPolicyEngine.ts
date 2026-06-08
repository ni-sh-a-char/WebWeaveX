/**
 * Converted from Python: core/crawling/domain_policy_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { isSafeUrl } from "../security/urlValidator.js";

export function sameDomain(seed: any, target: any): any {
  try {
    return py.eq(py.urlparse(seed).hostname, py.urlparse(target).hostname);
  } catch (_e: any) {
    return false;
  }
}
export function allowUrl(seed: any, url: any, same_domain_only: any = false): any {
  if (!py.truthy(isSafeUrl(url))) {
    return false;
  }
  if ((py.truthy(same_domain_only) && !py.truthy(sameDomain(seed, url)))) {
    return false;
  }
  return true;
}
export { isSafeUrl };
