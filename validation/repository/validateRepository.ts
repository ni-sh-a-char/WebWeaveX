import { extractRepository } from "../../src/repository/extractRepository.js";
import { ingestRepository } from "../../src/repository/repositoryIngestion.js";

const ingested = ingestRepository(".");
const extracted = extractRepository(".");

const results = {
  ingest_available: ingested.available === true,
  ingest_bounded: ingested.bounded === true,
  extract_ir: (extracted.repository_ir as Record<string, unknown>)?.ir === "repository_runtime",
  graph_nodes: Array.isArray(
    ((extracted.repository_ir as Record<string, unknown>)?.graph as Record<string, unknown>)?.nodes,
  ),
};

console.log("PASS", results);
if (!Object.values(results).every(Boolean)) process.exit(1);
