"""Generate full Python html.unescape tables for JS and Dart: entities (with
and without semicolon), _invalid_charrefs, _invalid_codepoints. Byte parity by
construction with Python html.unescape / bs4 convert_charrefs."""
from html import _invalid_charrefs, _invalid_codepoints
from html.entities import html5


def esc_char(ch, dollar=False):
    o = ord(ch)
    bad = "\"\\" + ("$" if dollar else "")
    if 0x20 <= o < 0x7F and ch not in bad:
        return ch
    if o <= 0xFFFF:
        return f"\\u{o:04x}"
    return f"\\u{{{o:x}}}"


def esc(s, dollar=False):
    return "".join(esc_char(c, dollar) for c in s)


with_semi = {k[:-1]: v for k, v in html5.items() if k.endswith(";")}
no_semi = {k: v for k, v in html5.items() if not k.endswith(";")}

# --- JavaScript ---
js = [
    "// @generated from Python html module by cross_language_verifier/gen_unescape_tables.py",
    "// Full Python html.unescape semantics: named entities (with and without",
    "// semicolon), numeric charrefs with the cp1252 invalid-charref map and",
    "// invalid-codepoint rules. Do not edit by hand.",
    "/* eslint-disable */",
    "export const HTML_ENTITIES: Record<string, string> = {",
]
for k in sorted(with_semi):
    js.append(f'  "{k}": "{esc(with_semi[k])}",')
js.append("};")
js.append("export const HTML_ENTITIES_NO_SEMI: Record<string, string> = {")
for k in sorted(no_semi):
    js.append(f'  "{k}": "{esc(no_semi[k])}",')
js.append("};")
js.append("export const INVALID_CHARREFS: Record<number, string> = {")
for k in sorted(_invalid_charrefs):
    js.append(f'  {k}: "{esc(_invalid_charrefs[k])}",')
js.append("};")
js.append("export const INVALID_CODEPOINTS: Set<number> = new Set([")
js.append("  " + ", ".join(str(c) for c in sorted(_invalid_codepoints)) + ",")
js.append("]);")
open(r"C:\Projects\wwx_js\src\runtime\htmlEntities.ts", "w", encoding="ascii").write("\n".join(js) + "\n")

# --- Dart ---
da = [
    "// @generated from Python html module by",
    "// cross_language_verifier/gen_unescape_tables.py -- full Python",
    "// html.unescape semantics. Do not edit by hand.",
    "",
    "const Map<String, String> htmlEntities = {",
]
for k in sorted(with_semi):
    da.append(f'  "{k}": "{esc(with_semi[k], dollar=True)}",')
da.append("};")
da.append("")
da.append("const Map<String, String> htmlEntitiesNoSemi = {")
for k in sorted(no_semi):
    da.append(f'  "{k}": "{esc(no_semi[k], dollar=True)}",')
da.append("};")
da.append("")
da.append("const Map<int, String> invalidCharrefs = {")
for k in sorted(_invalid_charrefs):
    da.append(f'  {k}: "{esc(_invalid_charrefs[k], dollar=True)}",')
da.append("};")
da.append("")
da.append("const Set<int> invalidCodepoints = {")
da.append("  " + ", ".join(str(c) for c in sorted(_invalid_codepoints)) + ",")
da.append("};")
open(r"C:\Projects\WebWeaveX\lib\src\soup\html_entities.dart", "w", encoding="ascii").write("\n".join(da) + "\n")

print(f"with_semi={len(with_semi)} no_semi={len(no_semi)} "
      f"invalid_charrefs={len(_invalid_charrefs)} invalid_codepoints={len(_invalid_codepoints)}")
