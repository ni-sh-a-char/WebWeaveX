/**
 * Converted from Python: core/agents/repository_query_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function queryRepository(result: any, key: any = ""): any {
  var repo: any = py.get(py.get(result, "content", {}), "repository", {});
  return (!py.truthy(key) ? repo : py.get(repo, key));
}
