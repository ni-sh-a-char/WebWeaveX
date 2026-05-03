"""FIND ALL TYPE FIELDS"""
import os

print("=== FINDING ALL TYPE FIELDS ===")
print("")

files_to_check = [
    "core/compiler_engine.py",
    "core/full_pipeline.py",
    "core/semantic_engine.py"
]

for f in files_to_check:
    with open(f) as fp:
        lines = fp.readlines()

    print("FILE:", f)
    for i, line in enumerate(lines):
        if '"type"' in line or "'type'" in line:
            print(f"  Line {i+1}: {line.strip()[:70]}")

print("")
print("SCAN COMPLETE")