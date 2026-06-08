/**
 * Converted from Python: core/replay/replay_equivalence_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { RuntimeGraphContract } from "../contracts/graphContracts.js";
import { computeKaalkaHash } from "../crypto/kaalkaHashEngine.js";
import { computeGlobalRuntimeFingerprint } from "../determinism/globalRuntimeFingerprint.js";

export function _graphHash(graph: any): any {
  var normalized: any = RuntimeGraphContract.normalize(graph);
  return computeKaalkaHash(py.jsonDumps({"nodes": py.get(normalized, "nodes", []), "edges": py.get(normalized, "edges", [])}, {sortKeys: true, defaultStr: true}));
}
export function validateReplayEquivalence(original: any, replayed: any): any {
  var orig_graph: any = py.get(original, "unified_runtime_graph", py.get(original, "graph", {}));
  var replay_graph: any = py.get(replayed, "unified_runtime_graph", py.get(replayed, "graph", {}));
  var orig_fp: any = computeGlobalRuntimeFingerprint(original, orig_graph);
  var replay_fp: any = computeGlobalRuntimeFingerprint(replayed, replay_graph);
  var checks: any = [{"name": "graph_hash", "ok": py.eq(_graphHash(orig_graph), _graphHash(replay_graph)), "original": py.slice(_graphHash(orig_graph), null, 16), "replay": py.slice(_graphHash(replay_graph), null, 16)}, {"name": "global_fingerprint", "ok": py.eq(orig_fp, replay_fp), "original": py.slice(orig_fp, null, 16), "replay": py.slice(replay_fp, null, 16)}, {"name": "browser_identity", "ok": py.eq(py.get(py.get(original, "browser_ir", {}), "runtime_identity"), py.get(py.get(replayed, "browser_ir", {}), "runtime_identity"))}];
  return {"equivalent": py.all(py.iter(checks).map((c: any) => py.at(c, "ok"))), "checks": checks, "bounded": true};
}
export { RuntimeGraphContract, computeGlobalRuntimeFingerprint, computeKaalkaHash };
