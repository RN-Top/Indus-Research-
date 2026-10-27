"""Do sign groups on texts written abroad behave like names with a repeating element at one edge (e.g. Semitic '-El')?
Scouting, descriptive (abroad texts already seen). Each text is split into groups at man signs (G90, G91, G125); for each
group of 1+ signs, its first and last sign are 'edge' tokens. Repetition = 1 - (distinct edge signs / edge tokens).
Abroad (the 42 texts in data/abroad/abroad_inscriptions.csv, NOMATCH/'?' dropped) vs 5,000 samples of 42 home
exploration texts matched on length. Also the commonest edge signs abroad."""
import csv, sys
from collections import Counter
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from indus_workbench import data  # noqa: E402
MAN = {"G90", "G91", "G125"}
def groups(s):
    out, cur = [], []
    for x in s:
        if x in MAN:
            if cur: out.append(cur)
            cur = []
        else: cur.append(x)
    if cur: out.append(cur)
    return out
def edges(texts, which):
    e = []
    for s in texts:
        for g in groups(s):
            if which in ("first", "both"): e.append(g[0])
            if which in ("last", "both") and len(g) > 1: e.append(g[-1])
    return e
def rep(e): return 1 - len(set(e)) / len(e) if e else np.nan
ab = []
for r in csv.DictReader(open(ROOT / "data/abroad/abroad_inscriptions.csv")):
    s = [x for x in r["signs"].split() if x.startswith("G")]
    if s: ab.append(s)
raw, _ = data.load_raw("indus_website")
home = [list(s) for s in {tuple(s) for s in data.explore_only(data.build_corpus(raw, "indus_website", drop_damaged=False, metadata=data.load_metadata("indus_website"))).df.signs}]
bylen = {}
for s in home: bylen.setdefault(min(len(s), 8), []).append(s)
rng = np.random.default_rng(20261026)
out = [f"Abroad texts used: {len(ab)}; home pool: {len(home)}"]
for which in ("first", "last", "both"):
    obs = rep(edges(ab, which)); null = []
    for _ in range(5000):
        smp = [bylen[min(len(s), 8)][rng.integers(len(bylen[min(len(s), 8)]))] for s in ab]
        null.append(rep(edges(smp, which)))
    null = np.array(null); p = (1 + (null >= obs).sum()) / (1 + len(null))
    out.append(f"{which:5} edge repetition abroad {obs:.2f}  home samples mean {null.mean():.2f} (95% {np.percentile(null, 2.5):.2f}-{np.percentile(null, 97.5):.2f})  p {p:.3f}")
out.append("\nCommonest group-first signs abroad: " + str(Counter(edges(ab, "first")).most_common(8)))
out.append("Commonest group-last signs abroad:  " + str(Counter(x for s in ab for g in groups(s) if len(g) > 1 for x in [g[-1]]).most_common(8)))
print("\n".join(out)); (ROOT / "results/abroad_name_edges_output.txt").write_text("\n".join(out) + "\n")
