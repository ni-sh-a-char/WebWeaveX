#!/usr/bin/env python3
"""Generate validation/vectors/* from canonical Python runtime probes."""
from __future__ import annotations

from materialize_python import materialize
from canonical_probes import write_vectors


def main() -> None:
    print("Materializing origin/python core…")
    materialize()
    print("Running canonical probes…")
    out = write_vectors()
    print(f"Wrote vector families under {out}")


if __name__ == "__main__":
    main()
