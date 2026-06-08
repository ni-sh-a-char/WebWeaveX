/**
 * Converted from Python: core/distributed_extraction/distributed_runtime_router.py
 * @generated — WebWeaveX python→javascript library port
 */

import { balanceExtractionWorkloads } from "./distributedLoadBalancer.js";

export function routeExtractionTasks(workers: any, tasks: any): any {
  return balanceExtractionWorkloads(workers, tasks);
}
export { balanceExtractionWorkloads };
