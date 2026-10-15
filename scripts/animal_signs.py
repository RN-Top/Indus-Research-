"""Does any sign track the seal animal once unicorns are set aside? (EXPLORATORY.)

Exploration split only, seals with a recorded animal other than the unicorn
(motif_group not in unicorn / none / unknown). The earlier closer test
(results/closer_category_test.md) was swamped by unicorns (79% of animal seals).

  1. Per sign (present on >= MIN_SUPPORT non-unicorn seals): is presence tied to
     the animal? Chi-square of presence x animal, against 5,000 shuffles of the
     animal labels. Cramer's V and excess V as effect sizes. The role slots are
     tested the same way (has an opener / a closer / a numeral; which closer
     ends the text; which opener starts it).
  2. Per animal (>= 10 seals) x sign: is the sign over-represented on that
     animal's seals against the other non-unicorn seals? One-sided Fisher exact
     test, lift.
  3. Candidates: rate on unicorn seals, and a shuffle kept inside each site
     (most animals come from Mohenjo-daro, so a site effect could pose as an
     animal effect).
Benjamini-Hochberg within (1) and within (2). Nothing reads the holdout.

    python scripts/animal_signs.py
"""

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.stats import fisher_exact

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from functional_skeleton import RULE, assign  # noqa: E402
from functional_slots import NUMERALS, load  # noqa: E402

MIN_SUPPORT = 8      # sign present on at least this many non-unicorn seals
MIN_ANIMAL = 8       # animals with fewer seals are merged into "other animal"
MIN_ANIMAL_TEST = 10  # animals tested one by one in part 2
N_PERM = 5000
RNG = np.random.default_rng(20261015)
NAMES = {"Gaur": "gaur (wild ox)", "Zebu": "zebu (humped bull)", "Elep": "elephant", "Rhin": "rhinoceros",
         "Tigr": "tiger", "Goat": "goat / markhor", "Buff": "water buffalo"}


def bh(p):
    p = np.asarray(p, float)
    if not len(p):
        return p
    o = np.argsort(p)
    q = p[o] * len(p) / np.arange(1, len(p) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty_like(q)
    out[o] = np.minimum(q, 1)
    return out


def chi2(x, y):
    """Chi-square of the contingency table of two integer-coded arrays."""
    t = np.zeros((x.max() + 1, y.max() + 1))
    np.add.at(t, (x, y), 1)
    e = t.sum(1, keepdims=True) * t.sum(0, keepdims=True) / t.sum()
    with np.errstate(divide="ignore", invalid="ignore"):
        return float(np.nansum((t - e) ** 2 / e)), t


def perm_assoc(x, y, strata=None):
    stat, t = chi2(x, y)
    null = np.empty(N_PERM)
    groups = [np.flatnonzero(strata == s) for s in np.unique(strata)] if strata is not None else None
    for i in range(N_PERM):
        if groups is None:
            yy = RNG.permutation(y)
        else:
            yy = y.copy()
            for g in groups:
                yy[g] = RNG.permutation(y[g])
        null[i] = chi2(x, yy)[0]
    n, k = len(x), min(t.shape) - 1
    return dict(chi2=stat, null_mean=float(null.mean()), p=float((1 + (null >= stat).sum()) / (N_PERM + 1)),
                cramers_v=float(np.sqrt(stat / (n * k))) if k else float("nan"),
                v_excess=float(np.sqrt(max(stat - null.mean(), 0) / (n * k))) if k else float("nan"))


def codes(vals):
    u, c = np.unique(np.asarray(vals, dtype=str), return_inverse=True)
    return u, c


def main():
    df = load()
    assert set(df["split"]) == {"explore"}, "holdout texts present"
    roles, _ = assign(list(df["signs"]))  # frozen rule, all exploration texts
    seals = df[df["object_type"] == "seal"]
    uni = seals[seals["motif_group"] == "unicorn"]
    nu = seals[~seals["motif_group"].astype(str).isin(["unicorn", "none", "unknown", "nan"])].reset_index(drop=True)
    raw_counts = nu["motif_group"].value_counts()
    keep = set(raw_counts[raw_counts >= MIN_ANIMAL].index)
    animal = np.array([a if a in keep else "other animal" for a in nu["motif_group"]])
    a_names, a_code = codes(animal)
    site = codes(nu["site"].astype(str))[1]
    sets = [set(s) for s in nu["signs"]]
    print(f"Exploration seals {len(seals)}: unicorn {len(uni)}, no animal recorded {int((seals.motif_group == 'none').sum())}, "
          f"other animals {len(nu)}")
    print("   per animal:", raw_counts.to_dict())
    print(f"   animals with < {MIN_ANIMAL} seals merged into 'other animal' ({int((animal == 'other animal').sum())} seals)")
    out = dict(rule=RULE, min_support=MIN_SUPPORT, min_animal=MIN_ANIMAL, n_perm=N_PERM,
               seals=len(seals), unicorn=len(uni), nonunicorn=len(nu), per_animal=raw_counts.to_dict(),
               per_site=nu["site"].value_counts().to_dict())

    # ---- 1. signs and slots against animal ---------------------------------------------
    pres = Counter(x for s in sets for x in s)
    signs = sorted([x for x, n in pres.items() if n >= MIN_SUPPORT], key=lambda x: -pres[x])
    tests1 = []
    for x in signs:
        p = np.array([x in s for s in sets], int)
        r = perm_assoc(p, a_code)
        on = {a_names[k]: int(p[a_code == k].sum()) for k in range(len(a_names))}
        size = {a_names[k]: int((a_code == k).sum()) for k in range(len(a_names))}
        best = max(on, key=lambda a: (on[a] / size[a]) / (p.mean()))
        r.update(test=f"sign {x}", sign=x, seals_with=int(p.sum()), by_animal=on,
                 strongest=dict(animal=best, with_sign=on[best], of=size[best],
                                lift=float(on[best] / size[best] / p.mean())))
        tests1.append(r)

    def slot_tests():
        has = lambda role: np.array([any(roles.get(y) == role for y in s) for s in nu["signs"]], int)  # noqa: E731
        num = np.array([any(y in NUMERALS for y in s) for s in nu["signs"]], int)
        for name, v in [("has an opener", has(0)), ("has a closer", has(2)), ("has a numeral", num)]:
            yield name, v
        last = [s[-1] if roles.get(s[-1]) == 2 else "no closer" for s in nu["signs"]]
        first = [s[0] if roles.get(s[0]) == 0 else "no opener" for s in nu["signs"]]
        for name, vals in [("which closer ends it", last), ("which opener starts it", first)]:
            c = Counter(vals)
            vals = [v if c[v] >= MIN_SUPPORT else "rare" for v in vals]
            yield name, codes(vals)[1]

    for name, v in slot_tests():
        r = perm_assoc(np.asarray(v), a_code)
        r.update(test=f"slot: {name}", levels=int(len(np.unique(v))))
        tests1.append(r)
    for r, q in zip(tests1, bh([t["p"] for t in tests1])):
        r["q"] = float(q)
    out["part1"] = tests1
    print(f"\n== 1. Is presence tied to the animal? {len(signs)} signs on >= {MIN_SUPPORT} non-unicorn seals + 5 slot tests "
          f"(BH across {len(tests1)}) ==")
    for r in sorted(tests1, key=lambda r: r["p"])[:15]:
        s = r.get("strongest")
        extra = (f"  most on {s['animal']} {s['with_sign']}/{s['of']} (x{s['lift']:.1f})" if s else "")
        print(f"   {r['test']:30} V {r['cramers_v']:.2f} (excess {r['v_excess']:.2f})  p={r['p']:.4f}  q={r['q']:.3f}{extra}")

    # ---- 2. each animal against the other non-unicorn seals ----------------------------
    tested_animals = [a for a in raw_counts.index if raw_counts[a] >= MIN_ANIMAL_TEST]
    tests2 = []
    for a in tested_animals:
        on_a = (nu["motif_group"] == a).to_numpy()
        for x in signs:
            p = np.array([x in s for s in sets])
            k, m = int(p[on_a].sum()), int(on_a.sum())
            ko, mo = int(p[~on_a].sum()), int((~on_a).sum())
            _, pv = fisher_exact([[k, m - k], [ko, mo - ko]], alternative="greater")
            tests2.append(dict(animal=a, sign=x, on_animal=k, animal_seals=m, on_others=ko, other_seals=mo,
                               lift=float((k / m) / (ko / mo)) if ko else float("inf"), p=float(pv)))
    for r, q in zip(tests2, bh([t["p"] for t in tests2])):
        r["q"] = float(q)
    out["part2"] = tests2
    print(f"\n== 2. Sign over-represented on one animal vs other non-unicorn seals "
          f"({len(tested_animals)} animals x {len(signs)} signs = {len(tests2)} tests, BH) ==")
    for r in sorted(tests2, key=lambda r: r["p"])[:12]:
        print(f"   {r['sign']:6} on {NAMES.get(r['animal'], r['animal']):20} {r['on_animal']:2}/{r['animal_seals']:2}"
              f"  vs others {r['on_others']:2}/{r['other_seals']}  lift x{r['lift']:.1f}  p={r['p']:.4f}  q={r['q']:.3f}")

    # ---- 3. candidates: unicorn rate and site-stratified check -----------------------------
    cands = sorted({r["sign"] for r in tests1 if r["q"] < 0.1 and r.get("sign")} |
                   {r["sign"] for r in sorted(tests2, key=lambda r: r["p"])[:5]})
    uni_sets = [set(s) for s in uni["signs"]]
    out["candidates"] = {}
    print("\n== 3. Candidates (q < 0.1 in part 1, plus the 5 strongest pairs in part 2) ==")
    for x in cands:
        p = np.array([x in s for s in sets], int)
        strat = perm_assoc(p, a_code, strata=site)
        best = min((r for r in tests2 if r["sign"] == x), key=lambda r: r["p"])
        u = float(np.mean([x in s for s in uni_sets]))
        out["candidates"][x] = dict(unicorn_rate=u, nonunicorn_rate=float(p.mean()), best_animal=best,
                                    p_within_site=strat["p"])
        print(f"   {x:6} on {NAMES.get(best['animal'], best['animal'])}: {best['on_animal']}/{best['animal_seals']} "
              f"({best['on_animal'] / best['animal_seals']:.0%}); other non-unicorn {best['on_others'] / best['other_seals']:.0%}; "
              f"unicorn seals {u:.0%}; animal association with shuffles inside site p={strat['p']:.4f}")

    (ROOT / "results" / "animal_signs_nonunicorn.json").write_text(json.dumps(out, indent=1, default=int))


if __name__ == "__main__":
    main()
