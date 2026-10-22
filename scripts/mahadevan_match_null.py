"""Is Mahadevan's Phu Khao Thong match rarer than chance? (no holdout used; IM77 = Mahadevan 1977 numbering)

Claim (agent_survivals_2026-10-22.md, 1c): a sherd from Phu Khao Thong, Thailand, has two non-Brahmi signs,
an "N"-like sign (~ M47/M48) followed by a diamond (~ M261/M373); the same pair occurs in Harappa texts 4589 and 5265.

1. Check the claim in IM77: which lines contain M47/M48 directly followed by M261/M373?
2. How often would a 2-sign graffito match SOME adjacent Indus pair by chance, allowing (as the claim does)
   two candidate Indus signs for each graffito sign? Graffito signs drawn at random from the Indus inventory,
   (a) weighted by token frequency, (b) uniformly over sign types. 100,000 draws each.
3. Same, requiring the match in a fixed order and in either order.

Usage: python3 scripts/mahadevan_match_null.py <im77_corpus_lines.csv>
Source (not copied here): github.com/paragorth/Indus- data/im77.
"""
import csv, sys
from collections import Counter
import numpy as np

RNG = np.random.default_rng(20261022)
rows = list(csv.DictReader(open(sys.argv[1])))
lines = []
for r in rows:
    if r["line"] == "9":
        continue
    seg = []
    for t in r["signs_clean"].split():
        if t == "0":  # break: lost or illegible
            if seg: lines.append((r["text_no"], seg)); seg = []
        else:
            seg.append(int(t))
    if seg:
        lines.append((r["text_no"], seg))
pairs = set(); pair_texts = {}
for tn, s in lines:
    for a, b in zip(s, s[1:]):
        pairs.add((a, b)); pair_texts.setdefault((a, b), set()).add(tn)
tok = Counter(x for _, s in lines for x in s)
signs = np.array(sorted(tok)); w = np.array([tok[s] for s in signs], float); w /= w.sum()
print(f"IM77 lines (split at breaks): {len(lines)}; sign types: {len(signs)}; distinct adjacent pairs attested: {len(pairs)}")
print(f"Share of all possible ordered pairs that are attested: {len(pairs) / len(signs) ** 2:.2%}")

print("\n1. The claimed pair (N-like M47/M48, then diamond M261/M373):")
for a in (47, 48):
    for b in (261, 373):
        for x, y in ((a, b), (b, a)):
            t = sorted(pair_texts.get((x, y), []))
            print(f"   M{x} -> M{y}: {len(t)} text(s) {t[:12]}")
for tn in ("4589", "5265"):
    for t, s in lines:
        if t == tn:
            print(f"   text {tn}: {' '.join('M%d' % x for x in s)}")
print(f"   token counts: M47 {tok[47]}, M48 {tok[48]}, M261 {tok[261]}, M373 {tok[373]}")


def chance(weighted, both_orders, n=100_000):
    p = w if weighted else None
    c1 = RNG.choice(signs, size=(n, 2), p=p); c2 = RNG.choice(signs, size=(n, 2), p=p)
    hit = 0
    for (a1, a2), (b1, b2) in zip(c1, c2):
        ok = any((x, y) in pairs for x in (a1, a2) for y in (b1, b2))
        if both_orders and not ok:
            ok = any((y, x) in pairs for x in (a1, a2) for y in (b1, b2))
        hit += ok
    return hit / n


print("\n2-3. Chance that a random 2-sign graffito matches some attested Indus pair (2 candidate signs each):")
for weighted in (True, False):
    for both in (False, True):
        print(f"   {'frequency-weighted' if weighted else 'uniform over types':20} {'either order' if both else 'fixed order ':12}"
              f" {chance(weighted, both):.1%}")


# 4. Frequency-matched: replace each of the four candidate signs by a random sign of similar frequency (within ±50%).
def similar(s):
    f = tok[s]; c = [x for x in signs if x != s and 0.5 * f <= tok[x] <= 1.5 * f]
    return c
pools = {s: similar(s) for s in (47, 48, 261, 373)}
hits = {False: 0, True: 0}; N = 20_000
for _ in range(N):
    a = [RNG.choice(pools[47]), RNG.choice(pools[48])]; b = [RNG.choice(pools[261]), RNG.choice(pools[373])]
    fixed = any((x, y) in pairs for x in a for y in b)
    hits[False] += fixed; hits[True] += fixed or any((y, x) in pairs for x in a for y in b)
print("\n4. Frequency-matched stand-ins for the four candidate signs (pools: "
      + ", ".join(f"M{s} {len(p)}" for s, p in pools.items()) + "):")
print(f"   match by chance, fixed order {hits[False] / N:.1%}; either order {hits[True] / N:.1%}")
