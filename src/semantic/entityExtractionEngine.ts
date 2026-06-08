/**
 * Converted from Python: core/semantic/entity_extraction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let ENTITY_PATTERNS: any = {"organization": py.regex("\\b(inc|corp|llc|ltd|company)\\b", "i"), "api": py.regex("\\b(api|endpoint|rest|graphql)\\b", "i"), "metric": py.regex("\\b(kpi|metric|latency|throughput|error rate)\\b", "i"), "user": py.regex("\\b(user|account|profile|login)\\b", "i"), "service": py.regex("\\b(service|microservice|worker|queue)\\b", "i"), "workflow": py.regex("\\b(workflow|pipeline|job|task)\\b", "i"), "infrastructure": py.regex("\\b(kubernetes|docker|vm|cluster|deploy)\\b", "i")};
export function extractSemanticEntities(text: any = "", structure: any = null): any {
  structure = py.or2(structure, () => ({}));
  var entities: any[] = [];
  var relations: any[] = [];
  var entity_index: any = 0;
  var label: any;
  var pattern: any;
  for ([label, pattern] of py.items(ENTITY_PATTERNS)) {
    if (py.truthy(pattern.search(text))) {
      var entity_id: any = `entity:${py.toStr(label)}:${py.toStr(entity_index)}`;
      py.listAppend(entities, {"id": entity_id, "type": label, "label": label, "source": "pattern"});
      entity_index = py.add(entity_index, 1);
    }
  }
  var action: any;
  for (action of py.iter(py.slice(py.get(structure, "actions", []), null, 5000))) {
    py.listAppend(entities, {"id": `entity:ui_action:${py.toStr(entity_index)}`, "type": "ui_action", "label": py.toStr(py.get(action, "label", py.get(action, "type", ""))), "source": "structure"});
    entity_index = py.add(entity_index, 1);
  }
  var artifact: any;
  for (artifact of py.iter(py.slice(py.get(structure, "artifacts", []), null, 5000))) {
    py.listAppend(entities, {"id": `entity:runtime:${py.toStr(entity_index)}`, "type": "runtime_artifact", "label": py.toStr(artifact), "source": "runtime"});
    entity_index = py.add(entity_index, 1);
  }
  entities = py.sorted(entities, {key: ((item: any) => py.at(item, "id")) as (item: any) => any});
  var index: any;
  for (index = 1; index < py.len(entities); index++) {
    py.listAppend(relations, {"from": py.at(py.at(entities, py.sub(index, 1)), "id"), "to": py.at(py.at(entities, index), "id"), "relation": "related_to"});
  }
  return {"entities": entities, "relations": relations, "ontology": {}, "bounded": true};
}
