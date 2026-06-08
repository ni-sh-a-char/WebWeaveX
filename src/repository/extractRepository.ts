import { computeDeterministicHash } from "../crypto/kaalkaRuntime.js";
import { buildRuntimeGraph } from "../graph/runtimeGraph.js";
import { ingestRepository } from "./repositoryIngestion.js";

export function extractRepository(path: string): Record<string, unknown> {
  const ingested = ingestRepository(path);
  const graph = buildRuntimeGraph({ repository: ingested });
  return {
    repository_ir: {
      available: ingested.available === true,
      ir: "repository_runtime",
      graph,
      hash: computeDeterministicHash({ path, nodes: graph.nodes.length }),
      bounded: true,
    },
    bounded: true,
  };
}
