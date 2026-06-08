/**
 * Converted from Python: core/streaming/dom_mutation_stream_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { computeKaalkaHash } from "../crypto/kaalkaHashEngine.js";
import { makeStreamEvent } from "./streamCaptureEngine.js";

export let MAX_MUTATIONS: any = 10000;
export function captureDomMutations(page: any): any {
  var mutations: any[] = [];
  var events: any[] = [];
  if (((page !== null && page !== undefined) && (page !== null && page !== undefined && typeof page === "object" && (String("_test_dom_mutations") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_dom_mutations")] === "function")))) {
    mutations = py.slice([...py.iter(page._test_dom_mutations)], null, MAX_MUTATIONS);
  }
  var index: any;
  var mutation: any;
  for ([index, mutation] of py.enumerate(mutations)) {
    py.listAppend(events, makeStreamEvent(index, "dom_mutation", py.toStr(py.get(mutation, "type", "mutation")), py.toStr(py.get(mutation, "payload", "")), py.toStr(py.get(mutation, "node_id", ""))));
  }
  var dom_snapshot: any = "";
  if (((page !== null && page !== undefined) && (page !== null && page !== undefined && typeof page === "object" && (String("_test_html") in (page as object) || typeof (page as Record<string, unknown>)[String("_test_html")] === "function")))) {
    dom_snapshot = py.toStr(page._test_html);
  }
  return {"mutations": mutations, "events": events, "dom_hash": computeKaalkaHash(py.slice(dom_snapshot, null, 1000000)), "bounded": true};
}
export { computeKaalkaHash, makeStreamEvent };
