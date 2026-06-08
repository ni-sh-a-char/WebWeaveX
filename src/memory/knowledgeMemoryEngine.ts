/**
 * Converted from Python: core/memory/knowledge_memory_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildKnowledgeMemory(entities: any = null, relations: any = null, topology: any = null): any {
  entities = [...py.iter(py.or2(entities, () => ([])))];
  relations = [...py.iter(py.or2(relations, () => ([])))];
  topology = py.or2(topology, () => ({}));
  return {"entities": py.sorted(entities, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any}), "semantic_relations": py.sorted(relations, {key: ((item: any) => [py.toStr(py.get(item, "from", "")), py.toStr(py.get(item, "to", "")), py.toStr(py.get(item, "relation", ""))]) as (item: any) => any}), "runtime_graphs": [...py.iter(py.get(topology, "graphs", []))], "distributed_topology": py.pyDict(py.get(topology, "distributed", {})), "application_cognition": py.pyDict(py.get(topology, "application", {})), "operational_structures": [...py.iter(py.get(topology, "operations", []))], "bounded": true};
}
