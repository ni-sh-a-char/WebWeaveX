"""Generate the full HTML5 named-entity table for the JS runtime from Python's
html.entities.html5 — parity by construction with html.unescape/bs4."""
from html.entities import html5

entries = {}
for name, value in html5.items():
    key = name.rstrip(";")
    # semicolon form is canonical; prefer it when both exist
    if name.endswith(";") or key not in entries:
        entries[key] = value

lines = [
    "// @generated from Python html.entities.html5 by cross_language_verifier/gen_entities.py",
    "// Full HTML5 named character reference table -- byte parity with Python",
    "// html.unescape (bs4 html.parser convert_charrefs).",
    "/* eslint-disable */",
    "export const HTML_ENTITIES: Record<string, string> = {",
]
def esc_char(ch):
    o = ord(ch)
    if 0x20 <= o < 0x7F and ch not in '"\\':
        return ch
    if o <= 0xFFFF:
        return f"\\u{o:04x}"
    return f"\\u{{{o:x}}}"


for key in sorted(entries):
    esc = "".join(esc_char(ch) for ch in entries[key])
    lines.append(f'  "{key}": "{esc}",')
lines.append("};")
with open(r"C:\Projects\wwx_cert_js\src\runtime\htmlEntities.ts", "w", encoding="ascii") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote htmlEntities.ts with {len(entries)} entries")
