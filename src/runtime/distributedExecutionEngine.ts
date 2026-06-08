/**
 * Converted from Python: core/runtime/distributed_execution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export let MAX_SHARDS: any = 64;
export function reconstructDistributedExecution(shards: any, parser_evidence: any): any {
  var ordered: any = py.slice(py.sorted(shards, {key: ((s: any) => py.toStr(py.get(s, "id", ""))) as (item: any) => any}), null, MAX_SHARDS);
  return {"shards": ordered, "shard_count": py.len(ordered), "evidence": py.sorted(py.toSet(parser_evidence)), "grounded": py.truthy(parser_evidence), "deterministic": true, "bounded": (py.len(ordered) <= MAX_SHARDS)};
}
