import { readFileSync, writeFileSync } from "node:fs";
import { extractSemanticHtml } from "./src/browser/htmlSemanticExtractionEngine.ts";
import { extractSemanticContent } from "./src/extraction/semanticContentExtractionEngine.ts";
import { computeKaalkaHash as H } from "./src/crypto/kaalkaRuntime.ts";

const vectors = JSON.parse(readFileSync(process.argv[2], "utf-8"));
const out = {};
for (const [vid, html] of Object.entries(vectors)) {
  out[vid] = { h: H(extractSemanticHtml(html)), c: H(extractSemanticContent(html)) };
}
writeFileSync(process.argv[3], JSON.stringify(out));
console.log(`js synth: ${Object.keys(out).length}`);
