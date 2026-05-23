import { orchestrate } from "../../src/orchestration/orchestrationEngine.js";
import { runDistributedExtraction } from "../../src/distributed/distributedExtractionOrchestrator.js";

const orch = orchestrate("https://example.com");
const dist = runDistributedExtraction([{ task_id: "t1", url: "https://example.com" }]);

const results = {
  orchestrate: orch.bounded === true,
  distributed: dist.bounded === true,
  workers: (dist.workers as unknown[])?.length > 0,
};

console.log("PASS", results);
if (!Object.values(results).every(Boolean)) process.exit(1);
