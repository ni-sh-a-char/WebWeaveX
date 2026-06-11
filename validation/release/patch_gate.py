"""Extend the python-validity gate in the Dart scanner (CRLF/regex safe)."""
p = 'lib/src/semantic_ir/python_ast_parser.dart'
raw = open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in raw else '\n'
src = raw.replace('\r\n', '\n')

BS = chr(92)
old = (
    "/// Crude Python-validity gate: rejects clearly non-Python statements.\n"
    "void _validateLine(String stripped, int lineno) {\n"
    "  if (stripped.isEmpty) return;\n"
    "  if (RegExp(r'^[<>%?" + BS + BS + "]').hasMatch(stripped)) "
    "throw _syntaxError(lineno);\n"
    "  if (RegExp(r'^[)" + BS + "]}]').hasMatch(stripped)) "
    "throw _syntaxError(lineno);\n"
    "}"
)
new = (
    "/// Python-validity gate: rejects lines that cannot begin a valid Python\n"
    "/// logical line (CPython ast.parse raises on all of these). Extended\n"
    "/// after real-world testing hit `/**`-led TypeScript sources that\n"
    "/// CPython rejects but the original narrow gate accepted. `*` (starred\n"
    "/// assignment), `.` (float literal), `+ - ~ @` (unary/decorator) remain\n"
    "/// valid starters.\n"
    "void _validateLine(String stripped, int lineno) {\n"
    "  if (stripped.isEmpty) return;\n"
    "  if (RegExp(r'^[<>%?" + BS + BS + "/,;:=&|!)" + BS + "]}]')"
    ".hasMatch(stripped)) {\n"
    "    throw _syntaxError(lineno);\n"
    "  }\n"
    "}"
)
assert old in src, 'gate block not found'
src = src.replace(old, new)
open(p, 'w', encoding='utf-8', newline='').write(src.replace('\n', nl))
print('dart gate extended')
