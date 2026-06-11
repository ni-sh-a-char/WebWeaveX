"""Phase 4: apply inventory-driven sanitization inside a release worktree.

Usage: python sanitize_release.py <inventory.json> <worktree_dir>
Removes ONLY files classified LEGACY / GENERATED / TEMPORARY, each with the
classification's justification recorded in removed_files_report.json.
"""
import json
import os
import sys

inv = json.load(open(sys.argv[1]))
wt = sys.argv[2]
REMOVE = {"LEGACY", "GENERATED", "TEMPORARY"}
removed, kept, missing = [], 0, 0
for e in inv["entries"]:
    if e["classification"] in REMOVE:
        p = os.path.join(wt, e["path"])
        if os.path.exists(p):
            os.remove(p)
            removed.append({"path": e["path"],
                            "classification": e["classification"],
                            "justification": e["purpose"],
                            "size": e["size"]})
        else:
            missing += 1
    else:
        kept += 1
report = {
    "branch": inv["branch"],
    "removed_count": len(removed),
    "removed_bytes": sum(r["size"] for r in removed),
    "retained_count": kept,
    "policy": "only LEGACY/GENERATED/TEMPORARY classifications removed; "
              "REQUIRED_*/UNKNOWN never touched; full history remains on "
              "the development branch",
    "removed": removed,
}
json.dump(report, open(os.path.join(wt, "removed_files_report.json"), "w"),
          indent=1)
print(f"{inv['branch']}: removed {len(removed)} "
      f"({report['removed_bytes']/1e6:.2f} MB), retained {kept}")
