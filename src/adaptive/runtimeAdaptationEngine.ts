/**
 * Converted from Python: core/adaptive/runtime_adaptation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { buildExtractionFallbackChain } from "./extractionFallbackEngine.js";
import { recoverInteractionFlow } from "./interactionRecoveryEngine.js";
import { recoverModalRuntime } from "./modalRecoveryEngine.js";
import { recoverPaginationFlow } from "./paginationRecoveryEngine.js";

export function runRuntimeAdaptation(url: any, dom_nodes: any, html: any, interactions: any, primary_selector: any, page: any = null): any {
  var fallback: any = buildExtractionFallbackChain(primary_selector, dom_nodes, html);
  var interaction_recovery: any = recoverInteractionFlow(interactions, dom_nodes, html);
  var modal_recovery: any = recoverModalRuntime(page, html);
  var pagination_recovery: any = recoverPaginationFlow(primary_selector, html);
  return {"url": url, "fallback": fallback, "interaction_recovery": interaction_recovery, "modal_recovery": modal_recovery, "pagination_recovery": pagination_recovery, "bounded": true};
}
export { buildExtractionFallbackChain, recoverInteractionFlow, recoverModalRuntime, recoverPaginationFlow };
