from __future__ import annotations


def plan_extraction(seed: str):
    return {
        "crawl_order": [seed],
        "extraction_order": [seed],
        "repo_traversal": [seed],
        "doc_traversal": [seed],
        "chunk_processing": ["c000000"],
    }

