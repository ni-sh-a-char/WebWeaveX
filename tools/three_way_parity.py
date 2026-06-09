"""Three-way public API comparison: Python (canonical) vs JavaScript vs Dart.

Measured from real branch sources via git. No assumptions. Emits a JSON-ish
summary to stdout and writes a name-level table to tools/_three_way.tsv.
"""
import ast
import os
import re
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def show(ref):
    return subprocess.check_output(
        ["git", "-C", REPO, "show", ref], stderr=subprocess.DEVNULL
    ).decode("utf-8", "replace")


def python_all():
    src = show("origin/python:webweavex/__init__.py")
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "__all__":
                    return [e.value for e in node.value.elts
                            if isinstance(e, ast.Constant)]
    return []


def js_names():
    names = set()
    refs = ["origin/javascript:src/index.ts",
            "origin/javascript:src/publicApi.ts",
            "origin/javascript:src/connectors/index.ts"]
    for ref in refs:
        try:
            src = show(ref)
        except Exception:
            continue
        for m in re.finditer(r"export\s*\{([^}]*)\}", src, re.S):
            for part in m.group(1).split(","):
                part = part.strip()
                if not part:
                    continue
                nm = (part.split(" as ")[-1] if " as " in part
                      else part.split()[0]).strip()
                if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", nm):
                    names.add(nm)
        for m in re.finditer(
                r"export\s+(?:async\s+)?(?:function|const|class)\s+([A-Za-z0-9_]+)",
                src):
            names.add(m.group(1))
    return names


def dart_symbols():
    funcs, classes = set(), set()
    func_re = re.compile(
        r"^(?:Future<[^>]*>|Map<[^>]*>|List<[^>]*>|Set<[^>]*>|"
        r"Iterable<[^>]*>|String|int|double|bool|void|RuntimeGraph|"
        r"dynamic|num|Object|[A-Z][A-Za-z0-9_]*\??) +([a-z][A-Za-z0-9_]*)\s*\(")
    class_re = re.compile(r"^(?:abstract\s+)?class\s+([A-Z][A-Za-z0-9_]*)")
    for root, _, files in os.walk(os.path.join(REPO, "lib")):
        for fn in files:
            if not fn.endswith(".dart"):
                continue
            with open(os.path.join(root, fn), encoding="utf-8",
                      errors="replace") as fh:
                for line in fh:
                    m = func_re.match(line)
                    if m:
                        funcs.add(m.group(1))
                    c = class_re.match(line)
                    if c:
                        classes.add(c.group(1))
    return funcs, classes


def snake_to_camel(s):
    parts = s.split("_")
    return parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:])


def main():
    py = python_all()
    js = js_names()
    funcs, classes = dart_symbols()
    dart = funcs | classes
    dart_lower = {s.lower(): s for s in dart}
    js_lower = {s.lower(): s for s in js}

    rows = []
    js_hit = dart_hit = 0
    for name in py:
        if name in ("__version__", "version"):
            continue
        camel = snake_to_camel(name)
        pascal = camel[:1].upper() + camel[1:]
        in_js = (camel in js or pascal in js or camel.lower() in js_lower)
        in_dart = (camel in dart or pascal in dart or camel.lower() in dart_lower)
        js_hit += in_js
        dart_hit += in_dart
        rows.append((name, camel, in_js, in_dart))

    total = len(rows)
    with open(os.path.join(REPO, "tools", "_three_way.tsv"), "w",
              encoding="utf-8") as fh:
        fh.write("python\tcamel\tin_js\tin_dart\n")
        for r in rows:
            fh.write(f"{r[0]}\t{r[1]}\t{int(r[2])}\t{int(r[3])}\n")

    print(f"Python canonical APIs (excl version): {total}")
    print(f"JS name-present:   {js_hit}/{total}")
    print(f"Dart name-present: {dart_hit}/{total}")
    print("--- Python APIs MISSING a JS name ---")
    for n, c, j, d in rows:
        if not j:
            print(f"  {n}")
    print("--- Python APIs MISSING a Dart name ---")
    for n, c, j, d in rows:
        if not d:
            print(f"  {n}  (js={'Y' if j else 'N'})")


if __name__ == "__main__":
    main()
