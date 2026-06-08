/**
 * Converted from Python: core/memory/stable_memory_hash.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { computeKaalkaHash } from "../crypto/kaalkaHashEngine.js";

export function stableMemoryHash(memory: any): any {
  var history: any = py.get(memory, "runtime_history", []);
  var lineage: any = py.get(memory, "lineage", []);
  var relations: any = py.get(memory, "semantic_relations", []);
  var canonical: any = {"memory_id": py.get(memory, "memory_id", ""), "runtime_history": py.sorted(history, {key: ((h: any) => [py.toInt(py.get(h, "tick", 0)), py.toStr(py.get(h, "kind", "")), py.toStr(py.get(h, "source", ""))]) as (item: any) => any}), "lineage": py.sorted(lineage, {key: ((x: any) => py.toStr(py.get(x, "id", ""))) as (item: any) => any}), "semantic_relations": py.sorted(relations, {key: ((r: any) => [py.toStr(py.get(r, "from", "")), py.toStr(py.get(r, "to", ""))]) as (item: any) => any})};
  return computeKaalkaHash(py.jsonDumps(canonical, {sortKeys: true, separators: [",", ":"] as [string, string]}));
}
export { computeKaalkaHash };
