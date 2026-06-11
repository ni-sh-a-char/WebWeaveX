import json
import sys


def load(p):
    raw = open(p, "rb").read()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return json.loads(raw.decode("utf-16"))
    return json.loads(raw.decode("utf-8-sig"))


py = load("synth_py.json")
js = load("synth_js.json")
da = load("synth_dart.json")
ids = sorted(set(py) | set(js) | set(da))
match = 0
fails = []
for i in ids:
    if py.get(i) == js.get(i) == da.get(i) and py.get(i) is not None:
        match += 1
    else:
        fails.append({"id": i, "py": py.get(i), "js": js.get(i), "dart": da.get(i)})
print(json.dumps({"vectors": len(ids), "match_3way": match, "mismatches": len(fails),
                  "verdict": "PASS" if not fails else "FAIL"}, indent=1))
if fails:
    print(json.dumps(fails[:6], indent=1))
sys.exit(0 if not fails else 1)
