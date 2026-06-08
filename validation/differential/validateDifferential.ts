/**
 * Differential equivalence orchestrator — specification vectors, JS-only execution.
 */
import { execSync } from "node:child_process";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "../..");
execSync("npx tsx validation/differential/runAllDifferential.ts", {
  stdio: "inherit",
  cwd: root,
});
