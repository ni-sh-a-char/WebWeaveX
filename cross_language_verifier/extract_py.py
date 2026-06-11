"""Phase 10/11: run extract_semantic_html + extract_semantic_content over the
corpus + offline torture set on Python; emit output hashes."""
import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Projects\wwx_cert_py")
from core.browser.html_semantic_extraction_engine import extract_semantic_html
from core.extraction.semantic_content_extraction_engine import extract_semantic_content
from core.crypto.kaalka_hash_engine import compute_kaalka_hash as H

TORTURE = {
    "unclosed": "<html><body><h1>Open heading<p>para<a href='/x'>link<div>tail",
    "nested_misnest": "<b><i>bold-italic</b></i><h2>after</h2>",
    "entities": "<title>A &amp; B &lt;C&gt; &#8212; &quot;D&quot; &copy;</title><h1>&nbsp;E&nbsp;</h1>",
    "comments_scripts": "<!-- c --><script>var x='<h1>not</h1>';</script><h1>real</h1><style>h2{}</style><a href='u'>l</a>",
    "attr_quirks": "<a href=unquoted>u</a><a href='single'>s</a><a HREF=\"UPPER\">c</a><a>none</a>",
    "deep_nesting": "<div>" * 50 + "<h3>deep</h3>" + "</div>" * 50,
    "tables_lists": "<table><tr><td>c1</td><td>c2</td></tr></table><ul><li>i1</li><li>i2</li></ul><ol><li>o1</li></ol>",
    "code_blocks": "<pre><code>if (a &lt; b) { run(); }</code></pre><p>after</p>",
    "metadata": "<head><title>T</title><meta name='description' content='D'><meta property='og:title' content='OG'>"
                "<script type='application/ld+json'>{\"@type\":\"Article\"}</script></head><body><h1>B</h1></body>",
    "empty": "",
    "text_only": "no tags at all, just text",
    "broken_brackets": "<h1>a < b</h1><a href='x'>y</a>< not-a-tag <h2>z</h2>",
    "duplicate_links": "<a href='/a'>1</a><a href='/a'>2</a><a href='/b'>3</a><a href='/a'>4</a>",
    "unicode_content": "<title>café 中文 🚀</title><h1>शीर्ष</h1><a href='/ü'>link</a>",
}


def main():
    out = {"torture": {}, "corpus": {}}
    for tid, html in TORTURE.items():
        h = extract_semantic_html(html)
        c = extract_semantic_content(html)
        out["torture"][tid] = {"html_hash": H(h), "content_hash": H(c),
                               "html_out": h, "content_out": c}
    corpus = Path("corpus")
    man = json.load(open(corpus / "manifest.json", encoding="utf-8"))
    for e in man:
        raw = (corpus / e["file"]).read_bytes()
        text = raw.decode("utf-8", errors="replace")
        h = extract_semantic_html(text)
        c = extract_semantic_content(text)
        out["corpus"][e["file"]] = {"html_hash": H(h), "content_hash": H(c)}
    with open(sys.argv[1], "wb") as f:
        f.write(json.dumps(out, ensure_ascii=False, sort_keys=True, indent=1).encode("utf-8"))
    print(f"python extraction: {len(out['torture'])} torture + {len(out['corpus'])} corpus pages")


if __name__ == "__main__":
    main()
