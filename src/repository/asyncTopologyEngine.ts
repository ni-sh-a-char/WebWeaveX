/**
 * Converted from Python: core/repository/async_topology_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let ASYNC_KEYWORDS: any = py.toSet(new Set(["asyncio", "aiohttp", "celery", "rq", "dramatiq"]));
export function inferAsyncTopology(dependencies: any, parser_evidence: any): any {
  var async_deps: any = py.sorted(py.iter(dependencies).filter((dep: any) => py.contains(ASYNC_KEYWORDS, String(dep).toLowerCase())).map((dep: any) => dep));
  return {"async_components": async_deps, "evidence": py.sorted(py.toSet(parser_evidence)), "grounded": py.truthy(parser_evidence), "deterministic": true};
}
