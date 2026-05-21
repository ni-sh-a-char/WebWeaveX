from __future__ import annotations
import re

def extract_migration_guides(text: str):
    src = text or ''
    sections = [m.group(1).strip() for m in re.finditer(r'^#{1,6}\s+(.+)$', src, flags=re.MULTILINE) if 'migration' in m.group(1).lower() or 'upgrade' in m.group(1).lower()]
    changes = sorted(set(re.findall(r'\b(breaking change|deprecated|removed|renamed)\b', src, flags=re.I)))
    return {"sections": sorted(set(sections)), "change_markers": changes}
