/**
 * Converted from Python: core/evolution_runtime/semantic_evolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function evolveSemanticRuntime(semantic: any = null, history: any = null): any {
  semantic = py.or2(semantic, () => ({}));
  history = py.or2(history, () => ([]));
  var inner: any = py.get(semantic, "semantic", semantic);
  var entities: any = py.get(py.get(inner, "entities", {}), "entities", []);
  var recurring: Record<string, any> = {};
  var entity: any;
  for (entity of py.iter(entities)) {
    var label: any = py.toStr(py.get(entity, "label", py.get(entity, "type", "")));
    py.setItem(recurring, label, py.add(py.get(recurring, label, 0), 1));
  }
  var stable: any = py.sorted(py.items(recurring).filter(([label, count]: any) => (count >= 1)).map(([label, count]: any) => label), {key: (py.toStr) as (item: any) => any});
  return {"recurring_entities": stable, "stable_ontology": py.get(inner, "ontology", {}), "domain": py.get(py.get(inner, "domain", {}), "domain", ""), "semantic_convergence": py.len(stable), "domain_stabilized": py.truthy(py.get(inner, "domain")), "history_length": py.len(history), "bounded": true};
}
