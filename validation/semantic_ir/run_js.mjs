// Execute JS semantic-IR engine functions; emit output + hash.
//   cp run_js.mjs <js-ref>/ && (cd <js-ref> && npx tsx run_js.mjs <abs fixtures.json>)
import { readFileSync } from "node:fs";
import { computeKaalkaHash } from "./src/index.ts";
import { extractRhetoricalStructure } from "./src/documents/rhetoricalStructureEngine.ts";
import { assignSemanticRoles } from "./src/documents/semanticRoleEngine.ts";
import { extractHeadings } from "./src/documents/headingEngine.ts";
import { reconstructArgumentDependencies } from "./src/documents/argumentDependencyEngine.ts";
import { resolveCoreferences } from "./src/documents/coreferenceResolutionEngine.ts";

function call(fn, args) {
  switch (fn) {
    case "extract_rhetorical_structure":
      return extractRhetoricalStructure(args[0]);
    case "assign_semantic_roles":
      return assignSemanticRoles(args[0]);
    case "extract_headings":
      return extractHeadings(args[0]);
    case "reconstruct_argument_dependencies":
      return reconstructArgumentDependencies(args[0]);
    case "resolve_coreferences":
      return resolveCoreferences(args[0]);
    default:
      throw new Error("unknown fn " + fn);
  }
}

const fixtures = JSON.parse(readFileSync(process.argv[2], "utf-8"));
const out = [];
for (const fx of fixtures) {
  try {
    const result = call(fx.fn, fx.args);
    out.push({ id: fx.id, fn: fx.fn, output: result, hash: computeKaalkaHash(result) });
  } catch (e) {
    out.push({ id: fx.id, fn: fx.fn, error: String(e && e.message ? e.message : e) });
  }
}
process.stdout.write(JSON.stringify(out));
