"""Does the same mark do the same thing on different signs? (scouting, EXPLORATION split only)

For each variant/base pair in the blind mark annotation (data/sign_marks/marks_blind_2026-10-20.csv) whose
variant carries exactly one mark type, the "shift" is how adding the mark changes the sign's company:
  shift = (neighbour distribution of variant) - (neighbour distribution of base),
over left and right neighbours (each as its own feature: L:<sign>, R:<sign>, plus L:# / R:# for text edges).
If a mark is a reusable modifier (like a grammatical ending), pairs sharing a mark should shift in the same
direction even on unrelated base signs: their shift vectors should be more alike (cosine) than shifts of pairs
with different marks.

Statistic: mean cosine between shifts of pairs with the SAME mark type but DIFFERENT base families, minus the
mean cosine between pairs with DIFFERENT mark types (also different families).
Null: mark-type labels permuted over pairs (5,000 times). Both signs need 6+ uses. Not a confirmatory test.

    python scripts/mark_consistency_scouting.py
"""
import csv, json, sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from functional_slots import load  # noqa: E402
from functional_skeleton import assign  # noqa: E402
from number_system import VAL  # noqa: E402

COARSE = "--coarse" in sys.argv  # neighbours as classes (opener, closer, numeral, other) + position bin

MIN_USES = 6
RNG = np.random.default_rng(20261022)


def mtype(m):
    for p in ("top_strokes", "side_strokes"):
        if m.startswith(p):
            return p
    return m


ann = {r["sign"]: r for r in csv.DictReader(open(ROOT / "data/sign_marks/marks_blind_2026-10-20.csv"))}
parent = {s: (s if r["base"] in ("self", "") else r["base"]) for s, r in ann.items()}


def fam(g):
    seen = set()
    while g in parent and parent[g] != g and g not in seen:
        seen.add(g); g = parent[g]
    return g


def main():
    df = load()
    roles, _ = assign(list(df.signs))
    def cl(y):
        if not COARSE:
            return y
        return "numeral" if y in VAL else {0: "opener", 2: "closer"}.get(roles.get(y), "other")
    nb = defaultdict(Counter); uses = Counter()
    for s in df.signs:
        for k, x in enumerate(s):
            uses[x] += 1
            nb[x]["L:" + (cl(s[k - 1]) if k else "#")] += 1
            nb[x]["R:" + (cl(s[k + 1]) if k + 1 < len(s) else "#")] += 1
            if COARSE and len(s) > 1:
                nb[x]["pos:" + str(min(int(3 * k / (len(s) - 1)), 2))] += 1
    pairs = []
    for v, r in ann.items():
        b = r["base"]
        if b in ("self", "") or b == v:
            continue
        ms = {mtype(m) for m in r["marks"].split(";") if m}
        ms.discard("other")
        if len(ms) != 1 or "doubled" in ms or "ligature" in ms:
            continue
        if uses[v] >= MIN_USES and uses[b] >= MIN_USES:
            pairs.append((v, b, ms.pop()))
    feats = sorted({f for v, b, _ in pairs for f in list(nb[v]) + list(nb[b])})
    ix = {f: i for i, f in enumerate(feats)}

    def dist(x):
        a = np.zeros(len(feats))
        for f, n in nb[x].items():
            a[ix[f]] = n
        return a / a.sum()

    shifts = []
    for v, b, m in pairs:
        d = dist(v) - dist(b)
        shifts.append(d / (np.linalg.norm(d) or 1))
    S = np.array(shifts); C = S @ S.T
    fams = [fam(b) for _, b, _ in pairs]
    labels = np.array([m for _, _, m in pairs])
    cross = [(i, j) for i, j in combinations(range(len(pairs)), 2) if fams[i] != fams[j]]
    I = np.array([i for i, _ in cross]); J = np.array([j for _, j in cross]); cij = C[I, J]

    def stat(lab):
        same = lab[I] == lab[J]
        if not same.any() or same.all():
            return float("nan")
        return cij[same].mean() - cij[~same].mean()

    obs = stat(labels)
    null = np.array([stat(RNG.permutation(labels)) for _ in range(5000)])
    p = (1 + np.sum(null >= obs)) / (len(null) + 1)
    print(f"Pairs with one mark type, both signs {MIN_USES}+ uses: {len(pairs)}; mark types: {dict(Counter(labels))}")
    print(f"Cross-family pair-of-pairs: {len(cross)}; same-mark among them: {int((labels[I] == labels[J]).sum())}")
    print(f"\nSame-mark minus different-mark cosine (different families only): {obs:+.3f}  "
          f"(null {null.mean():+.3f}; one-sided p = {p:.4f})")

    per = {}
    print("\nBy mark type (mean cosine between shifts of same-mark pairs on different families; "
          "null: random pairs of pairs on different families):")
    allc = cij
    for m in sorted(set(labels)):
        sel = (labels[I] == m) & (labels[J] == m)
        if sel.sum() == 0:
            continue
        o = cij[sel].mean()
        nn = np.array([allc[RNG.choice(len(allc), size=int(sel.sum()), replace=False)].mean() for _ in range(5000)])
        pm = (1 + np.sum(nn >= o)) / (len(nn) + 1)
        members = [f"{v}/{b}" for v, b, mm in pairs if mm == m]
        per[m] = dict(pairs=members, cross_family_comparisons=int(sel.sum()), mean_cos=float(o), p=float(pm))
        print(f"   {m:18} {len(members):2} pairs, {int(sel.sum()):3} comparisons: cos {o:+.3f}  (p {pm:.3f})  {' '.join(members)}")

    # what the shift looks like for each mark type: features most increased, averaged over its pairs
    print("\nTop features gained when the mark is added (mean over that mark's pairs):")
    for m in per:
        idx = [k for k, (_, _, mm) in enumerate(pairs) if mm == m]
        mean = S[idx].mean(0)
        top = np.argsort(-mean)[:5]
        print(f"   {m:18} " + ", ".join(f"{feats[t]} {mean[t]:+.2f}" for t in top))
    json.dump(dict(pairs=pairs, observed=float(obs), null_mean=float(null.mean()), p=float(p), by_mark=per),
              open(ROOT / ("results/mark_consistency_scouting" + ("_coarse" if COARSE else "") + ".json"), "w"), indent=1)


if __name__ == "__main__":
    main()
