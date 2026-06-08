/**
 * Converted from Python: core/knowledge/reconstruction/architecture_knowledge_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function buildArchitectureKnowledge(arch: any): any {
  var styles: any = py.sorted(py.toSet(py.get(arch, "styles", [])));
  var rels: any = py.iter(py.get(arch, "relationships", [])).filter((e: any) => (((e !== null && typeof e === "object" && !Array.isArray(e) && !(e instanceof Set) && !(e instanceof Map))) && py.truthy(py.get(e, "from")) && py.truthy(py.get(e, "to")))).map((e: any) => ({"from": py.get(e, "from", ""), "to": py.get(e, "to", "")}));
  return {"nodes": py.add(styles, py.sorted(py.toSet(py.iter(rels).flatMap((e: any) => py.iter([py.at(e, "from"), py.at(e, "to")]).map((x: any) => x))))), "edges": py.sorted(rels, {key: ((e: any) => [py.at(e, "from"), py.at(e, "to")]) as (item: any) => any})};
}
