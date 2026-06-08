/**
 * Converted from Python: core/evolution_runtime/runtime_evolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimeEvolution(mutations: any, lineage: any): any {
  var payload: any = py.join("|", py.sorted(py.iter(mutations).map((m: any) => `${py.toStr(py.get(m, "kind", ""))}:${py.toStr(py.get(m, "target", ""))}`)));
  var evolution_id: any = py.slice(py.hashNew("sha256", py.encode(payload, "utf-8")).hexdigest(), null, 32);
  return {"evolution_id": evolution_id, "mutations": py.sorted(mutations, {key: ((item: any) => py.toStr(py.get(item, "target", ""))) as (item: any) => any}), "lineage": py.sorted(lineage, {key: ((item: any) => py.toStr(py.get(item, "id", ""))) as (item: any) => any}), "improvements": {"selector_repairs": py.sum(py.iter(mutations).filter((m: any) => py.eq(py.get(m, "kind"), "selector")).map((m: any) => 1)), "workflow_optimizations": py.sum(py.iter(mutations).filter((m: any) => py.eq(py.get(m, "kind"), "workflow")).map((m: any) => 1)), "semantic_convergence": py.sum(py.iter(mutations).filter((m: any) => py.eq(py.get(m, "kind"), "semantic")).map((m: any) => 1)), "sync_improvements": py.sum(py.iter(mutations).filter((m: any) => py.eq(py.get(m, "kind"), "sync")).map((m: any) => 1))}, "bounded": true};
}
