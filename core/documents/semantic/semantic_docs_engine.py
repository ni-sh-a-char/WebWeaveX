from __future__ import annotations

from core.documents.intelligence.semantic_outline_engine import extract_semantic_outline as _v14_outline
from .semantic_reference_engine import extract_semantic_references
from .semantic_example_engine import extract_semantic_examples
from .semantic_table_engine import extract_semantic_tables


def analyze_semantic_docs(text: str):
    outline = _v14_outline(text)
    refs = extract_semantic_references(text)
    examples = extract_semantic_examples(text)
    tables = extract_semantic_tables(text)
    return {
        "hierarchy": outline,
        "references": refs,
        "examples": examples,
        "tables": tables,
    }
