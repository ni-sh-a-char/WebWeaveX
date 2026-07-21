#!/usr/bin/env python3
"""Verify that every exported symbol in the Dart barrel export actually exists in its source file."""

import re
import os
from pathlib import Path

BARREL = r"C:\Projects\wwx-dart-verify\lib\webweavex.dart"
LIB_DIR = r"C:\Projects\wwx-dart-verify\lib"

def parse_barrel(barrel_path):
    """Parse export statements from the barrel file, return list of (file, symbols)."""
    content = Path(barrel_path).read_text()
    exports = []
    # Match: export '...' show sym1, sym2, ...;
    for m in re.finditer(r"export\s+'([^']+)'(?:\s+show\s+([^;]+))?\s*;", content):
        uri = m.group(1)
        if m.group(2):
            syms = [s.strip() for s in m.group(2).split(",")]
        else:
            syms = None  # wildcard export (all public)
        exports.append((uri, syms))
    return exports

def resolve_uri(uri):
    """Convert package URI to filesystem path."""
    # 'package:webweavex/src/foo/bar.dart' -> 'lib/src/foo/bar.dart'
    m = re.match(r"package:webweavex/(.+)", uri)
    if m:
        return os.path.join(LIB_DIR, m.group(1))
    return None

def check_file_has_symbols(file_path, symbols):
    """Check that a file contains all the listed symbols."""
    content = Path(file_path).read_text()
    missing = []
    for sym in symbols:
        # Check for class, abstract class, mixin, enum, typedef, function, extension, const, final, top-level var
        patterns = [
            rf"\bclass\s+{re.escape(sym)}\b",
            rf"\bmixin\s+{re.escape(sym)}\b",
            rf"\benum\s+{re.escape(sym)}\b",
            rf"\btypedef\s+{re.escape(sym)}\b",
            rf"\bextension\s+{re.escape(sym)}\b",
            rf"\b{re.escape(sym)}\s*\(",  # function call / definition
            rf"\bconst\s+{re.escape(sym)}\b",
            rf"\bfinal\s+{re.escape(sym)}\b",
            rf"\b{re.escape(sym)}\s*=",  # top-level variable
        ]
        found = any(re.search(p, content) for p in patterns)
        if not found:
            missing.append(sym)
    return missing

def main():
    exports = parse_barrel(BARREL)
    total = 0
    missing_total = 0
    missing_details = []

    for uri, symbols in exports:
        fpath = resolve_uri(uri)
        if fpath is None:
            print(f"WARN: Cannot resolve URI: {uri}")
            continue
        if not os.path.exists(fpath):
            print(f"MISSING FILE: {uri} -> {fpath}")
            continue
        if symbols is None:
            # Wildcard export — skip symbol check
            print(f"  WILDCARD: {uri}")
            continue
        total += len(symbols)
        missing = check_file_has_symbols(fpath, symbols)
        if missing:
            missing_total += len(missing)
            missing_details.append((uri, missing))
            print(f"MISSING SYMBOLS in {uri}:")
            for s in missing:
                print(f"  - {s}")
        else:
            print(f"  OK: {uri} ({len(symbols)} symbols)")

    print(f"\n{'='*60}")
    print(f"Total checked symbols: {total}")
    print(f"Missing symbols: {missing_total}")
    if missing_details:
        print("\nMissing details:")
        for uri, syms in missing_details:
            print(f"  {uri}: {syms}")
    else:
        print("\nAll symbols verified present.")

if __name__ == "__main__":
    main()
