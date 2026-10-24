"""Do inscriptions found abroad use sign pairs never seen at home? (scouting, EXPLORATION split only)

Laursen (2010) and Parpola (1994) report that most Gulf-seal sequences are not paralleled in the Indus Valley
and suggest Indus signs were used there to write another language's names. Measured here:
  unattested-pair rate = share of a text's adjacent sign pairs that never occur in the reference home texts.
Abroad texts: exploration texts from sites outside the Indus region. Reference: all exploration texts from home sites.
Control: home texts from small home sites (under 60 texts), each scored leave-its-own-site-out (reference = all other
home sites), so a small site's local vocabulary is treated the same way as an abroad site's.
Null: abroad/control labels permuted over texts (5,000 times). Texts of 2+ signs; damaged texts kept (pairs only).
"""
import sys
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from indus_workbench import data  # noqa: E402
ABROAD = {"Ur", "Kish", "Tell Umma", "Susa", "Luristan", "Qala'at al-Bahrain", "Saar", "Karzakan", "Hajar", "Ra's al-Junayz",
          "Salut", "Altyn Depe", "Gonur Depe", "Failaka", "Nippur", "Tello", "Girsu", "Janabiyah", "Dilmun", "Kalba", "Tepe Yahya"}
RNG = np.random.default_rng(20261023)
raw, _ = data.load_raw("indus_website")
c = data.build_corpus(raw, "indus_website", drop_damaged=False, dedupe=True, metadata=data.load_metadata("indus_website")).df
ex = c[c.split == "explore"]
pairs = lambda s: list(zip(s, s[1:]))
by_site = defaultdict(list)
for s, site in zip(ex.signs, ex.site):
    by_site[site].append(list(s))
home_sites = [k for k in by_site if k not in ABROAD]
home_pairs = defaultdict(Counter)
for k in home_sites:
    for s in by_site[k]:
        home_pairs[k].update(pairs(s))
allhome = Counter()
for k in home_sites:
    allhome.update(home_pairs[k])
def rate(s, ref):
    ps = pairs(s)
    return sum(ref[p] == 0 for p in ps) / len(ps)
ab = [(k, s, rate(s, allhome)) for k in by_site if k in ABROAD for s in by_site[k] if len(s) >= 2]
ctl = []
for k in home_sites:
    if len(by_site[k]) < 60:
        ref = allhome - home_pairs[k]
        ctl += [(k, s, rate(s, ref)) for s in by_site[k] if len(s) >= 2]
a = np.array([r for *_, r in ab]); b = np.array([r for *_, r in ctl])
obs = a.mean() - b.mean(); y = np.concatenate([a, b]); lab = np.array([1] * len(a) + [0] * len(b), bool)
null = [(lambda q: y[q].mean() - y[~q].mean())(RNG.permutation(lab)) for _ in range(5000)]
p = (1 + np.sum(np.array(null) >= obs)) / 5001
print(f"Abroad exploration texts (2+ signs): {len(a)} from {len({k for k, *_ in ab})} sites; mean unattested-pair rate {a.mean():.2f}")
print(f"Control: {len(b)} texts from {len({k for k, *_ in ctl})} small home sites (leave-own-site-out); mean rate {b.mean():.2f}")
print(f"Difference {obs:+.2f}; one-sided p {p:.4f}")
print("Abroad texts:"); [print(f"   {k:20} {' '.join(s):40} {r:.2f}") for k, s, r in ab]
