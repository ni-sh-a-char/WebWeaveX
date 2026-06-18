#!/usr/bin/env python3
"""Session-4B cross-language golden vectors from canonical Python 2.1.0.

Run from a materialized Python-branch checkout (so `core` is importable):

    python tools/gen_java_parity_vectors_s4b.py <out.json>

Covers the two extraction APIs that survive the Session-4B dependency proof
(JAVA_SESSION_4B_DEPENDENCY_PROOF.md) — pure, JDK-portable, no BeautifulSoup /
lxml / browser / OCR / PDF / DOCX / network / LLM:

  * extract_document_runtime  (core.documents.universal_document_extraction_engine)
  * extract_paginated_content (core.interaction.pagination_engine)

Each entry stores the inputs plus the canonical `stable_serialize` of the Python
output and its `compute_kaalka_hash`; the Java test reconstructs the inputs,
recomputes, and asserts byte-equality.
"""
from __future__ import annotations

import json
import sys

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize

from core.documents.universal_document_extraction_engine import extract_document_runtime
from core.interaction.pagination_engine import extract_paginated_content


def entry(name, inputs, value):
    return {
        "name": name,
        "inputs": inputs,
        "serialized": stable_serialize(value),
        "hash": compute_kaalka_hash(value),
    }


# --------------------------- document_runtime ---------------------------------

def doc(name, text, slides=None, workbook=None):
    return entry(
        name,
        {"text": text, "slides": slides, "workbook": workbook},
        extract_document_runtime(text, slides=slides, workbook=workbook),
    )


# --------------------------- paginated_content --------------------------------

class _Page:
    """Deterministic fixture page mirroring the duck-typed `_test_*` protocol."""

    def __init__(self, spec):
        self._test_url = spec["test_url"]
        pmap = spec.get("paginate")
        if pmap is not None:
            self._pmap = pmap
            self._test_paginate = self._paginate
        if spec.get("next_url") is not None:
            self._test_next_url = spec["next_url"]
        if spec.get("has_click"):
            self.click = self._click
        self._raises = bool(spec.get("click_raises"))

    def _click(self, selector):
        if self._raises:
            raise RuntimeError("click failed")

    def _paginate(self, current):
        return self._pmap.get(current, "")


def page(name, next_selector, spec):
    p = None if spec is None else _Page(spec)
    return entry(
        name,
        {"next_selector": next_selector, "page": spec},
        extract_paginated_content(p, next_selector),
    )


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 4B: pure document + pagination extraction)"}

    # ---- extract_document_runtime -------------------------------------------
    # nested headings + body
    nested = "# Title\nintro line\n## Section A\nbody a1\nbody a2\n### Sub\ndeep\n"
    refs = "# Doc\npreamble\n## References\n[1] First ref\n[2] Second ref\n"
    biblio = "# Doc\ntext\n## Bibliography\nSmith 2020\nJones 2021\n"
    table = "name | value\nalpha | 1\nbeta | 2\n"
    # Unicode: CJK, astral emoji (U+1F600), combining marks (e + U+0301)
    unicode_text = "# 标题 \U0001F600\ncafé line\n## 参考\n[٤] arabic-indic digit cite\n"
    # normalization: CRLF endings, trailing whitespace, NBSP, zero-width
    norm_text = "# Heading   \r\nbody with trailing space  \r\n## Next\t\r\nx​\r\n"
    # malformed: bare '#', empty brackets, non-digit cite, pipe-only lines, heading-after-heading
    malformed = "#\n## \n[] [abc] [42]\n|||\n# A\n# B\ncontent under B\n"
    blanks = "\n\n# Only Heading\n\n\n"

    out["extract_document_runtime"] = [
        doc("doc_empty", ""),                       # empty input
        doc("doc_whitespace", "   \n\t\n"),         # whitespace-only lines
        doc("doc_nested_headings", nested),         # heading hierarchy + sections
        doc("doc_citations", "see [1] and [2] also [12] and [007]\n"),
        doc("doc_references", refs),                # references section
        doc("doc_bibliography", biblio),            # bibliography section
        doc("doc_table", table),                    # markdown table
        doc("doc_unicode", unicode_text),           # Unicode (CJK/emoji/combining/arabic digit)
        doc("doc_normalization", norm_text),        # CRLF + trailing ws + NBSP + zero-width
        doc("doc_malformed", malformed),            # malformed input + empty-section drop
        doc("doc_leading_blanks", blanks),
        doc("doc_with_slides", "# Deck\nintro\n", slides=[
            {"title": "Slide 1", "content": "hello"},
            {"title": "Slide 2", "content": "world"},
            {"content": "no title"},                # missing title -> None
        ]),
        doc("doc_with_workbook", "# Book\n", workbook={
            "Sheet1": [["a", "b"], ["c", "d"]],
            "Sheet2": [["x"]],
        }),
        doc("doc_slides_and_workbook", "# Both\ntext\n",
            slides=[{"title": "S", "content": "c"}],
            workbook={"Only": [["1", "2", "3"]]}),
        doc("doc_table_ragged", "| a | b |\n|c|\nd | e | f | g\n"),  # ragged + empty cells
    ]

    # ---- extract_paginated_content ------------------------------------------
    linear = {"test_url": "p0", "paginate": {"p0": "p1", "p1": "p2", "p2": ""}}
    cycle = {"test_url": "p0", "paginate": {"p0": "p1", "p1": "p2", "p2": "p0"}}
    long_map = {f"p{i}": f"p{i + 1}" for i in range(150)}
    boundary = {"test_url": "p0", "paginate": long_map}     # hits MAX_PAGES=100
    click_ok = {"test_url": "p0", "paginate": {"p0": "p1", "p1": ""}, "has_click": True}
    click_bad = {"test_url": "p0", "paginate": {"p0": "p1"}, "has_click": True, "click_raises": True}
    const_next = {"test_url": "p0", "next_url": "p1"}        # constant _test_next_url, no paginate
    next_eq_cur = {"test_url": "p0", "next_url": "p0",       # next == current -> paginate fallback
                   "paginate": {"p0": "p1", "p1": ""}}
    unicode_urls = {"test_url": "\U0001F600", "paginate": {"\U0001F600": "中", "中": ""}}

    out["extract_paginated_content"] = [
        page("pg_none", "a.next", None),               # page is None -> single empty-url page
        page("pg_no_selector", "", linear),            # empty selector -> single page
        page("pg_linear", "a.next", linear),           # 3-page linear walk
        page("pg_cycle", "a.next", cycle),             # cycle -> loop stops (replay safety)
        page("pg_max_pages", "a.next", boundary),      # MAX_PAGES boundary, loop_prevented False
        page("pg_click_ok", "a.next", click_ok),       # click no-op then paginate
        page("pg_click_raises", "a.next", click_bad),  # click raises -> break after first page
        page("pg_const_next", "a.next", const_next),   # constant _test_next_url
        page("pg_next_eq_current", "a.next", next_eq_cur),
        page("pg_unicode_urls", "a.next", unicode_urls),
        page("pg_single", "a.next", {"test_url": "only", "paginate": {"only": ""}}),
    ]

    target = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s4b.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    counts = {k: len(v) for k, v in out.items() if isinstance(v, list)}
    sys.stderr.write(f"wrote {target}: {sum(counts.values())} vectors {counts}\n")


if __name__ == "__main__":
    main()
