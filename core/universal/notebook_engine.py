from __future__ import annotations
import json

def parse_notebook(text: str):
    src = text or ''
    try:
        obj = json.loads(src)
    except Exception:
        obj = {}
    cells = obj.get('cells', []) if isinstance(obj, dict) else []
    cell_types = sorted([c.get('cell_type','') for c in cells if isinstance(c, dict)])
    return {"cell_count": len(cells), "cell_types": cell_types}
