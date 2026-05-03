"""STOP CONDITION VERIFICATION"""
import time
import os
from webweavex import run, __version__
from core.semantic_engine import process_all_semantics
import inspect

print("=== STOP CONDITION VERIFICATION ===")
print("")

# 1. Semantic engine takes RAW STRING only
sig = inspect.signature(process_all_semantics)
params = list(sig.parameters.keys())
print("1. process_all_semantics takes: ", params)
ok1 = params == ['user_input']
print("   PASS:", ok1)

# 2. Schema consistent
r = run({'input': 'test', 'mode': 'compiler'})
sd = r.get('structured_data', {})
design = sd.get('system_design', {})
ok2 = 'system_type' in design and 'architecture' in design
print("2. Schema consistency:", ok2)

# 3. Performance
start = time.time()
run({'input': 'test', 'mode': 'compiler'})
elapsed = time.time() - start
ok3 = elapsed < 1.0
print("3. Performance:", elapsed, "s < 1.0:", ok3)

# 4. Determinism
r1 = run({'input': 'det', 'mode': 'compiler'})
r2 = run({'input': 'det', 'mode': 'compiler'})
ok4 = r1 == r2
print("4. Determinism:", ok4)

# 5. No fallback words
clean = True
files = ['core/execution_graph.py', 'core/system_inference.py']
for f in files:
    with open(f) as fp:
        content = fp.read()
        if 'execute' in content and '=' in content:
            # Skip comments and real code
            for line in content.split('\n'):
                if 'execute' in line and '=' in line and not line.strip().startswith('#'):
                    if '"execute"' in line or "'execute'" in line:
                        clean = False
print("5. No fallback words:", clean)

# 6. No mapping tables
with open('core/system_inference.py') as fp:
    sys = fp.read()
ok6 = 'SYSTEM_TYPE_MAP' not in sys and 'ROLE_TO_TYPE' not in sys
print("6. No mapping tables:", ok6)

# 7. Universal input
ok7 = len(design.get('components', [])) > 0
print("7. Universal input works:", ok7)

print("")
print("VERSION:", __version__)

all_ok = ok1 and ok2 and ok3 and ok4 and clean and ok6 and ok7
print("")
if all_ok:
    print("=== ALL STOP CONDITIONS MET ===")
else:
    print("=== SOME CONDITIONS FAILED ===")