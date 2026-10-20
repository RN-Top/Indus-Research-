"""S1/S2 of drafts/S1_S2_PREDICTIONS.md: are closers suffix-like (diverse predecessors) and openers
prefix-like (diverse successors), against frequency-matched non-role signs? EXPLORATION split only.

Implementation note (fixed before looking at results): entropy depends on sample size, so the target and
every matched control sign are each subsampled to the same m = floor(0.7 * n_target) neighbour tokens,
200 times, and the mean entropy is used. The control distribution is over the matched signs.
"""
import json, sys
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from functional_slots import load, NUMERALS  # noqa: E402

H = json.load(open(ROOT / "hypotheses/H-2026-10-16-51b7445b.json"))["params"]
OPEN, CLOSE = H["openers"], H["closers"]
RNG = np.random.default_rng(20261019)


def ent(tokens):
    c = np.array(list(Counter(tokens).values()), float); p = c / c.sum()
    return float(-(p * np.log2(p)).sum())


def sub_ent(neigh, m, reps=200):
    a = np.array(neigh, dtype=object)
    return float(np.mean([ent(RNG.choice(a, m, replace=False)) for _ in range(reps)]))


def main():
    seqs = [list(s) for s in load()["signs"]]
    pred, succ = defaultdict(list), defaultdict(list)
    for s in seqs:
        for i, x in enumerate(s):
            if i > 0: pred[x].append(s[i - 1])
            if i < len(s) - 1: succ[x].append(s[i + 1])
    tok = Counter(x for s in seqs for x in s)
    roles = set(OPEN) | set(CLOSE) | set(NUMERALS)
    out = {}
    for label, targets, neigh in [("S1 closers: predecessor diversity", CLOSE, pred),
                                  ("S2 openers: successor diversity", OPEN, succ)]:
        print(f"\n== {label}")
        res = []
        for t in targets:
            n = len(neigh[t])
            ctrl = [x for x in tok if x not in roles and 0.7 * tok[t] <= tok[x] <= 1.3 * tok[t] and len(neigh[x]) >= 0.7 * n]
            if n < 10 or len(ctrl) < 5:
                print(f"   {t:6} n={n:4}  too few tokens or controls ({len(ctrl)})"); res.append((t, "n/a")); continue
            m = int(0.7 * n)
            te = sub_ent(neigh[t], m)
            ce = np.array([sub_ent(neigh[x], m, 50) for x in ctrl])
            lo, hi = np.percentile(ce, 5), np.percentile(ce, 95)
            verdict = "ABOVE 95th" if te > hi else ("BELOW 5th" if te < lo else "within")
            top = Counter(neigh[t]).most_common(3)
            print(f"   {t:6} n={n:4} H={te:.2f} bits  control mean {ce.mean():.2f} [{lo:.2f}, {hi:.2f}] ({len(ctrl)} signs)  {verdict}  top {top}")
            res.append((t, verdict, te, float(ce.mean()), float(lo), float(hi), n))
        k_above = sum(r[1] == "ABOVE 95th" for r in res); k_below = sum(r[1] == "BELOW 5th" for r in res)
        print(f"   above: {k_above}  below: {k_below}  within: {sum(r[1]=='within' for r in res)}  n/a: {sum(r[1]=='n/a' for r in res)}")
        out[label] = res
    (ROOT / "results" / "affix_profile.json").write_text(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
