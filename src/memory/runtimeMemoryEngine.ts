/**
 * Converted from Python: core/memory/runtime_memory_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { stableMemoryHash } from "./stableMemoryHash.js";

export function buildRuntimeMemory(runtime_history: any = null, lineage: any = null, semantic_relations: any = null): any {
  runtime_history = [...py.iter(py.or2(runtime_history, () => ([])))];
  lineage = [...py.iter(py.or2(lineage, () => ([])))];
  semantic_relations = [...py.iter(py.or2(semantic_relations, () => ([])))];
  var payload: any = py.join("|", py.add(py.iter(runtime_history).map((item: any) => py.toStr(py.get(item, "tick", py.get(item, "step", "")))), py.iter(lineage).map((item: any) => py.toStr(py.get(item, "id", "")))));
  var memory_id: any = py.slice(py.hashNew("sha256", py.encode(payload, "utf-8")).hexdigest(), null, 32);
  var result: any = {"memory_id": memory_id, "runtime_history": py.sorted(runtime_history, {key: ((item: any) => py.toInt(py.get(item, "tick", py.get(item, "step", 0)))) as (item: any) => any}), "workflow_history": py.iter(runtime_history).filter((item: any) => py.eq(py.get(item, "kind"), "workflow")).map((item: any) => item), "synchronization_history": py.iter(runtime_history).filter((item: any) => py.eq(py.get(item, "kind"), "sync")).map((item: any) => item), "evolution_history": py.iter(runtime_history).filter((item: any) => py.eq(py.get(item, "kind"), "evolution")).map((item: any) => item), "lineage": py.sorted(lineage, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any}), "semantic_relations": py.sorted(semantic_relations, {key: ((item: any) => [py.toStr(py.get(item, "from", "")), py.toStr(py.get(item, "to", ""))]) as (item: any) => any}), "bounded": true};
  py.setItem(result, "stable_hash", stableMemoryHash(result));
  return result;
}
export { stableMemoryHash };
