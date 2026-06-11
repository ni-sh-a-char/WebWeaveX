// Phase 10/11: JS extraction over the same corpus + torture set.
// Run from the javascript worktree: npx tsx extract_js.mjs <verifier_dir> <out.json>
import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { extractSemanticHtml } from "./src/browser/htmlSemanticExtractionEngine.ts";
import { extractSemanticContent } from "./src/extraction/semanticContentExtractionEngine.ts";
import { computeKaalkaHash as H } from "./src/crypto/kaalkaRuntime.ts";

const TORTURE = {
  unclosed: "<html><body><h1>Open heading<p>para<a href='/x'>link<div>tail",
  nested_misnest: "<b><i>bold-italic</b></i><h2>after</h2>",
  entities: "<title>A &amp; B &lt;C&gt; &#8212; &quot;D&quot; &copy;</title><h1>&nbsp;E&nbsp;</h1>",
  comments_scripts: "<!-- c --><script>var x='<h1>not</h1>';</script><h1>real</h1><style>h2{}</style><a href='u'>l</a>",
  attr_quirks: "<a href=unquoted>u</a><a href='single'>s</a><a HREF=\"UPPER\">c</a><a>none</a>",
  deep_nesting: "<div>".repeat(50) + "<h3>deep</h3>" + "</div>".repeat(50),
  tables_lists: "<table><tr><td>c1</td><td>c2</td></tr></table><ul><li>i1</li><li>i2</li></ul><ol><li>o1</li></ol>",
  code_blocks: "<pre><code>if (a &lt; b) { run(); }</code></pre><p>after</p>",
  metadata: "<head><title>T</title><meta name='description' content='D'><meta property='og:title' content='OG'>" +
    "<script type='application/ld+json'>{\"@type\":\"Article\"}</script></head><body><h1>B</h1></body>",
  empty: "",
  text_only: "no tags at all, just text",
  broken_brackets: "<h1>a < b</h1><a href='x'>y</a>< not-a-tag <h2>z</h2>",
  duplicate_links: "<a href='/a'>1</a><a href='/a'>2</a><a href='/b'>3</a><a href='/a'>4</a>",
  unicode_content: "<title>café 中文 \u{1F680}</title><h1>शीर्ष</h1><a href='/ü'>link</a>",
};

const [vdir, outPath] = process.argv.slice(2);
const out = { torture: {}, corpus: {} };
for (const [tid, html] of Object.entries(TORTURE)) {
  const h = extractSemanticHtml(html);
  const c = extractSemanticContent(html);
  out.torture[tid] = { html_hash: H(h), content_hash: H(c), html_out: h, content_out: c };
}
const man = JSON.parse(readFileSync(join(vdir, "corpus", "manifest.json"), "utf-8"));
for (const e of man) {
  const raw = readFileSync(join(vdir, "corpus", e.file));
  // identical byte->text decoding as Python: utf-8 with U+FFFD replacement
  const text = new TextDecoder("utf-8", { fatal: false }).decode(raw);
  const h = extractSemanticHtml(text);
  const c = extractSemanticContent(text);
  out.corpus[e.file] = { html_hash: H(h), content_hash: H(c) };
}
writeFileSync(outPath, JSON.stringify(out, null, 1));
console.log(`js extraction: ${Object.keys(out.torture).length} torture + ${Object.keys(out.corpus).length} corpus pages`);
