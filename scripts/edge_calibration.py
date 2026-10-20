"""Calibrated edge test (drafts/edge_calibration_PREDICTIONS.md). EXPLORATION only.

W1 (word level): Simpson(word-final sign) / Simpson(word-initial sign), words of 2+ signs.
T1 (text level): Simpson(text-final sign) / Simpson(text-initial sign), texts of 3+ signs.
Then: does T1 track W1 across known languages (Spearman >= 0.6)? Only then is Indus T1 interpreted.

    python scripts/edge_calibration.py <cdli_data_folder>
"""
import hashlib, json, re, sys, unicodedata
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import mesopotamian_seals as ms  # noqa: E402

RNG = np.random.default_rng(20261020)


def simpson(items):
    c = np.array(list(Counter(items).values()), float); n = c.sum()
    return float((c * (c - 1)).sum() / (n * (n - 1))) if n > 1 else float("nan")


def cune_signs(word):
    return [s for s in re.split(r"[-.{}+]", word) if s]


def syll(word):
    w = unicodedata.normalize("NFKD", word); w = "".join(c for c in w if not unicodedata.combining(c)).lower()
    w = re.sub(r"[^a-z]", "", w)
    return re.findall(r"[^aeiou]*[aeiou]+|[^aeiou]+$", w)


def measures(texts):
    """texts: list of texts; each text = list of words; each word = list of signs."""
    words = [w for t in texts for w in t if len(w) >= 2]
    W1 = simpson([w[-1] for w in words]) / simpson([w[0] for w in words]) if words else float("nan")
    flat = [[s for w in t for s in w] for t in texts]
    flat = [f for f in flat if len(f) >= 3]
    T1 = simpson([f[-1] for f in flat]) / simpson([f[0] for f in flat])
    boot = []
    for _ in range(1000):
        idx = RNG.integers(0, len(flat), len(flat))
        b = [flat[i] for i in idx]
        boot.append(simpson([f[-1] for f in b]) / simpson([f[0] for f in b]))
    return dict(words=len(words), texts=len(flat), W1=W1, T1=T1, T1_lo=float(np.percentile(boot, 2.5)),
                T1_hi=float(np.percentile(boot, 97.5)))


def cuneiform(folder):
    folder = Path(folder)
    cat = pd.read_csv(folder / "cdli_cat.csv", usecols=["id_text", "period", "object_type", "language", "genre"],
                      dtype=str, low_memory=False).fillna("")
    cat["P"] = "P" + cat["id_text"].str.zfill(6)
    info = cat.set_index("P").to_dict("index")
    groups = {k: {} for k in ["Sumerian seals", "Akkadian seals", "Sumerian royal", "Akkadian royal", "Elamite royal"]}
    for p, kind, lines in ms.parse(folder / "cdliatf_unblocked.atf"):
        m = info.get(p)
        if not m:
            continue
        lang, genre, per, obj = m["language"], m["genre"], m["period"], m["object_type"]
        text = [cune_signs(w) for ln in lines for w in ln if w != "NUM"]
        text = [w for w in text if w]
        if len(text) < 2:
            continue
        key = None
        is_seal = kind == "impression" or (kind == "object" and "seal" in obj)
        if is_seal and per.startswith(ms.PERIODS):
            key = {"Sumerian": "Sumerian seals", "Akkadian": "Akkadian seals"}.get(lang)
        elif kind == "object" and genre.startswith("Royal"):
            if lang == "Sumerian": key = "Sumerian royal"
            elif lang == "Akkadian": key = "Akkadian royal"
            elif lang == "Elamite" and "Elamite" in per: key = "Elamite royal"
        if key:
            sig = " ".join("-".join(w) for w in text)
            if int(hashlib.sha256(f"{ms.SALT}:{sig}".encode()).hexdigest(), 16) % 100 >= 20:  # exploration only
                groups[key].setdefault(sig, text)
    return {k: list(v.values()) for k, v in groups.items()}


def jsonl_words(fn, field):
    out = []
    for line in open(fn):
        d = json.loads(line)
        ws = [syll(w["form"]) for w in d.get("words", [])] if field == "words" else [syll(x) for x in d[field].split()]
        ws = [w for w in ws if w]
        if ws:
            out.append(ws)
    return out


def main(cdli):
    C = cuneiform(cdli)
    C["Old Tamil"] = jsonl_words(ROOT / "data/tamil_brahmi/corpus_roles.jsonl", "words")
    C["Prakrit"] = jsonl_words(ROOT / "data/prakrit_eiad/tagged_roles.jsonl", "words")
    from functional_slots import load
    C["Indus"] = [[[x] for x in s] for s in load()["signs"]]
    res = {}
    for k, T in C.items():
        r = measures(T); res[k] = r
        w1 = "  n/a " if k == "Indus" else f"{r['W1']:6.2f}"
        print(f"{k:16} texts {r['texts']:5} words {r['words']:6}  W1 {w1}  T1 {r['T1']:6.2f} [{r['T1_lo']:.2f}, {r['T1_hi']:.2f}]")
    langs = [k for k in res if k != "Indus"]
    from scipy.stats import spearmanr
    rho, p = spearmanr([res[k]["W1"] for k in langs], [res[k]["T1"] for k in langs])
    print(f"\nCalibration: Spearman(W1, T1) across {len(langs)} language corpora = {rho:.2f} (p = {p:.2f}); pass needs >= 0.6")
    res["_calibration"] = dict(rho=float(rho), p=float(p), passed=bool(rho >= 0.6))
    (ROOT / "results" / "edge_calibration.json").write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
