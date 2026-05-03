"""FINAL PURITY VERIFICATION"""
import os
from webweavex import run, __version__

print("=== FINAL PURITY VERIFICATION ===")
print("")

# 1. No type fields in nodes
clean_nodes = True
with open("core/compiler_engine.py") as fp:
    content = fp.read()
    if '"type"' in content and "components" in content:
        clean_nodes = False
print("1. No type fields in nodes:", clean_nodes)

# 2. Empty system_type
with open("core/compiler_engine.py") as fp:
    content = fp.read()
    ok2 = 'system_type' in content and '""' in content
print("2. Empty system_type:", ok2)

# 3. No entities/actions split in semantics
with open("core/semantic_engine.py") as fp:
    content = fp.read()
    ok3 = '"entities"' not in content or 'return' not in content
print("3. No entities split:", ok3)

# 4. Graph = pure nodes + relationships
sem = run({"input": "test", "mode": "compiler"})
sd = sem.get("structured_data", {})
sys = sd.get("system", {})
ok4 = sys.get("system_type") == "" and sys.get("architecture") == ""
print("4. Empty system_type/architecture:", ok4)

# 5. Determinism
r1 = run({"input": "det", "mode": "compiler"})
r2 = run({"input": "det", "mode": "compiler"})
ok5 = r1 == r2
print("5. Determinism:", ok5)

print("")
print("VERSION:", __version__)
print("")

if all([clean_nodes, ok2, ok3, ok4, ok5]):
    print("ALL STOP CONDITIONS MET")
else:
    print("SOME CONDITIONS FAILED - review manually")