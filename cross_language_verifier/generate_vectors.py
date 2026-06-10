"""Deterministic cross-language torture-vector generator.

Generates vectors.json: 1000+ vectors covering Unicode (Latin, Hindi, Arabic,
Chinese, Japanese, Korean, emoji, combining marks, astral plane, RTL/bidi,
compatibility characters), float determinism, key ordering, nested structures,
volatile-key stripping, and large payloads. Fully seeded — no time, no
machine-dependent state.

Input-domain contract (documented, enforced by construction):
- integers must satisfy |n| <= 2^53 (JavaScript exact-integer zone)
- strings must be valid Unicode scalar sequences (no lone surrogates)
"""
import json
import random

SEED = 20260611
ENCRYPTION_KEY = "wwx-cross-language-verifier-key-α\U0001F680"

# -- curated unicode samples (explicit code points; file stays pure ASCII) ----
U = "".join
SAMPLES = {
    "latin_nfd": "cafe" + chr(0x301) + " Vie" + chr(0x302) + "t Nam",
    "latin_nfc": "café Ångström straße",
    "fullwidth": U(map(chr, [0xFF37, 0xFF45, 0xFF42, 0xFF37, 0xFF45, 0xFF41, 0xFF56, 0xFF45])),
    "compat": U(map(chr, [0x2460, 0x00B2, 0xFB01, 0x3392, 0x2126, 0x212B, 0x01C4])),
    "hindi": U(map(chr, [0x0928, 0x092E, 0x0938, 0x094D, 0x0924, 0x0947, 0x0020, 0x0926, 0x0941, 0x0928, 0x093F, 0x092F, 0x093E])),
    "arabic": U(map(chr, [0x0627, 0x0644, 0x0633, 0x0644, 0x0627, 0x0645, 0x0020, 0x0639, 0x0644, 0x064A, 0x0643, 0x0645])),
    "arabic_pres": U(map(chr, [0xFEFB, 0xFE8D, 0xFEE0])),
    "chinese": U(map(chr, [0x4F60, 0x597D, 0x4E16, 0x754C, 0x3002])),
    "japanese": U(map(chr, [0x30B3, 0x30F3, 0x30CB, 0x30C1, 0x30CF, 0x0020, 0x30AB, 0x3099])),
    "korean_syllables": U(map(chr, [0xC548, 0xB155, 0xD558, 0xC138, 0xC694])),
    "korean_jamo": U(map(chr, [0x1112, 0x1161, 0x11AB, 0x1100, 0x1173, 0x11AF])),
    "emoji": U(map(chr, [0x1F680, 0x1F525, 0x1F468, 0x200D, 0x1F469, 0x200D, 0x1F467, 0x1F3FD])),
    "astral_gothic": U(map(chr, [0x10330, 0x10331, 0x10332])),
    "astral_math": U(map(chr, [0x1D400, 0x1D401, 0x1D7D8])),
    "combining_stack": "e" + U(map(chr, [0x0301, 0x0316, 0x0327, 0x0334])),
    "rtl_mixed": "abc " + U(map(chr, [0x05E9, 0x05DC, 0x05D5, 0x05DD])) + " def",
    "bidi_controls": chr(0x202E) + "reversed" + chr(0x202C),
    "line_seps": "a" + chr(0x2028) + "b" + chr(0x2029) + "c",
    "controls": "tab\tnl\nbell\x07esc\x1bdel\x7f",
    "whitespace_tail": "trailing  \t ",
    "crlf": "line1\r\nline2\rline3",
    "replacement": chr(0xFFFD) + "x" + chr(0xE000),
    "empty": "",
}

FLOATS = [
    42, 42.0, 0.0, -0.0, 1e6, 1.5, -2.5, 0.1, 1.0 / 3.0, 2.0 / 3.0,
    0.0001, 0.00001, 5e-7, 1e-10, 1.5e-300, 5e300, 1e16, 1.5e16, 1e19,
    1e21, 1.5e21, 9.007199254740991e15, 123456.789, 123456789.123456789,
    -123456.789, 3.141592653589793, 2.718281828459045, 1e15 + 0.5,
    0.30000000000000004, 9007199254740991, -9007199254740991, 0, 1, -1,
]

KEY_SETS = [
    ["b", "a", "B", "A", "0", "9", "_", "~"],
    [chr(0xFFFD), chr(0x1F680), "A", chr(0xE000), chr(0x10000), "z"],
    [SAMPLES["hindi"][:3], SAMPLES["arabic"][:3], SAMPLES["chinese"][:2], "latin"],
    [chr(0x1D400), chr(0xFF21), "A", chr(0x00C5), chr(0x212B)],
    ["k" + chr(0x301), "k" + chr(0x300), "k"],
]


def rnd_string(rng):
    pool = list(SAMPLES.values())
    n = rng.randint(1, 3)
    return " ".join(rng.choice(pool) for _ in range(n))[: rng.randint(1, 80)]


def rnd_scalar(rng):
    c = rng.randint(0, 6)
    if c == 0:
        return rng.choice(FLOATS)
    if c == 1:
        return rng.randint(-2**53, 2**53)
    if c == 2:
        return rng.choice([True, False])
    if c == 3:
        return None
    if c == 4:
        return round(rng.uniform(-1e6, 1e6), rng.randint(0, 12))
    return rnd_string(rng)


def rnd_value(rng, depth=0):
    if depth >= 4:
        return rnd_scalar(rng)
    c = rng.randint(0, 9)
    if c <= 4:
        return rnd_scalar(rng)
    if c <= 7:
        return {rnd_key(rng, i): rnd_value(rng, depth + 1) for i in range(rng.randint(0, 5))}
    return [rnd_value(rng, depth + 1) for _ in range(rng.randint(0, 5))]


def rnd_key(rng, i):
    c = rng.randint(0, 5)
    if c == 0:
        return rng.choice(["timestamp", "uuid", "nonce", "created_at"])  # volatile
    if c == 1:
        return rng.choice([k for ks in KEY_SETS for k in ks])
    return f"k{i}_" + rnd_string(rng)[:12]


def main():
    rng = random.Random(SEED)
    vectors = {}

    # 1. every unicode sample as plain string and as dict value (2 x 24)
    for name, s in SAMPLES.items():
        vectors[f"str_{name}"] = s
        vectors[f"obj_{name}"] = {"text": s, "tag": name}

    # 2. float matrix: scalars, list, dict (34 + 2)
    for i, f in enumerate(FLOATS):
        vectors[f"float_{i:02d}"] = f
    vectors["float_list"] = list(FLOATS)
    vectors["float_dict"] = {f"f{i:02d}": f for i, f in enumerate(FLOATS)}

    # 3. key-ordering sets (5)
    for i, ks in enumerate(KEY_SETS):
        vectors[f"keys_{i}"] = {k: f"v{j}" for j, k in enumerate(ks)}

    # 4. structural / volatile (6)
    vectors["volatile_depths"] = {
        "timestamp": "DROP", "keep": {"uuid": "DROP", "list": [{"nonce": "DROP", "x": 1}, [{"random": "KEPT-inner", "y": 2.0}]]},
    }
    vectors["empty_containers"] = {"a": [], "b": {}, "c": [[], {}], "d": ""}
    vectors["deep_nest"] = {"l1": {"l2": {"l3": {"l4": {"l5": [1, 2.5, "x"]}}}}}
    vectors["top_list"] = [SAMPLES["emoji"], SAMPLES["latin_nfd"], {"k": 2.0}, [3.5, None, True]]
    vectors["list_sort_astral"] = {"items_keyed": [chr(0x1F680), chr(0xFFFD), chr(0xE000), "A", chr(0x10000)]}
    vectors["scalar_null"] = None

    # 5. large payload (1)
    vectors["large_payload"] = {
        "blob": (SAMPLES["chinese"] + SAMPLES["emoji"] + SAMPLES["latin_nfc"]) * 600,
        "rows": [{"id": i, "score": i / 7.0, "name": f"row-{i}"} for i in range(200)],
    }

    # 6. seeded random structures -> 1000+ total
    while len(vectors) < 1100:
        vid = f"rand_{len(vectors):04d}"
        vectors[vid] = rnd_value(rng)

    spec = {"key": ENCRYPTION_KEY, "vectors": vectors}
    with open("vectors.json", "w", encoding="ascii") as f:
        json.dump(spec, f, ensure_ascii=True, sort_keys=True)
    print(f"wrote vectors.json with {len(vectors)} vectors")


if __name__ == "__main__":
    main()
