/**
 * Converted from Python: core/world_model/repository_world_model_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { normalizeImports, normalizeSymbols } from "./_normalize.js";

export let MAX_WORLD_FILES: any = 10000;
export function buildRepositoryWorldModel(repository_irs: any): any {
  var bounded: any = py.slice(repository_irs, null, MAX_WORLD_FILES);
  var files: any[] = [];
  var symbols: any[] = [];
  var imports: any[] = [];
  var ir: any;
  for (ir of py.iter(bounded)) {
    var path: any = py.get(ir, "path");
    py.listAppend(files, path);
    var semantic_ast: any = py.get(ir, "semantic_ast", {});
    py.extend(symbols, normalizeSymbols(semantic_ast));
    py.extend(imports, normalizeImports(semantic_ast));
  }
  return {"file_count": py.len(files), "files": py.sorted(py.iter(files).filter((f: any) => py.truthy(f)).map((f: any) => py.toStr(f))), "symbol_count": py.len(symbols), "import_count": py.len(imports), "symbols": py.slice(symbols, null, 10000), "imports": py.slice(imports, null, 10000), "bounded": true};
}
export { normalizeImports, normalizeSymbols };
