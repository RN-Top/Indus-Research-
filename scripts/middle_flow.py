"""Does the middle of an inscription have an internal order? (EXPLORATION ONLY: description, no tests.)

Middle = what is left after removing the heading (opening sign(s), plus G2 or G60 right
after them) and the closing sign(s) at the end. Two samples:
  strict: texts with both a heading and a closer;
  loose:  texts with a closer (heading removed if present).
For common middle signs: mean relative position (0 = just after the heading, 1 = just
before the closer), spread, and directional pairs (A before B against B before A).
Exploration split only; nothing tested or registered.

    python scripts/middle_flow.py
"""

import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from functional_skeleton import assign  # noqa: E402
from functional_slots import NUMERALS, load  # noqa: E402

MIN = 15


def middle(s, roles):
    i = 0
    while i < len(s) and roles.get(s[i]) == 0:
        i += 1
    head = i > 0
    if head and i < len(s) and s[i] in ("G2", "G60"):
        i += 1
    j = len(s)
    while j > i and roles.get(s[j - 1]) == 2:
        j -= 1
    return head, j < len(s), s[i:j]


def describe(mids, label, out):
    mids = [m for m in mids if m]
    L = [len(m) for m in mids]
    print(f"\n== {label}: {len(mids)} texts with a non-empty middle; middle length "
          f"{dict(sorted(Counter(min(x, 6) for x in L).items()))} (6 = 6 or more) ==")
    pos, cnt = defaultdict(list), Counter()
    for m in mids:
        if len(m) < 2:
            continue
        for k, x in enumerate(m):
            pos[x].append(k / (len(m) - 1))
            cnt[x] += 1
    rows = [dict(sign=x, n=cnt[x], numeral=x in NUMERALS, mean=float(np.mean(v)), sd=float(np.std(v)),
                 first=float(np.mean([p == 0 for p in v])), last=float(np.mean([p == 1 for p in v])))
            for x, v in pos.items() if cnt[x] >= MIN]
    rows.sort(key=lambda r: r["mean"])
    print(f"   {len(rows)} signs used >= {MIN} times in middles of 2+ signs (a uniform spread would give mean 0.5, sd about 0.4)")
    print("   EARLY:", ", ".join(f"{r['sign']}{'#' if r['numeral'] else ''} {r['mean']:.2f}±{r['sd']:.2f} (n {r['n']}, first {r['first']:.0%})" for r in rows[:10]))
    print("   LATE: ", ", ".join(f"{r['sign']}{'#' if r['numeral'] else ''} {r['mean']:.2f}±{r['sd']:.2f} (n {r['n']}, last {r['last']:.0%})" for r in rows[::-1][:10]))
    # directional pairs among common signs
    common = {r["sign"] for r in rows}
    ab = Counter()
    for m in mids:
        first_at = {}
        for k, x in enumerate(m):
            first_at.setdefault(x, k)
        for a, b in combinations([x for x in first_at if x in common], 2):
            if first_at[a] < first_at[b]:
                ab[(a, b)] += 1
            elif first_at[b] < first_at[a]:
                ab[(b, a)] += 1
    pairs = []
    seen = set()
    for (a, b), n in ab.items():
        if (b, a) in seen or (a, b) in seen:
            continue
        seen.add((a, b))
        r = ab.get((b, a), 0)
        tot = n + r
        if tot >= 10:
            hi, lo, x, y = (n, r, a, b) if n >= r else (r, n, b, a)
            pairs.append(dict(before=x, after=y, forward=hi, backward=lo, total=tot, share=hi / tot))
    pairs.sort(key=lambda p: (-p["share"], -p["total"]))
    strong = [p for p in pairs if p["share"] >= 0.9]
    print(f"   pairs co-occurring in >= 10 middles: {len(pairs)}; with one order >= 90% of the time: {len(strong)} "
          f"({len(strong) / len(pairs):.0%}); >= 75%: {sum(p['share'] >= 0.75 for p in pairs)}")
    print("   strongest:", "; ".join(f"{p['before']}→{p['after']} {p['forward']}:{p['backward']}" for p in pairs[:15]))
    out[label] = dict(texts=len(mids), length=dict(Counter(L)), signs=rows, pairs=pairs[:60],
                      n_pairs=len(pairs), n_90=len(strong), n_75=sum(p['share'] >= 0.75 for p in pairs))


def main():
    df = load()
    roles, _ = assign(list(df["signs"]))
    parts = [middle(s, roles) for s in df["signs"]]
    out = {}
    describe([m for h, c, m in parts if h and c], "strict (heading and closer)", out)
    describe([m for h, c, m in parts if c], "loose (closer; heading removed if present)", out)
    (ROOT / "results" / "middle_flow.json").write_text(json.dumps(out, indent=1, default=float))


if __name__ == "__main__":
    main()
