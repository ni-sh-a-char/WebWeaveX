"""Phase 11: fetch a diverse real-internet HTML corpus ONCE (single source of
bytes for every language). Polite: sequential per host, ~0.3s delay, UA set."""
import hashlib
import json
import time
import urllib.request
from pathlib import Path

OUT = Path("corpus")
OUT.mkdir(exist_ok=True)

CURATED = [
    "https://en.wikipedia.org/wiki/Unicode",
    "https://en.wikipedia.org/wiki/HTML",
    "https://ar.wikipedia.org/wiki/%D9%84%D8%BA%D8%A9_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9",
    "https://he.wikipedia.org/wiki/%D7%99%D7%A8%D7%95%D7%A9%D7%9C%D7%99%D7%9D",
    "https://zh.wikipedia.org/wiki/%E4%B8%AD%E6%96%87",
    "https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC%E8%AA%9E",
    "https://ko.wikipedia.org/wiki/%ED%95%9C%EA%B5%AD%EC%96%B4",
    "https://hi.wikipedia.org/wiki/%E0%A4%B9%E0%A4%BF%E0%A4%A8%E0%A5%8D%E0%A4%A6%E0%A5%80",
    "https://th.wikipedia.org/wiki/%E0%B8%A0%E0%B8%B2%E0%B8%A9%E0%B8%B2%E0%B9%84%E0%B8%97%E0%B8%A2",
    "https://ru.wikipedia.org/wiki/%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9_%D1%8F%D0%B7%D1%8B%D0%BA",
    "https://developer.mozilla.org/en-US/docs/Web/HTML",
    "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
    "https://docs.python.org/3/library/json.html",
    "https://docs.python.org/3/tutorial/index.html",
    "https://dart.dev/language",
    "https://nodejs.org/en",
    "https://www.w3.org/TR/html52/",
    "https://www.rfc-editor.org/rfc/rfc8259",
    "https://github.com/torvalds/linux",
    "https://github.com/python/cpython",
    "https://news.ycombinator.com/",
    "https://example.com/",
    "https://www.gnu.org/licenses/gpl-3.0.en.html",
    "https://peps.python.org/pep-0008/",
    "https://go.dev/doc/",
    "https://www.kernel.org/",
    "https://archive.org/about/",
    "https://www.apache.org/licenses/LICENSE-2.0",
    "https://en.wikibooks.org/wiki/Main_Page",
    "https://commons.wikimedia.org/wiki/Main_Page",
]
RANDOM_SOURCES = [
    ("https://en.wikipedia.org/wiki/Special:Random", 330),
    ("https://de.wikipedia.org/wiki/Spezial:Zuf%C3%A4llige_Seite", 120),
    ("https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard", 120),
    ("https://es.wikipedia.org/wiki/Especial:Aleatoria", 120),
    ("https://ja.wikipedia.org/wiki/%E7%89%B9%E5%88%A5:%E3%81%8A%E3%81%BE%E3%81%8B%E3%81%9B%E8%A1%A8%E7%A4%BA", 100),
    ("https://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%A1%D0%BB%D1%83%D1%87%D0%B0%D0%B9%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0", 60),
    ("https://zh.wikipedia.org/wiki/Special:%E9%9A%8F%E6%9C%BA%E9%A1%B5%E9%9D%A2", 50),
    ("https://ar.wikipedia.org/wiki/%D8%AE%D8%A7%D8%B5:%D8%B5%D9%81%D8%AD%D8%A9_%D8%B9%D8%B4%D9%88%D8%A7%D8%A6%D9%8A%D8%A9", 40),
    ("https://it.wikipedia.org/wiki/Speciale:PaginaCasuale", 40),
]

HEADERS = {"User-Agent": "WebWeaveX-parity-verifier/1.0 (cross-language extraction certification)"}


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        final_url = r.geturl()
        data = r.read()
    return final_url, data


def main():
    manifest = []
    seen = set()

    def save(url, data, final_url):
        digest = hashlib.sha256(data).hexdigest()
        if digest in seen:
            return False
        seen.add(digest)
        name = f"page_{len(manifest):04d}.html"
        (OUT / name).write_bytes(data)
        manifest.append({"file": name, "url": url, "final_url": final_url,
                         "bytes": len(data), "sha256": digest})
        return True

    for url in CURATED:
        try:
            final_url, data = fetch(url)
            save(url, data, final_url)
            print(f"ok  {len(manifest):4d} {url[:80]}")
        except Exception as e:  # noqa: BLE001
            print(f"ERR {url[:80]} {type(e).__name__}: {e}")
        time.sleep(0.3)

    for src, n in RANDOM_SOURCES:
        for _ in range(n):
            try:
                final_url, data = fetch(src)
                save(src, data, final_url)
            except Exception as e:  # noqa: BLE001
                print(f"ERR random {type(e).__name__}: {e}")
            time.sleep(0.3)
        print(f"random batch {src[:50]} -> total {len(manifest)}")

    json.dump(manifest, open(OUT / "manifest.json", "w", encoding="utf-8"), indent=1)
    print(f"corpus: {len(manifest)} pages")


if __name__ == "__main__":
    main()
