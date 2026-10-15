"""Do closer signs act as category markers? (EXPLORATORY; exploration split only.)

For each closer found by the frozen role rule (results/functional_by_site.md D.1),
take the texts whose final sign is that closer and ask whether they are spread
over object types, sites and seal animals differently from all other texts.

Test: chi-square statistic of the 2 x K table (ends in this closer / does not, by
category), compared with 5,000 shuffles of which texts end in the closer
(a permutation null; no chi-square tables are used for p). Effect sizes: Cramer's V
(phi for a 2 x K table) and the category with the largest positive adjusted
residual, with its lift. Benjamini-Hochberg across every closer x field test.

Secondary check: the same test with shuffles kept inside strata (inside each site
for object type and animal; inside each object type for site), because sites
and object types are tangled (Harappa has most tablets).

Nothing here reads the Indus holdout, and nothing is registered.

    python scripts/closer_categories.py
"""

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from functional_skeleton import RULE, assign  # noqa: E402
from functional_slots import load  # noqa: E402

MIN_SUPPORT = 15
N_PERM = 5000
RNG = np.random.default_rng(20261015)


def collapse(labels, min_n, other):
    c = Counter(labels)
    return np.array([x if c[x] >= min_n else other for x in labels])


def chi2(member, codes, k):
    """Chi-square of the 2 x k table; member is boolean (n,) or (p, n)."""
    tot = np.bincount(codes, minlength=k).astype(float)
    n = len(codes)
    m = member.sum(-1, keepdims=True).astype(float)
    if member.ndim == 1:
        obs_in = np.bincount(codes[member], minlength=k).astype(float)
    else:
        obs_in = np.stack([np.bincount(codes[r], minlength=k) for r in member]).astype(float)
    obs_out = tot - obs_in
    e_in = m * tot / n
    e_out = (n - m) * tot / n
    with np.errstate(divide="ignore", invalid="ignore"):
        s = np.nansum((obs_in - e_in) ** 2 / e_in + (obs_out - e_out) ** 2 / e_out, -1)
    return s, obs_in


def shuffles(member, strata):
    out = np.empty((N_PERM, len(member)), bool)
    if strata is None:
        for i in range(N_PERM):
            out[i] = RNG.permutation(member)
        return out
    idx = [np.flatnonzero(strata == s) for s in np.unique(strata)]
    for i in range(N_PERM):
        row = member.copy()
        for g in idx:
            row[g] = RNG.permutation(member[g])
        out[i] = row
    return out


def bh(p):
    p = np.asarray(p, float)
    o = np.argsort(p)
    q = p[o] * len(p) / np.arange(1, len(p) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty_like(q)
    out[o] = np.minimum(q, 1)
    return out


def test(member, labels, strata=None):
    cats, codes = np.unique(labels, return_inverse=True)
    k, n = len(cats), len(codes)
    stat, obs_in = chi2(member, codes, k)
    null, _ = chi2(shuffles(member, strata), codes, k)
    p = float((1 + (null >= stat).sum()) / (N_PERM + 1))
    tot = np.bincount(codes, minlength=k)
    m = member.sum()
    v = float(np.sqrt(stat / n))  # 2 x k table: min(r, c) - 1 = 1
    # adjusted residuals for the "ends in this closer" row
    e = m * tot / n
    adj = (obs_in - e) / np.sqrt(e * (1 - m / n) * (1 - tot / n))
    j = int(np.nanargmax(adj))
    return dict(n_texts=int(n), n_closer=int(m), categories=int(k), chi2=float(stat),
                null_mean=float(null.mean()), p=p, cramers_v=v,
                v_excess=float(np.sqrt(max(stat - null.mean(), 0) / n)),
                strongest=dict(category=str(cats[j]), with_closer=int(obs_in[j]),
                               share_with_closer=float(obs_in[j] / m), share_all=float(tot[j] / n),
                               lift=float((obs_in[j] / m) / (tot[j] / n)), adj_residual=float(adj[j])),
                table={str(c): [int(a), int(t)] for c, a, t in zip(cats, obs_in, tot)})


def main():
    df = load()  # exploration split, duplicates removed; the holdout is not loaded
    assert set(df["split"]) == {"explore"}, "holdout texts present"
    seqs = list(df["signs"])
    roles, table = assign(seqs)
    closers = [r["sign"] for r in sorted(table, key=lambda r: -r["tokens"]) if r["role"] == "closer"]
    last = np.array([s[-1] if len(s) else "" for s in seqs])

    df = df.assign(obj=collapse(df["object_type"].astype(str), 10, "other object"),
                   site_c=collapse(df["site"].astype(str), 10, "other sites"))
    seal = (df["object_type"] == "seal").to_numpy()
    animal_known = seal & ~df["motif_group"].astype(str).isin(["none", "unknown", "nan"]).to_numpy()
    animal = collapse(df["motif_group"].astype(str)[animal_known], 8, "other animal")

    out = dict(rule=RULE, min_support=MIN_SUPPORT, n_perm=N_PERM, texts=len(df),
               fields=dict(object_type=dict(df["obj"].value_counts()),
                           site=dict(df["site_c"].value_counts()),
                           seals=int(seal.sum()), seals_with_animal=int(animal_known.sum()),
                           animal=dict(Counter(animal))),
               closers={}, skipped={})
    print(f"Exploration texts: {len(df)}; seals {seal.sum()}, of which {animal_known.sum()} have an animal recorded")
    print("Closers (frozen rule, all exploration texts):", closers)

    rows = []
    for c in closers:
        member = last == c
        res = {"ends_here": int(member.sum())}
        if member.sum() < MIN_SUPPORT:
            out["skipped"][c] = f"only {member.sum()} texts end in it"
            continue
        site_arr = df["site_c"].to_numpy()
        obj_arr = df["obj"].to_numpy()
        res["object_type"] = test(member, obj_arr)
        res["object_type"]["stratified_by_site"] = test(member, obj_arr, site_arr)["p"]
        res["site"] = test(member, site_arr)
        res["site"]["stratified_by_object"] = test(member, site_arr, obj_arr)["p"]
        ma = member[animal_known]
        if ma.sum() >= MIN_SUPPORT:
            res["animal"] = test(ma, animal)
            res["animal"]["stratified_by_site"] = test(ma, animal, site_arr[animal_known])["p"]
        else:
            res["animal_skipped"] = f"only {int(ma.sum())} seals with an animal end in it"
        out["closers"][c] = res
        for f in ("object_type", "site", "animal"):
            if f in res:
                rows.append((c, f))

    q = bh([out["closers"][c][f]["p"] for c, f in rows])
    qs = bh([out["closers"][c][f]["stratified_by_site" if f != "site" else "stratified_by_object"] for c, f in rows])
    for (c, f), qi, qsi in zip(rows, q, qs):
        out["closers"][c][f]["q"] = float(qi)
        out["closers"][c][f]["q_stratified"] = float(qsi)
    out["tests"] = len(rows)

    print(f"\n{len(rows)} tests; BH across all of them\n")
    print(f"{'closer':7}{'field':12}{'n':>5}{'V':>7}{'Vexc':>7}{'p':>9}{'q':>8}{'q_strat':>9}  strongest")
    for c, f in rows:
        r = out["closers"][c][f]
        s = r["strongest"]
        print(f"{c:7}{f:12}{r['n_closer']:5}{r['cramers_v']:7.2f}{r['v_excess']:7.2f}{r['p']:9.4f}{r['q']:8.4f}"
              f"{r['q_stratified']:9.4f}  {s['category']} {s['with_closer']}/{r['n_closer']} "
              f"({s['share_with_closer']:.0%} vs {s['share_all']:.0%}, x{s['lift']:.1f})")
    for c, why in out["skipped"].items():
        print(f"skipped {c}: {why}")
    for c, r in out["closers"].items():
        if "animal_skipped" in r:
            print(f"animal test skipped for {c}: {r['animal_skipped']}")

    (ROOT / "results" / "closer_category_test.json").write_text(json.dumps(out, indent=1, default=int))


if __name__ == "__main__":
    main()
