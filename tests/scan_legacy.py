"""SCAN ALL LEGACY STRUCTURES"""
import os

print("=== SCANNING FOR LEGACY STRUCTURES ===")
print("")

legacy_terms = [
    "entities", "actions", "action_pairs",
    "semantic_category", "role_mapping",
    "template", "inference_map",
    "ui_schema", "human_readable"
]

files_to_scan = []
for root, dirs, files in os.walk("core"):
    for f in files:
        if f.endswith(".py"):
            files_to_scan.append(os.path.join(root, f))

violations = []

for f in files_to_scan:
    with open(f) as fp:
        lines = fp.readlines()
    
    for i, line in enumerate(lines):
        for term in legacy_terms:
            if term in line.lower() and not line.strip().startswith("#"):
                violations.append(f"{f}:{i+1}: {line.strip()[:50]}")

print(f"VIOLATIONS FOUND: {len(violations)}")
for v in violations[:20]:
    print("  ", v)

if len(violations) > 20:
    print(f"  ... and {len(violations) - 20} more")

print("")
print("SCAN COMPLETE")