/** Mirror of Python: validation/final_production_master.py */
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";

const results = {
  bounded: buildRuntimeGraph({ probe: true }).bounded === true,
  subsystem: "production_master",
};

console.log("PASS", results);
if (!Object.values(results).every(Boolean)) process.exit(1);
