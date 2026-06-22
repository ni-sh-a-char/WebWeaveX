# JAVA_RUNTIME_FRONTIER_run_semantic_runtime

**Runtime frontier analysis (Phase B2). Verdict: PORTABLE for the `html=""` contract — next
executable target.** Canon `9625f4a`. Measured.

## Frontier

`run_semantic_runtime(url, html, text, ...)` (`core.semantic.semantic_orchestrator`) — runtime
closure **23 modules / 1179 lines**. No `ast.parse`. It fans to ~23 semantic engines
(entity-extraction/resolution, ontology, semantic-graph, alignment, diff, replay, memory, IR) plus
the HTML engines `extract_table_semantics` / `extract_ui_semantics`.

## bs4 behaviour (measured)

Unlike `query_documents` (bs4 never called at runtime), `run_semantic_runtime` **does** call
`BeautifulSoup` at runtime — but on `html or ""`. For **`html=""`** the parse is empty, so the
table/UI semantics are deterministically empty and the output is **bs4-independent** (identical to
the `heal_selector` empty-HTML pattern). → certifiable byte-exact for the `html=""` contract by
reimplementing the table/UI engines' empty-input result and porting the other ~21 engines. The
`html≠""` path needs the lxml/bs4 Soup engine (Tier C).

## Plan (next session — sizeable but tractable)

Port the 23-engine frontier as `io.webweavex.semantic.SemanticRuntime` (mirrors the document-IR
approach: read all engines → one class → vectors with engine-level sections → byte-exact test).
Likely co-certifies `run_semantic_for_extraction` (shares the orchestrator). Expected **+1–2 APIs →
95–96/128**. No epistemic engine, no `ast`, no Python change.

## Ranking note

This is now the **highest parity-gain / lowest-frontier portable target** remaining (the
ast-coupled semantic APIs are condition-B blocked; OCR/Playwright/platform are non-portable). It
is the correct next executable slice.
