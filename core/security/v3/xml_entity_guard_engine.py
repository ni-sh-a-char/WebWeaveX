from __future__ import annotations


def guard_xml_entities_v3(xml_text: str):
    source = (xml_text or "").lower()
    blocked = "<!entity" in source or "<!doctype" in source
    return {"allowed": not blocked}
