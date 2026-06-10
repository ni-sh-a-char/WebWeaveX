// Execute the JavaScript reference for each fixture; emit output + hash.
// Run from inside the materialized JS branch (imports ./src/index.ts via tsx):
//   cp run_js.mjs <js-ref>/  &&  cd <js-ref>  &&  npx tsx run_js.mjs <fixtures.json>
import { readFileSync } from "node:fs";
import {
  extractKubernetesRuntime,
  extractDatabaseRuntime,
  buildRuntimeMemory,
  queryRuntimeMemory,
  buildBrowserIdentity,
  computeKaalkaHash,
} from "./src/index.ts";

function call(api, args) {
  switch (api) {
    case "extract_kubernetes_runtime":
      return extractKubernetesRuntime(args[0] ?? undefined);
    case "extract_database_runtime":
      return extractDatabaseRuntime(args[0], args[1] ?? undefined);
    case "build_runtime_memory":
      return buildRuntimeMemory(args[0], args[1], args[2]);
    case "query_runtime_memory":
      return queryRuntimeMemory(args[0], args[1], args[2]);
    case "build_browser_identity":
      return buildBrowserIdentity(args[0]);
    case "compute_kaalka_hash":
      return computeKaalkaHash(args[0]);
    default:
      throw new Error("unknown api " + api);
  }
}

const fixtures = JSON.parse(readFileSync(process.argv[2], "utf-8"));
const out = [];
for (const fx of fixtures) {
  try {
    const result = call(fx.api, fx.args);
    out.push({
      id: fx.id,
      api: fx.api,
      output: result,
      hash: fx.api === "compute_kaalka_hash" ? result : computeKaalkaHash(result),
    });
  } catch (e) {
    out.push({ id: fx.id, api: fx.api, error: String(e && e.message ? e.message : e) });
  }
}
process.stdout.write(JSON.stringify(out));
