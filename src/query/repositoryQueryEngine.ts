/**
 * Converted from Python: core/query/repository_query_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { compileRepositoryIr } from "../ir/repositoryIr.js";

export function queryRepository(source: any = "", path: any = "", files: any = null): any {
  var ir: any = compileRepositoryIr(source, path, files);
  return {"ir": ir, "evidence": py.get(ir, "semantic_evidence", {}), "explainable": true, "bounded": true};
}
export { compileRepositoryIr };
