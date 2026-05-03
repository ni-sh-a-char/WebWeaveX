"""TRUE GRAPH COMPILER TEST"""
from webweavex import run, __version__

print("=== TRUE GRAPH COMPILER TEST ===")
print("")

tests = [
    "build REST API",
    "create docker app",
    "login system",
    "quantum trading engine"
]

for inp in tests:
    r = run({"input": inp, "mode": "compiler"})
    sd = r.get("structured_data", {})
    
    sys = sd.get("system", {})
    exec_graph = sd.get("execution_graph", {})
    
    comps = sys.get("components", [])
    edges = exec_graph.get("edges", [])
    sys_type = sys.get("system_type")
    arch = sys.get("architecture")
    
    print(inp[:18] + ": comps=" + str(len(comps)) + " edges=" + str(len(edges)) + ' type=""' + str(sys_type) + '"" arch=""' + str(arch) + '""')

print("")
print("VERSION:", __version__)