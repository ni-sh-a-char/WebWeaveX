/**
 * Converted from Python: core/kernel/runtime_semantic_bridge.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { runSemanticForExtraction } from "../semantic/semanticOrchestrator.js";

export function runSemanticPhase(sources: any = null, tick: any = 0, kwargs: Record<string, any> = {}): any {
  var extraction: any = py.get(py.or2(sources, () => ({})), "extraction", {});
  return py.callKw(runSemanticForExtraction as (...a: any[]) => any, ["semantic_runtime", "memory_path", "memory_key", "url", "html", "interactions", "application_result", "causality_result", "native_cognition", "runtime_graph", "objective", "merge_graph"], {"semantic_runtime": true, "url": py.toStr(py.get(extraction, "url", "")), "html": py.slice(py.toStr(py.get(py.get(extraction, "runtime", {}), "html", "")), null, 50000), "merge_graph": false}, Object.fromEntries(py.items(kwargs).filter(([k, v]: any) => py.contains(["memory_path", "memory_key"], k)).map(([k, v]: any) => ([k, v] as [any, any]))));
}
export { runSemanticForExtraction };
