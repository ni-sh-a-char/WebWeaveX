/**
 * Converted from Python: core/semantic/semantic_alignment_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function alignSemanticRuntimes(browser: any = null, native: any = null, repository: any = null, document: any = null, multimodal: any = null, runtime: any = null): any {
  var layers: any = {"browser": py.or2(browser, () => ({})), "native": py.or2(native, () => ({})), "repository": py.or2(repository, () => ({})), "document": py.or2(document, () => ({})), "multimodal": py.or2(multimodal, () => ({})), "runtime": py.or2(runtime, () => ({}))};
  var aligned_domains: any[] = [];
  var name: any;
  var payload: any;
  for ([name, payload] of py.items(layers)) {
    if (py.truthy(payload)) {
      py.listAppend(aligned_domains, {"layer": name, "domain": py.get(payload, "domain", py.get(payload, "primary_kind", ""))});
    }
  }
  return {"layers": layers, "aligned_domains": aligned_domains, "aligned": true, "bounded": true};
}
