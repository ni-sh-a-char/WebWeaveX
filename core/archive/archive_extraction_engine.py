from __future__ import annotations

import zipfile
from pathlib import Path
from typing import Any, Dict

MAX_ARCHIVE_FILES = 10000


def extract_archive(path: str) -> Dict[str, Any]:
    if not Path(path).is_file():
        return {
            "files": [],
            "count": 0,
            "available": False,
            "reason": "file_not_found",
            "bounded": True,
        }

    try:
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()[:MAX_ARCHIVE_FILES]

            files = [
                {"path": name}
                for name in names
            ]
    except zipfile.BadZipFile as exc:
        return {
            "files": [],
            "count": 0,
            "available": False,
            "reason": str(exc)[:200],
            "bounded": True,
        }
    except Exception as exc:
        return {
            "files": [],
            "count": 0,
            "available": False,
            "reason": str(exc)[:200],
            "bounded": True,
        }

    return {
        "files": files,
        "count": len(files),
        "available": True,
        "bounded": True,
    }
