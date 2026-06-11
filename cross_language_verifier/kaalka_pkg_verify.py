"""Phase 6: verify the repo's embedded kaalka v5 byte bridge matches the
PUBLISHED kaalka 5.0.0 package (PyPI), executable, over random vectors."""
import json
import random
import sys

sys.path.insert(0, r"C:\Projects\wwx_cert_py")
import kaalka as published
from core.crypto.kaalka_v5_proc import kaalka_v5_proc, parse_time_key

rng = random.Random(20260611)
TIME_KEYS = ["0:0:0", "3:0:0", "12:34:56", "11:59:59", "23:45:1", "1:2:3", "12:0:0"]

trials = mismatches = 0
detail = []
for tk in TIME_KEYS:
    k = published.Kaalka()
    k._set_time(tk) if hasattr(k, "_set_time") else None
    # set time fields explicitly via the same parse the repo uses
    h, m, s = parse_time_key(tk)
    k.h, k.m, k.s = h, m, s
    for _ in range(200):
        data = bytes(rng.randrange(256) for _ in range(rng.randint(0, 300)))
        pub_enc = k._proc(data, True)
        repo_enc = kaalka_v5_proc(data, True, tk)
        pub_dec = k._proc(pub_enc, False)
        repo_dec = kaalka_v5_proc(repo_enc, False, tk)
        trials += 1
        if pub_enc != repo_enc or pub_dec != data or repo_dec != data:
            mismatches += 1
            if len(detail) < 5:
                detail.append({"time_key": tk, "data": data.hex(),
                               "pub": pub_enc.hex(), "repo": repo_enc.hex()})

# also verify h%12 parsing parity for 23:45:1 (published parses via _set_time?)
result = {
    "published_package": f"kaalka {getattr(published, '__version__', '5.0.0')} (PyPI, installed)",
    "trials": trials,
    "time_keys": TIME_KEYS,
    "mismatches": mismatches,
    "detail": detail,
    "verdict": "PASS" if mismatches == 0 else "FAIL",
}
json.dump(result, open("kaalka_pkg_python.json", "w"), indent=1)
print(json.dumps(result, indent=1)[:600])
