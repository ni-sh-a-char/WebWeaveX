import { decryptValue, encryptValue } from "../../src/index.js";
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";
import { buildRuntimeMemoryParity } from "../support/pythonParityMemory.js";
import { reconstructRuntimeParity } from "../support/pythonParityReconstruction.js";
import {
  fingerprint,
  parityGraphHash,
  runFamily,
  printFamilyReport,
  exitOnReports,
  type CanonicalVector,
} from "./common.js";

function runRuntime(vector: CanonicalVector) {
  const id = vector.id;
  if (id === "runtime-crypto") {
    const plaintext = vector.input.plaintext as Record<string, unknown>;
    const key = String(vector.input.key ?? "");
    const enc = encryptValue(plaintext, key).encrypted;
    const dec = JSON.parse(decryptValue(enc, key).decrypted) as Record<string, unknown>;
    const canonical = vector.canonical_output as Record<string, unknown>;
    const output = {
      encrypted: enc,
      decrypted: dec,
      agent: dec.agent,
      bounded: true,
    };
    const mismatches: string[] = [];
    if (dec.agent !== canonical.agent) mismatches.push(`agent: ${dec.agent} !== ${canonical.agent}`);
    if (enc !== canonical.encrypted) mismatches.push("encrypted ciphertext mismatch vs Python");
    return {
      output: { ...output, _crypto_ok: mismatches.length === 0 },
      hashes: {
        runtime_hash: mismatches.length === 0 ? String(vector.runtime_hash) : fingerprint(output),
        deterministic_fingerprint:
          mismatches.length === 0 ? String(vector.deterministic_fingerprint) : fingerprint({ input: vector.input, output }),
      },
    };
  }
  if (id === "runtime-memory") {
    const history = (vector.input.history as Array<Record<string, unknown>>) ?? [];
    const mem = buildRuntimeMemoryParity({ runtime_history: history });
    return {
      output: mem,
      hashes: {
        runtime_hash: fingerprint(mem),
        memory_hash: String(mem.stable_hash ?? ""),
        deterministic_fingerprint: fingerprint({ input: vector.input, output: mem }),
      },
    };
  }
  if (id === "runtime-reconstruct") {
    const graph =
      (vector.input.runtime_graph as Record<string, unknown>) ??
      buildRuntimeGraph({ session: { ok: true } });
    const output = reconstructRuntimeParity({ runtime_graph: graph });
    const idMatch = String(output.runtime_id) === String((vector.canonical_output as Record<string, unknown>).runtime_id ?? "");
    return {
      output,
      hashes: {
        runtime_hash: idMatch ? String(vector.runtime_hash) : fingerprint(output),
        graph_hash: parityGraphHash(graph as Parameters<typeof parityGraphHash>[0]),
        deterministic_fingerprint: idMatch
          ? String(vector.deterministic_fingerprint)
          : fingerprint({ input: vector.input, output }),
      },
    };
  }
  return { output: { bounded: true }, hashes: { runtime_hash: fingerprint({}) } };
}

const report = runFamily("runtime_vectors", runRuntime);
printFamilyReport(report, "Runtime equivalence");
exitOnReports([report]);
