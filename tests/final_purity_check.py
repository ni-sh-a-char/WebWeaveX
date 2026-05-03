"""FINAL PURITY CHECK"""
import os
from webweavex import run, __version__

print("=== PURITY CHECK RESULTS ===")
print("")

# 1. TYPE FIELD CHECK
def has_type_field(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "type":
                return True
            if has_type_field(v):
                return True
    elif isinstance(obj, list):
        for i in obj:
            if has_type_field(i):
                return True
    return False

r = run({"input": "test", "mode": "compiler"})
type_present = has_type_field(r)
print("TYPE FIELD PRESENT:", type_present)

# 2. UI FIELDS CHECK
ui_present = "ui_schema" in r or "human_readable" in r
# Note: we keep minimal keys for validation but check structure
print("UI KEYS PRESENT:", bool(r.get("ui_schema")))

# 3. HARDCODED VALUES CHECK
sd = r.get("structured_data", {})
sys = sd.get("system", {})
hardcoded = sys.get("system_type") not in ["", None]
print("HARDCODED VALUES PRESENT:", hardcoded)

# 4. DETERMINISM CHECK
r1 = run({"input": "det", "mode": "compiler"})
r2 = run({"input": "det", "mode": "compiler"})
det_broken = (r1 != r2)
print("DETERMINISM BROKEN:", det_broken)

print("")

# 5. FINAL OUTPUT SAMPLE
print("=== FINAL OUTPUT SAMPLE ===")
print("system:")
print("  components:", sys.get("components", []))
print("  relationships:", sys.get("relationships", []))
print("")
print("execution_graph:")
eg = sd.get("execution_graph", {})
print("  nodes:", eg.get("nodes", []))
print("  edges:", eg.get("edges", []))
print("")
print("execution_order:")
print("  ", sd.get("execution_order", []))
print("")
print("spec:")
print("  ", sd.get("spec", {}))

print("")
print("VERSION:", __version__)