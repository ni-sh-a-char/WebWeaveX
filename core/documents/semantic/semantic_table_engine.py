from __future__ import annotations

import re


def extract_semantic_tables(text: str):
    source = text or ""
    rows = []
    for line in source.splitlines():
        if line.count("|") >= 2:
            rows.append(line.strip())
    markdown_tables = sorted(set(rows))
    html_tables = len(re.findall(r"<table\b", source, flags=re.IGNORECASE))
    return {"markdown_rows": markdown_tables, "html_table_count": html_tables}
