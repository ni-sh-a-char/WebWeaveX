import json
import sys


def walk(p, j, path=""):
    if type(p) is not type(j) and not (isinstance(p, (int, float)) and isinstance(j, (int, float))):
        print("TYPE", path, type(p).__name__, type(j).__name__)
        return
    if isinstance(p, dict):
        for k in sorted(set(p) | set(j)):
            if k not in p:
                print("JS-ONLY", path + "/" + k, json.dumps(j[k], ensure_ascii=True)[:90])
            elif k not in j:
                print("PY-ONLY", path + "/" + k, json.dumps(p[k], ensure_ascii=True)[:90])
            else:
                walk(p[k], j[k], path + "/" + k)
    elif isinstance(p, list):
        if len(p) != len(j):
            print("LEN", path, len(p), len(j))
            return
        for i, (a, b) in enumerate(zip(p, j)):
            walk(a, b, path + f"[{i}]")
    elif p != j:
        print("VAL", path, "py:", json.dumps(p, ensure_ascii=True)[:90],
              "js:", json.dumps(j, ensure_ascii=True)[:90])


p = json.load(open(sys.argv[1], encoding="utf-8"))
j = json.load(open(sys.argv[2], encoding="utf-8"))
walk(p, j)
print("diff done")
