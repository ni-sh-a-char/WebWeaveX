from __future__ import annotations
import re

def detect_languages(text: str):
    src = text or ""
    langs=[]
    if re.search(r"def\s+\w+\(", src): langs.append("python")
    if "import " in src and ("from '" in src or 'from "' in src): langs.append("javascript")
    if "fun " in src: langs.append("kotlin")
    if "public class" in src: langs.append("java")
    if "import 'package:" in src: langs.append("dart")
    return sorted(set(langs))
