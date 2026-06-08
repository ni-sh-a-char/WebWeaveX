/**
 * Converted from Python: core/engineering/semantic_repository_heatmap_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_HEATMAP: any = 10000;
export function buildRepositoryHeatmap(repository_ir: any): any {
  var files: any = py.slice([...py.iter(py.get(repository_ir, "files", []))], null, MAX_HEATMAP);
  var heatmap: any = py.iter(py.sorted(py.iter(files).filter((f: any) => py.truthy(f)).map((f: any) => py.toStr(f)))).map((path: any) => ({"path": path, "intensity": 1}));
  return {"heatmap": heatmap, "count": py.len(heatmap), "bounded": true};
}
