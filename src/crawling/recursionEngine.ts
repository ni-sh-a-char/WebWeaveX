/**
 * Converted from Python: core/crawling/recursion_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { CrawlBudget } from "./crawlBudgetEngine.js";

export function shouldRecurse(depth: any, budget: any): any {
  return budget.allow(depth);
}
export { CrawlBudget };
