import os
cur = None
tot = hit = 0
files = {}
for line in open("coverage/lcov.info", encoding="utf-8"):
    line = line.strip()
    if line.startswith("SF:"):
        cur = line[3:].replace("\\", "/")
        files[cur] = [0, 0]
    elif line.startswith("DA:"):
        _, rest = line.split(":", 1)
        parts = rest.split(",")
        cnt = int(parts[1])
        files[cur][0] += 1
        tot += 1
        if cnt > 0:
            files[cur][1] += 1
            hit += 1
print(f"TOTAL: {hit}/{tot} = {hit/tot*100:.2f}%")
print("--- files below 90% ---")
below = []
for f, (t, h) in files.items():
    pct = h / t * 100 if t else 100.0
    if pct < 90:
        below.append((pct, h, t, f))
for pct, h, t, f in sorted(below):
    short = f.split("/lib/")[-1] if "/lib/" in f else f
    print(f"  {pct:6.2f}%  {h}/{t}  {short}")
print(f"files below 90%: {len(below)} of {len(files)}")
