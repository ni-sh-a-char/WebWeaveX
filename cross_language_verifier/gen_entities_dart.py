"""Generate lib/src/soup/html_entities.dart from Python html.entities.html5."""
from html.entities import html5

entries = {}
for name, value in html5.items():
    key = name.rstrip(";")
    if name.endswith(";") or key not in entries:
        entries[key] = value


def esc_char(ch):
    o = ord(ch)
    if 0x20 <= o < 0x7F and ch not in "\"\\$":
        return ch
    if o <= 0xFFFF:
        return f"\\u{o:04x}"
    return f"\\u{{{o:x}}}"


lines = [
    "// @generated from Python html.entities.html5 by",
    "// cross_language_verifier/gen_entities_dart.py -- byte parity with Python",
    "// html.unescape (bs4 html.parser convert_charrefs). Do not edit by hand.",
    "",
    "const Map<String, String> htmlEntities = {",
]
for key in sorted(entries):
    esc = "".join(esc_char(ch) for ch in entries[key])
    lines.append(f'  "{key}": "{esc}",')
lines.append("};")
with open(r"C:\Projects\WebWeaveX\lib\src\soup\html_entities.dart", "w", encoding="ascii") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote html_entities.dart with {len(entries)} entries")
