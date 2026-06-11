// Real-world scenario runner (JS) — mirror of real_world_py.py.
// Run from the javascript clone: npx tsx real_world_js.mjs <dart_clone> <js_clone>
import { readFileSync } from "node:fs";
import {
  compileDocument, queryDocuments, compileRepository, queryRepository,
  reasonSemantically, runApplicationCognition, querySemantics,
  computeKaalkaHash as H,
} from "./src/index.ts";

const dart = process.argv[2];
const js = process.argv[3];
const read = (p) => readFileSync(p, "utf-8");
// code-point cap (Python slice semantics; UTF-16 .slice would diverge)
const cap = (s, n) => [...s].slice(0, n).join("");

const readme = read(`${dart}/README.md`);
const tsSrc = read(`${js}/src/parsers/parserRegistry.ts`);
const page = read(`${dart}/cross_language_verifier/corpus/page_0000.html`);

const out = {
  doc_readme: H(compileDocument(cap(readme, 20000))),
  query_doc_readme: H(queryDocuments(null, cap(readme, 20000))),
  repo_ts_engine: H(compileRepository(tsSrc, "src/parsers/parserRegistry.ts")),
  query_repo_ts: H(queryRepository(null, tsSrc, "src/parsers/parserRegistry.ts")),
  reason_discourse: H(reasonSemantically("discourse", { text: cap(readme, 5000) })),
  reason_runtime: H(reasonSemantically("runtime", { source: tsSrc, path: "src/parsers/parserRegistry.ts" })),
  app_cognition_real_page: H(runApplicationCognition("https://release.test/app", page)),
  semantics_repo: H(querySemantics("repository", { source: tsSrc, path: "x.ts" })),
};
process.stdout.write(JSON.stringify(out));
