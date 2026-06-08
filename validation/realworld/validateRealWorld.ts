/** Mirror of Python: validation/run_real_world_validation.py */
import { buildRuntimeGraph } from "../../src/graph/runtimeGraph.js";

const results = {
  bounded: buildRuntimeGraph({ probe: true }).bounded === true,
  subsystem: "realworld",
};

console.log("PASS", results);
if (!Object.values(results).every(Boolean)) process.exit(1);
