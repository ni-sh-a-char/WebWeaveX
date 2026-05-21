from __future__ import annotations

from typing import Any, Dict, List

from ._normalize import normalize_imports, normalize_symbols


MAX_WORLD_FILES = 10000


def build_repository_world_model(
    repository_irs: List[Dict[str, Any]],
) -> Dict[str, Any]:

    bounded = repository_irs[:MAX_WORLD_FILES]

    files = []
    symbols: List[Dict[str, Any]] = []
    imports: List[Dict[str, Any]] = []

    for ir in bounded:

        path = ir.get("path")

        files.append(path)

        semantic_ast = ir.get("semantic_ast", {})

        symbols.extend(normalize_symbols(semantic_ast))

        imports.extend(normalize_imports(semantic_ast))

    return {
        "file_count": len(files),
        "files": sorted(
            str(f)
            for f in files
            if f
        ),
        "symbol_count": len(symbols),
        "import_count": len(imports),
        "symbols": symbols[:10000],
        "imports": imports[:10000],
        "bounded": True,
    }
