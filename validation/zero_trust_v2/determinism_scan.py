"""Phase 10 determinism audit: scan all three source trees for
nondeterminism constructs; classify hits as controlled/uncontrolled."""
import glob
import json
import re
from collections import Counter

PATTERNS = {
    "python": [
        (r'\btime\.time\(', 'time.time'),
        (r'datetime\.now\(|datetime\.utcnow\(', 'datetime.now'),
        (r'\brandom\.', 'random module'),
        (r'\buuid\.', 'uuid'),
        (r'os\.urandom', 'os.urandom'),
        (r'sys\.platform', 'platform branch'),
    ],
    "dart": [
        (r'DateTime\.now\(', 'DateTime.now'),
        (r'\bRandom\(', 'Random'),
        (r'Platform\.localeName', 'locale variance'),
        (r'Platform\.operatingSystem', 'platform branch'),
    ],
    "js": [
        (r'Date\.now\(|new Date\(\)', 'Date.now'),
        (r'Math\.random\(', 'Math.random'),
        (r'crypto\.randomUUID|randomBytes', 'random bytes'),
        (r'process\.platform', 'platform branch'),
    ],
}


def scan(root, lang, exts):
    hits = []
    for ext in exts:
        for p in glob.glob(f'{root}/**/*{ext}', recursive=True):
            norm = p.replace('\\', '/')
            if ('__pycache__' in norm or 'node_modules' in norm
                    or '.dart_tool' in norm):
                continue
            try:
                src = open(p, encoding='utf-8', errors='replace').read()
            except OSError:
                continue
            for pat, label in PATTERNS[lang]:
                for m in re.finditer(pat, src):
                    line = src[:m.start()].count('\n') + 1
                    hits.append({"file": norm, "line": line,
                                 "construct": label})
    return hits


res = {
    "python_core": scan('C:/Projects/wwx_ref_py/core', 'python', ['.py']),
    "dart_lib": scan('lib', 'dart', ['.dart']),
    "js_src": scan('C:/Projects/wwx_ref_js/src', 'js', ['.ts']),
}
for k, v in res.items():
    print(k, len(v), dict(Counter(h['construct'] for h in v)))
json.dump(res, open('validation/zero_trust_v2/determinism_scan_raw.json', 'w'),
          indent=1)
