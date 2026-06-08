/**
 * Converted from Python: core/evolution_runtime/runtime_pattern_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimePatterns(ui: any = null, workflows: any = null, semantic: any = null, sync_history: any = null): any {
  ui = py.or2(ui, () => ({}));
  workflows = py.or2(workflows, () => ([]));
  sync_history = py.or2(sync_history, () => ([]));
  return {"ui_structures": (((ui !== null && typeof ui === "object" && !Array.isArray(ui) && !(ui instanceof Set) && !(ui instanceof Map))) ? py.sorted(py.keys(ui)) : []), "workflow_patterns": py.iter(py.slice(workflows, null, 1000)).map((w: any) => py.toStr(py.get(w, "objective", py.get(w, "action", "")))), "semantic_layouts": py.slice([...py.iter(py.keys(py.or2(semantic, () => ({}))))], null, 100), "sync_histories": py.len(sync_history), "bounded": true};
}
