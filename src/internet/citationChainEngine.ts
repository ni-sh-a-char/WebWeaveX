/**
 * Converted from Python: core/internet/citation_chain_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function extractCitationChain(text: any): any {
  var urls: any = py.sorted(py.toSet(py.reFindall("https?://[^\\s\\)\\]>\\\"']+", py.or2(text, () => ("")), "")));
  var refs: any = py.sorted(py.toSet(py.reFindall("\\[[^\\]]+\\]\\((https?://[^\\)]+)\\)", py.or2(text, () => ("")), "")));
  var chain: any = py.sorted(py.toSet(py.add(urls, refs)));
  var edges: any = py.range(py.sub(py.len(chain), 1)).map((i: any) => ({"from": py.at(chain, i), "to": py.at(chain, py.add(i, 1))}));
  return {"citations": chain, "edges": edges, "citation_count": py.len(chain)};
}
