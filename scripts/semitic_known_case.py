"""P22: known-case check, Aramaic and Hebrew (IIP) against Tamil (DHARMA)."""
import csv, glob, random, re, sys, xml.etree.ElementTree as ET
from datetime import date
sys.path.insert(0, "scripts")
from structure_battery import features, distance  # noqa

IIP = "/tmp/claude-0/-home-claude/5444b495-3534-509a-b0d3-d3a720a00472/scratchpad/iip/epidoc-files"
OUT = "results/known_case_semitic_P22_2026-11-07.md"
SEED, N = 20261107, 1000
PUNCT = re.compile(r"[=\|\.,;:!?()\[\]\-–—\"'“”‘’<>{}]+")
TEI = "{http://www.tei-c.org/ns/1.0}"

def iip_words(path):
    root = ET.parse(path).getroot()
    words = []
    for div in root.iter(TEI + "div"):
        if div.get("type") == "edition":
            text = PUNCT.sub(" ", " ".join(div.itertext()))
            words += [w for w in text.split() if w.strip()]
    return words

def chunk(words):
    out, i = [], 0
    while i < len(words):
        L = min(8, len(words) - i)
        if L >= 3:
            out.append(words[i:i+L])
        i += L
    return out

def load_lang(tag):
    texts = []
    for p in sorted(glob.glob(f"{IIP}/*.xml")):
        try:
            s = open(p, encoding="utf-8").read(3000)
        except OSError:
            continue
        if f'xml:lang="{tag}"' not in open(p, encoding="utf-8").read():
            continue
        try:
            texts += chunk(iip_words(p))
        except ET.ParseError:
            continue
    return texts

def tamil():
    rows = list(csv.DictReader(open("data/structure/tamil_dharma.csv", encoding="utf-8")))
    return [r["units"].split() for r in rows]

def sample(texts, n, rng):
    return rng.sample(texts, min(n, len(texts)))

def main():
    rng = random.Random(SEED)
    arc = load_lang("arc")
    he = load_lang("he")
    tam = tamil()
    # write corpora for the record
    for name, ts in [("aramaic_iip", arc), ("hebrew_iip", he)]:
        with open(f"data/structure/{name}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["text_id", "units"])
            for i, t in enumerate(ts):
                w.writerow([f"{name}{i}", " ".join(t)])
    m = min(len(arc), len(he), len(tam))
    A = sample(arc, m, rng); H = sample(he, m, rng); T = sample(tam, m, rng)
    fA, fH, fT = features(A), features(H), features(T)
    d_ah, d_at, d_tt_half = distance(fA, fH), distance(fA, fT), None
    # null (as registered in P22): length-matched draws from Aramaic's word inventory,
    # compared against each partner corpus; observed distance must beat the 5th percentile.
    inv_a = [u for t in arc for u in t]
    null_ah, null_at = [], []
    for _ in range(N):
        syn = [[rng.choice(inv_a) for _ in t] for t in sample(arc, m, rng)]
        fs = features(syn)
        null_ah.append(distance(fs, fH))
        null_at.append(distance(fs, fT))
    q5 = lambda xs: sorted(xs)[int(0.05*len(xs))]
    med = lambda xs: sorted(xs)[len(xs)//2]
    tam_halves = []
    for _ in range(N):
        idx = list(range(len(tam))); rng.shuffle(idx)
        h = len(idx)//2
        tam_halves.append(distance(features([tam[i] for i in idx[:h]]), features([tam[i] for i in idx[h:]])))
    pred_1 = d_ah < d_at
    lines = [f"# P22 known-case check, Semitic, {date.today().isoformat()}", "",
             f"Texts per corpus after matching: {m} (Aramaic {len(arc)}, Hebrew {len(he)}, Tamil {len(tam)} before matching).",
             "",
             "| pair | distance | null median | null 5th pct |",
             "|---|---|---|---|",
             f"| Aramaic-Hebrew | {d_ah:.4f} | {med(null_ah):.4f} | {q5(null_ah):.4f} |",
             f"| Aramaic-Tamil | {d_at:.4f} | {med(null_at):.4f} | {q5(null_at):.4f} |",
             "",
             f"Tamil halves (null for Tamil self-consistency): median {med(tam_halves):.4f}, max {max(tam_halves):.4f}.",
             "",
             f"**Part 1 (Aramaic-Hebrew distance below Aramaic-Tamil distance): {'PASS' if pred_1 else 'FAIL'}.**",
             f"**Part 1b (observed Aramaic-Hebrew below 5th percentile of its null): {'PASS' if d_ah < q5(null_ah) else 'FAIL'}.**",
             f"**Part 2 (Tamil halves closer to each other than Aramaic is to Tamil): {'PASS' if med(tam_halves) < d_at else 'FAIL'}.**",
             "",
             "Confounds: IIP texts are mostly funerary and dedicatory; DHARMA texts are grants. Genre can drive these features, so a pass does not show family.",
             "Licences: IIP files tagged CC BY-NC 4.0 (accepted by Erin 7 Nov 2026 for research reuse); DHARMA CC BY 4.0 / CC BY-SA 4.0."]
    open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines))

if __name__ == "__main__":
    main()
