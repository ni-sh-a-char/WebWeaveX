/**
 * Converted from Python: core/runtime/semantic_task_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export function buildSemanticTasks(specs: any): any {
  return py.iter(py.sorted(specs, {key: ((x: any) => py.toStr(py.get(x, "id", ""))) as (item: any) => any})).map((s: any) => ({"id": py.get(s, "id"), "kind": py.get(s, "kind", "semantic"), "priority": py.toInt(py.get(s, "priority", 0)), "evidence": py.sorted(py.toSet(py.or2(py.get(s, "evidence", []), () => ([]))))}));
}
