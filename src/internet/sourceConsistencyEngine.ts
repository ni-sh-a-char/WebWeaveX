/**
 * Converted from Python: core/internet/source_consistency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { measureSemanticConsensus } from "./semanticConsensusEngine.js";

export function analyzeSourceConsistency(sources: any): any {
  var claims: any = py.iter(py.or2(sources, () => ([]))).map((s: any) => ({"text": py.get(s, "url", py.get(s, "id", ""))}));
  var consensus: any = measureSemanticConsensus(claims);
  var consistent: any = py.or2((py.get(consensus, "consensus", 0) >= py.F(0.5)), () => ((py.len(py.or2(sources, () => ([]))) <= 1)));
  return {...(consensus), "consistent": consistent, "source_count": py.len(py.or2(sources, () => ([])))};
}
export { measureSemanticConsensus };
