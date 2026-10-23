"""Robustness: the fish lead in Mahadevan's independent transcription (IM77). Not a confirmatory test.

IM77 covers largely the same objects as ICIT (exploration and holdout alike), so this checks that the result does not
depend on ICIT's reading conventions; it is not new evidence. Signs reached through paragorth's unvalidated
ICIT->Mahadevan bridge: G220 -> M59, G231 -> M70, G233 -> M72 (G244 unmapped). Numerals = Mahadevan numbers bridged
from the frozen numeral list; G2 (M99/M100) right after a bridged opener is not counted. Lines split at 0 (lost sign).

    python3 scripts/fish_numeral_im77.py <im77_corpus_lines.csv> <bridge_extended.json>
"""
import csv, json, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "scripts"))
from number_system import VAL  # noqa: E402
bridge = json.load(open(sys.argv[2]))
m = lambda g: {int(x) for x in bridge.get(g[1:], [])}
NUM = set().union(*(m(g) for g in VAL)); G2 = m("G2")
OPEN = set().union(*(m(g) for g in ["G416", "G503", "G692", "G817", "G820", "G861", "G920"]))
PLAIN, MARKED = m("G220"), m("G231") | m("G233") | m("G244")
toks = []
for r in csv.DictReader(open(sys.argv[1])):
    if r["line"] == "9":
        continue
    s = [int(t) for t in r["signs_clean"].split()]
    for k, x in enumerate(s):
        if x in PLAIN | MARKED:
            prev = k > 0 and s[k - 1] in NUM and not (s[k - 1] in G2 and k > 1 and s[k - 2] in OPEN)
            toks.append((x in PLAIN, prev))
lab = np.array([a for a, _ in toks]); y = np.array([b for _, b in toks], float)
obs = y[lab].mean() - y[~lab].mean(); r = np.random.default_rng(20261023)
null = np.array([y[q].mean() - y[~q].mean() for q in (r.permutation(lab) for _ in range(5000))])
print(f"Bridged: plain {sorted(PLAIN)}, marked {sorted(MARKED)}; numerals {len(NUM)} signs")
print(f"Plain fish preceded by a numeral: {int(y[lab].sum())}/{int(lab.sum())} = {y[lab].mean():.1%}")
print(f"Inside-marked fish: {int(y[~lab].sum())}/{int((~lab).sum())} = {y[~lab].mean():.1%}")
print(f"Difference {obs:+.3f}; one-sided p = {(1 + np.sum(null >= obs)) / (len(null) + 1):.4f}")
