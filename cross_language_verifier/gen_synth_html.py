"""Generate 10,000 deterministic synthetic HTML torture documents for
extraction parity (seeded, no time/machine state). Pure-ASCII JSON output."""
import json
import random
from html.entities import html5

SEED = 20260612
ENTITY_NAMES = sorted({n.rstrip(";") for n in html5})

U = "".join
TEXT_POOL = [
    "plain ascii text",
    "cafe" + chr(0x301) + " latin",
    U(map(chr, [0x4F60, 0x597D])),
    U(map(chr, [0x65E5, 0x672C, 0x8A9E])),
    U(map(chr, [0x0627, 0x0644, 0x0633, 0x0644, 0x0627, 0x0645])),
    U(map(chr, [0x05E9, 0x05DC, 0x05D5, 0x05DD])),
    U(map(chr, [0x0928, 0x092E, 0x0938])),
    U(map(chr, [0x0E2A, 0x0E27, 0x0E31, 0x0E2A])),
    U(map(chr, [0xC548, 0xB155])),
    chr(0x1F680) + chr(0x200D) + chr(0x1F525),
    "tab\there",
    "nbsp" + chr(0xA0) + "x",
    "zero" + chr(0x200B) + "width",
    "a < b and c > d",
    "quote ' and \" mix",
]
TAGS = ["div", "span", "p", "section", "article", "li", "td", "em", "strong", "b", "i", "u",
        "h4", "h5", "blockquote", "figure", "nav", "aside", "main", "footer", "header",
        "custom-tag", "x-widget", "ruby"]
VOIDS = ["br", "hr", "img", "input", "meta", "link"]


def rnd_text(rng):
    parts = []
    for _ in range(rng.randint(1, 4)):
        c = rng.randint(0, 9)
        if c < 6:
            parts.append(rng.choice(TEXT_POOL))
        elif c < 8:
            parts.append("&" + rng.choice(ENTITY_NAMES) + ";")
        elif c == 8:
            parts.append("&#%d;" % rng.randint(33, 0x2FFF))
        else:
            parts.append("&#x%x;" % rng.randint(0x21, 0x2FFF))
        parts.append(rng.choice([" ", "\n", "\t", "", "\n\t "]))
    return "".join(parts)


def rnd_attr(rng):
    name = rng.choice(["id", "class", "href", "title", "data-x", "aria-label", "name", "src"])
    val = rng.choice([
        "v" + str(rng.randint(0, 999)),
        "/path/" + str(rng.randint(0, 99)) + rng.choice(["", "/"]),
        "has > inside",
        "has ' inside",
        'has " inside',
        "&amp; entity",
        rng.choice(TEXT_POOL),
    ])
    style = rng.randint(0, 3)
    if style == 0:
        return f'{name}="{val.replace(chr(34), "&quot;")}"'
    if style == 1:
        return f"{name}='{val.replace(chr(39), '&#39;')}'"
    if style == 2 and " " not in val and '"' not in val and "'" not in val and ">" not in val:
        return f"{name}={val}"
    return name


def rnd_node(rng, depth):
    c = rng.randint(0, 12)
    if depth >= 5 or c <= 4:
        return rnd_text(rng)
    if c == 5:
        return f"<{rng.choice(VOIDS)} {rnd_attr(rng)}>"
    if c == 6:
        return f"<a {rnd_attr(rng)} href=\"{rnd_text(rng)[:30].replace(chr(34), '')}\">{rnd_text(rng)}</a>"
    if c == 7:
        return f"<h{rng.randint(1, 3)}>{rnd_text(rng)}</h{rng.randint(1, 3)}>"
    if c == 8:
        return f"<!-- {rnd_text(rng)[:40]} -->"
    if c == 9:
        return f"<script>var x = '{rnd_text(rng)[:40]}';</script>"
    if c == 10:
        return f"<pre>{rnd_text(rng)}\n\t keep \n</pre>"
    if c == 11:
        inner = "".join(rnd_node(rng, depth + 1) for _ in range(rng.randint(0, 3)))
        return f"<template>{inner}</template>" if rng.random() < 0.3 else \
            f"<ruby>{rnd_text(rng)[:10]}<rp>(</rp><rt>{rnd_text(rng)[:10]}</rt><rp>)</rp></ruby>"
    tag = rng.choice(TAGS)
    attrs = " ".join(rnd_attr(rng) for _ in range(rng.randint(0, 2)))
    inner = "".join(rnd_node(rng, depth + 1) for _ in range(rng.randint(0, 4)))
    close = rng.random() < 0.9  # 10% unclosed
    open_tag = f"<{tag} {attrs}>" if attrs else f"<{tag}>"
    return open_tag + inner + (f"</{tag}>" if close else "")


def main():
    rng = random.Random(SEED)
    vectors = {}
    while len(vectors) < 10000:
        vid = f"sx_{len(vectors):05d}"
        body = "".join(rnd_node(rng, 0) for _ in range(rng.randint(1, 6)))
        title = f"<title>{rnd_text(rng)[:60]}</title>" if rng.random() < 0.7 else ""
        doctype = "<!DOCTYPE html>" if rng.random() < 0.5 else ""
        vectors[vid] = f"{doctype}<html><head>{title}</head><body>{body}</body></html>" \
            if rng.random() < 0.8 else doctype + title + body
    with open("synth_html.json", "w", encoding="ascii") as f:
        json.dump(vectors, f, ensure_ascii=True)
    print(f"wrote synth_html.json with {len(vectors)} documents")


if __name__ == "__main__":
    main()
