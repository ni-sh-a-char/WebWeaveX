import json
import sys
from types import SimpleNamespace

sys.path.insert(0, r"C:\Projects\wwx_cert_py")
import webweavex as w
from core.crypto.kaalka_hash_engine import compute_kaalka_hash as H

page1 = SimpleNamespace(url="https://x.test/1", _test_url="https://x.test/1")
page_chain = SimpleNamespace(
    url="https://l.test/a", _test_url="https://l.test/a",
    _test_paginate=lambda cur: {"https://l.test/a": "https://l.test/b",
                                "https://l.test/b": "https://l.test/c"}.get(cur, ""),
)
out = {
    "paginated_none": H(w.extract_paginated_content(None, ".next")),
    "paginated_basic": H(w.extract_paginated_content(page1, ".next")),
    "paginated_chain": H(w.extract_paginated_content(page_chain, ".next")),
    "modal_none": H(w.recover_modal_runtime(None)),
    "modal_html": H(w.recover_modal_runtime(None, html="<div class='modal'><button class='close'>x</button></div>")),
    "ingest_missing": H(w.ingest_input(r"C:\nonexistent\file.html")),
    "multimodal_missing": H(w.extract_multimodal(r"C:\nonexistent\img.png")),
}
print(json.dumps(out, indent=1, sort_keys=True))
