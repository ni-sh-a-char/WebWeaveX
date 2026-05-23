import { runDistributedExtraction } from "../../src/distributed/distributedExtractionOrchestrator.js";

const result = runDistributedExtraction(
  [{ task_id: "a", url: "https://a.example", priority: 1 }],
  undefined,
  {},
  0,
);

console.log("PASS", { bounded: result.bounded, workers: (result.workers as unknown[])?.length });
if (!result.bounded) process.exit(1);
