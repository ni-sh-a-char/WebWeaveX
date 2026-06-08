/**
 * Converted from Python: core/graph/topology_reasoning_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { proveTopology } from "./topologyProofEngine.js";
import { modelGraphEntropy } from "./graphEntropyEngine.js";

export function reasonTopology(graph: any): any {
  var proof: any = proveTopology(graph);
  var entropy: any = modelGraphEntropy(graph);
  return {...(proof), "entropy": py.get(entropy, "entropy", 0), "evidence": ["graph:topology_proof"], "justification": {"hubs": py.get(proof, "hubs", []), "max_degree": py.get(proof, "max_degree", 0)}, "uncertainty": {"visible": (py.get(entropy, "entropy", 0) > 0)}, "deterministic_inputs": py.get(proof, "deterministic_inputs", [])};
}
export { modelGraphEntropy, proveTopology };
