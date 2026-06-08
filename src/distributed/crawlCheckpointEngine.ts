/**
 * Converted from Python: core/distributed/crawl_checkpoint_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import { dumpsDeterministic } from "../serialize/deterministicSerializer.js";

export function checkpoint(state: any): any {
  return dumpsDeterministic(state);
}
export { dumpsDeterministic };
