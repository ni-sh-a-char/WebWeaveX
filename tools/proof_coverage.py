"""Phase 3 proof-coverage audit: every COMPLETE API must be exercised by a test.

Parses PUBLIC_API_MATRIX.md for status==Complete rows (python_name, dart_symbol),
then checks whether each dart_symbol is referenced in any test/**/*.dart file
AND whether the python_name/symbol appears in any validation/**/*.json vector.
Reports any COMPLETE API lacking executed proof.
"""
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATRIX = os.path.join(REPO, "PUBLIC_API_MATRIX.md")


def complete_rows():
    rows = []
    for line in open(MATRIX, encoding="utf-8"):
        # | family | `name` | ✅ | `dart` | ✅ Complete |
        if "Complete" not in line or not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        if "Complete" not in cells[-1]:
            continue
        pyname = cells[1].strip("`")
        dart = cells[3].strip("`")
        if dart == "—" or not dart:
            dart = ""
        rows.append((pyname, dart))
    return rows


def all_test_text():
    blobs = []
    for root, _, files in os.walk(os.path.join(REPO, "test")):
        for fn in files:
            if fn.endswith(".dart"):
                blobs.append(open(os.path.join(root, fn), encoding="utf-8",
                                  errors="replace").read())
    return "\n".join(blobs)


def all_vector_text():
    blobs = []
    for root, _, files in os.walk(os.path.join(REPO, "validation")):
        for fn in files:
            if fn.endswith(".json"):
                blobs.append(open(os.path.join(root, fn), encoding="utf-8",
                                  errors="replace").read())
    return "\n".join(blobs)


def main():
    rows = complete_rows()
    tests = all_test_text()
    vectors = all_vector_text()

    no_symbol = []
    no_test = []
    no_vector = []
    for pyname, dart in rows:
        if not dart:
            no_symbol.append(pyname)
            continue
        # symbol referenced in a test?
        sym = dart.split(".")[0]
        if not re.search(r"\b" + re.escape(sym) + r"\b", tests):
            no_test.append((pyname, dart))
        # python name or symbol present in a vector file?
        if (pyname not in vectors) and (sym not in vectors):
            no_vector.append((pyname, dart))

    print(f"COMPLETE rows: {len(rows)}")
    print(f"COMPLETE without dart symbol (matrix anomaly): {len(no_symbol)}")
    for n in no_symbol:
        print(f"   {n}")
    print(f"\nCOMPLETE whose dart symbol is NOT referenced in any test: {len(no_test)}")
    for n, d in no_test:
        print(f"   {n}  ->  {d}")
    print(f"\nCOMPLETE with no name/symbol in any validation vector json: {len(no_vector)}")
    for n, d in no_vector:
        print(f"   {n}  ->  {d}")


if __name__ == "__main__":
    main()
