"""P21: known-case check for the structural method, on DHARMA Tamil edited XML."""
import csv, glob, random, re, sys, xml.etree.ElementTree as ET
from datetime import date
sys.path.insert(0, "scripts")
from structure_battery import features, distance, load_corpus  # noqa

SRC = "/tmp/claude-0/-home-claude/5444b495-3534-509a-b0d3-d3a720a00472/scratchpad/tfa"
CSV_OUT = "data/structure/tamil_dharma.csv"
OUT = "results/known_case_tamil_P21_2026-11-07.md"
NS = {"t": "http://www.tei-c.org/ns/1.0"}
SEED = 20261107
N = 1000
PUNCT = re.compile(r"[=௳।॥|॥\.,;:!?()\[\]\-–—\"'“”‘’]+")

def edition_words(path):
    root = ET.parse(path).getroot()
    words = []
    for div in root.iter():
        if div.tag.endswith("div") and div.get("type") == "edition":
            text = " ".join(div.itertext())
            text = PUNCT.sub(" ", text)
            words += [w for w in text.split() if w.strip()]
    return words

def chunk(words, rng=None):
    # split each edition into texts of 3-8 words (consecutive runs)
    out = []
    i = 0
    while i < len(words):
        L = min(8, len(words) - i)
        if L >= 3:
            out.append(words[i:i+L])
        i += L
    return out

def main():
    texts = []
    for p in sorted(glob.glob(f"{SRC}/*.xml")):
        try:
            ws = edition_words(p)
        except ET.ParseError:
            continue
        texts += chunk(ws)
    with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["text_id", "units"])
        for i, t in enumerate(texts):
            w.writerow([f"tam{i}", " ".join(t)])
    corpus = [t for t in texts if 3 <= len(t) <= 8]
    rng = random.Random(SEED)
    inventory = [u for t in corpus for u in t]
    lengths = [len(t) for t in corpus]

    obs_same = []
    for _ in range(N):
        idx = list(range(len(corpus))); rng.shuffle(idx)
        h = len(idx)//2
        a = [corpus[i] for i in idx[:h]]; b = [corpus[i] for i in idx[h:]]
        obs_same.append(distance(features(a), features(b)))

    diff = []
    for _ in range(N):
        syn = []
        for L in lengths[:len(lengths)]:
            syn.append([rng.choice(inventory) for _ in range(L)])
        rng.shuffle(syn)
        diff.append(distance(features(corpus), features(syn)))

    f_tam = features(corpus)
    med = lambda xs: sorted(xs)[len(xs)//2]
    same_med, same_max = med(obs_same), max(obs_same)
    diff_med = med(diff)
    passed = same_med < diff_med and max(obs_same) < min(diff)
    lines = [f"# P21 known-case check, Tamil (DHARMA), {date.today().isoformat()}", "",
             f"Texts (3-8 words): {len(corpus)}. Tamil profile: " + " | ".join(f"{x:.3f}" for x in f_tam),
             "",
             f"Known-same (random halves of Tamil, {N} draws): median distance {same_med:.4f}, max {same_max:.4f}.",
             f"Known-different (Tamil vs synthetic word-random corpus, {len(diff)} draws): median distance {diff_med:.4f}, min {min(diff):.4f}.",
             "",
             f"**Result: {'PASS' if passed else 'FAIL'}.** "
             + ("The method separates known-same from known-different. It can be used to test Indus against a comparison corpus."
                if passed else "The method does not separate known-same from known-different. Do not test Indus until this is fixed."),
             "",
             "Limit: this checks only the method. It does not test Semitic against non-Semitic, because no Aramaic or Hebrew text is licensed and readable yet.",
             "Licence: DHARMA tfa-sii-epigraphy README: CC BY 4.0. Individual pages: CC BY-SA 4.0. Both allow research reuse with attribution."]
    open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines))

if __name__ == "__main__":
    main()
