/**
 * Converted from Python: core/adaptive/adaptive_recovery_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { recoverInfiniteScroll } from "./infiniteScrollRecoveryEngine.js";
import { recoverModalRuntime } from "./modalRecoveryEngine.js";
import { recoverPaginationFlow } from "./paginationRecoveryEngine.js";

export function recoverAdaptiveRuntime(page: any, html: any, pagination_selector: any): any {
  return {"modal": recoverModalRuntime(page, html), "pagination": recoverPaginationFlow(pagination_selector, html), "scroll": recoverInfiniteScroll(page), "bounded": true};
}
export { recoverInfiniteScroll, recoverModalRuntime, recoverPaginationFlow };
