"""Which parts of Indus inscriptions travel between sites, and which stay local? (EXPLORATORY.)

Idea (Erin): if seals worked in trade or contact that moved by water, the parts a
stranger "on another boat" must read should be shared across sites, while
purely local parts stay at one site. Three questions, exploration split only:

  A. Per sign: how local is it? Locality = Jensen-Shannon divergence between the
     sign's spread over sites and the spread of all signs over sites, minus the
     divergence expected for a sign with the same number of uses drawn from the
     overall spread (so rare signs are not called "local" just for being rare).
  B. Are openers less local (more shared) than closers and middle signs?
     Permutation test: role labels shuffled among signs, within frequency bins.
  C. Do sites on the same waterway share more of their sign inventory than other
     site pairs? Inventories are rarefied to the smallest site; site labels are
     permuted (all 720 orders of 6 sites) for a Mantel-type test, with and
     without removing a distance trend.

Benjamini-Hochberg across every test in this file. The Indus holdout is not read
and nothing is registered.

    python scripts/sign_travel.py
"""

import itertools
import json
import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from functional_skeleton import RULE, assign  # noqa: E402
from functional_slots import NUMERALS, load  # noqa: E402

MIN_SUPPORT = 15
RNG = np.random.default_rng(20261015)
N_PERM = 5000
N_RARE = 500

# Sites with at least MIN_SUPPORT exploration texts. Water setting from the
# sources in data/site_coordinates.csv and Wikipedia; "waterway" groups sites that
# share one river system or one stretch of coast. This is a coarse proxy.
SITES = {
    "Mohenjo-daro": dict(lat=27.32917, lon=68.13889, water="Indus river", way="Indus system"),
    "Chanhujo-daro": dict(lat=26.16, lon=68.32, water="Indus floodplain (river later moved away)",
                          way="Indus system", approx="placed 130 km south of Mohenjo-daro (Wikipedia gives no coordinates)"),
    "Harappa": dict(lat=30.62889, lon=72.86389, water="Ravi, a tributary of the Indus", way="Indus system"),
    "Kalibangan": dict(lat=29.47417, lon=74.13028, water="Ghaggar (seasonal, later dry)", way="Ghaggar-Hakra"),
    "Lothal": dict(lat=22.52139, lon=72.24944, water="estuary on the Gulf of Khambhat (dock)", way="Gujarat coast"),
    "Dholavira": dict(lat=23.8886056, lon=70.2136361, water="island in the Rann of Kutch", way="Gujarat coast"),
}
ABROAD = {  # exploration texts found outside the Indus region
    "Gulf and Mesopotamia (by sea)": ["Ur", "Susa", "Tell Umma", "Qala'at al-Bahrain", "Ra's al-Junayz",
                                      "Salut", "Saar", "Hajar", "Karzakan"],
    "Iran and Central Asia (overland)": ["Luristan", "Altyn Depe", "Gonur Depe", "Shortughai"],
}


def jsd(p, q):
    m = (p + q) / 2
    with np.errstate(divide="ignore", invalid="ignore"):
        a = np.nansum(np.where(p > 0, p * np.log2(p / m), 0))
        b = np.nansum(np.where(q > 0, q * np.log2(q / m), 0))
    return (a + b) / 2


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a["lat"], a["lon"], b["lat"], b["lon"]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def bh(p):
    p = np.asarray(p, float)
    o = np.argsort(p)
    q = p[o] * len(p) / np.arange(1, len(p) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty_like(q)
    out[o] = np.minimum(q, 1)
    return out


def units(s, roles, r):
    u = [x for x in s if roles.get(x) == r]
    return " ".join(u) if u else None


def main():
    df = load()
    assert set(df["split"]) == {"explore"}, "holdout texts present"
    roles, table = assign(list(df["signs"]))  # frozen rule, all exploration texts
    sites = list(SITES)
    core = df[df["site"].isin(sites)]
    print(f"Exploration texts {len(df)}; at the {len(sites)} sites with >= {MIN_SUPPORT} texts: {len(core)}")
    print("   " + ", ".join(f"{s} {int((core.site == s).sum())}" for s in sites))
    out = dict(rule=RULE, min_support=MIN_SUPPORT, sites=SITES, texts_per_site={s: int((core.site == s).sum()) for s in sites})

    # ---- A. locality of each sign ------------------------------------------------
    cnt = {s: Counter(x for seq in core[core.site == s]["signs"] for x in seq) for s in sites}
    base = np.array([sum(cnt[s].values()) for s in sites], float)
    base /= base.sum()
    tot = Counter()
    for s in sites:
        tot.update(cnt[s])
    rows = []
    exp_cache = {}
    for x, n in tot.items():
        if n < MIN_SUPPORT:
            continue
        v = np.array([cnt[s][x] for s in sites], float)
        obs = jsd(v / n, base)
        if n not in exp_cache:
            sim = RNG.multinomial(n, base, size=300)
            exp_cache[n] = float(np.mean([jsd(r / n, base) for r in sim]))
        lift = (v / n) / base
        k = int(np.argmax(lift))
        r = roles.get(x, 1)
        cls = "opener" if r == 0 else "closer" if r == 2 else "numeral" if x in NUMERALS else "middle"
        rows.append(dict(sign=x, uses=int(n), role=cls, sites_present=int((v > 0).sum()),
                         top_site=sites[k], top_site_share=float(v[k] / n), top_site_lift=float(lift[k]),
                         locality=float(obs - exp_cache[n]), raw_jsd=float(obs)))
    rows.sort(key=lambda r: r["locality"])
    out["signs"] = rows
    print(f"\n== A. {len(rows)} signs used >= {MIN_SUPPORT} times at these sites ==")
    print("   locality 0 = spread over sites like the corpus as a whole; higher = concentrated at one site")
    print("   Most travelling (by locality, used >= 40 times):")
    for r in [r for r in rows if r["uses"] >= 40][:12]:
        print(f"      {r['sign']:6} {r['role']:8} uses {r['uses']:4} sites {r['sites_present']}/6  locality {r['locality']:+.3f}")
    print("   Most local:")
    for r in rows[::-1][:15]:
        print(f"      {r['sign']:6} {r['role']:8} uses {r['uses']:4} sites {r['sites_present']}/6  locality {r['locality']:+.3f}"
              f"  {r['top_site']} {r['top_site_share']:.0%} of uses (x{r['top_site_lift']:.1f})")

    # ---- B. roles: are openers less local? -------------------------------------------
    loc = np.array([r["locality"] for r in rows])
    role = np.array([r["role"] for r in rows])
    uses = np.array([r["uses"] for r in rows])
    bins = np.digitize(np.log(uses), np.quantile(np.log(uses), [0.25, 0.5, 0.75]))
    print("\n== B. Locality by role (mean; lower = more shared) ==")
    summ = {}
    for g in ["opener", "middle", "closer", "numeral"]:
        m = role == g
        summ[g] = dict(signs=int(m.sum()), mean_locality=float(loc[m].mean()), median=float(np.median(loc[m])),
                       all_six_sites=float(np.mean([r["sites_present"] == 6 for r in rows if r["role"] == g])))
        print(f"   {g:8} {m.sum():3} signs  mean {loc[m].mean():+.3f}  median {np.median(loc[m]):+.3f}  "
              f"found at all 6 sites: {summ[g]['all_six_sites']:.0%}")
    out["by_role"] = summ

    def perm_diff(a, b):
        keep = np.isin(role, [a, b])
        lab, l, bn = role[keep], loc[keep], bins[keep]
        obs = l[lab == a].mean() - l[lab == b].mean()
        null = np.empty(N_PERM)
        for i in range(N_PERM):
            sh = lab.copy()
            for g in np.unique(bn):
                idx = np.flatnonzero(bn == g)
                sh[idx] = RNG.permutation(lab[idx])
            null[i] = l[sh == a].mean() - l[sh == b].mean()
        sd = np.sqrt((l[lab == a].var(ddof=1) + l[lab == b].var(ddof=1)) / 2)
        return dict(diff=float(obs), p=float((1 + (np.abs(null) >= abs(obs)).sum()) / (N_PERM + 1)),
                    cohen_d=float(obs / sd) if sd > 0 else float("nan"))

    tests = []
    for a, b in [("opener", "closer"), ("opener", "middle"), ("closer", "middle")]:
        r = perm_diff(a, b)
        r["test"] = f"locality {a} - {b}"
        tests.append(r)

    # ---- C. site pairs: do sites on one waterway share more? ---------------------------
    texts = {s: list(core[core.site == s]["signs"]) for s in sites}
    n_min = min(len(t) for t in texts.values())
    kinds = {"signs": lambda s: set(s), "opening units": lambda s: {units(s, roles, 0)} - {None},
             "closing units": lambda s: {units(s, roles, 2)} - {None}}
    J = {k: np.zeros((6, 6)) for k in kinds}
    for _ in range(N_RARE):
        inv = {k: [] for k in kinds}
        for s in sites:
            pick = RNG.choice(len(texts[s]), n_min, replace=False)
            for k, f in kinds.items():
                inv[k].append(set().union(*[f(texts[s][i]) for i in pick]))
        for k in kinds:
            for i, j in itertools.combinations(range(6), 2):
                a, b = inv[k][i], inv[k][j]
                J[k][i, j] += len(a & b) / len(a | b) / N_RARE
    for k in kinds:
        J[k] = J[k] + J[k].T
    D = np.array([[km(SITES[a], SITES[b]) for b in sites] for a in sites])
    W = np.array([[SITES[a]["way"] == SITES[b]["way"] for b in sites] for a in sites], float)
    iu = np.triu_indices(6, 1)
    pairs = [dict(a=sites[i], b=sites[j], same_waterway=bool(W[i, j]), km=round(float(D[i, j])),
                  **{k: float(J[k][i, j]) for k in kinds}) for i, j in zip(*iu)]
    out["pairs"] = pairs
    out["rarefied_to_texts"] = n_min
    print(f"\n== C. Site pairs (each site rarefied to {n_min} texts, {N_RARE} draws; Jaccard overlap) ==")
    for p in sorted(pairs, key=lambda p: -p["signs"]):
        print(f"   {p['a']:14} {p['b']:14} {'SAME waterway' if p['same_waterway'] else 'different':13} {p['km']:5} km"
              f"  signs {p['signs']:.2f}  openings {p['opening units']:.2f}  closings {p['closing units']:.2f}")

    logd = np.log(D[iu])
    w = W[iu]
    perms = list(itertools.permutations(range(6)))
    for k in kinds:
        y = J[k][iu]
        res = y - np.polyval(np.polyfit(logd, y, 1), logd)  # distance trend removed
        for label, v in [("raw", y), ("distance removed", res)]:
            def stat(P, v=v, y=y):
                if label == "raw":
                    M = J[k][np.ix_(P, P)][iu]
                else:
                    M = J[k][np.ix_(P, P)][iu]
                    M = M - np.polyval(np.polyfit(logd, M, 1), logd)
                return M[w == 1].mean() - M[w == 0].mean()
            obs = stat(list(range(6)))
            null = np.array([stat(list(P)) for P in perms])
            tests.append(dict(test=f"same waterway > different, {k}, {label}", diff=float(obs),
                              p=float((null >= obs - 1e-12).mean()),
                              same_mean=float(v[w == 1].mean()), different_mean=float(v[w == 0].mean())))
    r_d = {k: float(np.corrcoef(logd, J[k][iu])[0, 1]) for k in kinds}
    out["corr_overlap_vs_log_distance"] = r_d

    q = bh([t["p"] for t in tests])
    for t, qi in zip(tests, q):
        t["q"] = float(qi)
    out["tests"] = tests
    print(f"\n== Tests (BH across all {len(tests)}) ==")
    for t in tests:
        extra = f"  d={t['cohen_d']:+.2f}" if "cohen_d" in t else f"  same {t['same_mean']:+.3f} vs different {t['different_mean']:+.3f}"
        print(f"   {t['test']:52} diff {t['diff']:+.3f}{extra}  p={t['p']:.4f}  q={t['q']:.4f}")
    print("   correlation of overlap with log distance:", {k: round(v, 2) for k, v in r_d.items()})

    # ---- D. texts found abroad (descriptive) -------------------------------------------
    print("\n== D. Exploration texts found outside the Indus region (descriptive only) ==")
    known = {r["sign"]: r for r in rows}
    out["abroad"] = {}
    for g, names in ABROAD.items():
        sub = df[df.site.isin(names)]
        toks = [x for s in sub["signs"] for x in s]
        res = dict(texts=len(sub), signs=len(toks),
                   share_common_shared=float(np.mean([x in known and known[x]["locality"] < 0.02 for x in toks])) if toks else None,
                   with_opener=int(sum(any(roles.get(x) == 0 for x in s) for s in sub["signs"])),
                   with_closer=int(sum(any(roles.get(x) == 2 for x in s) for s in sub["signs"])),
                   ends_in_closer=int(sum(roles.get(s[-1]) == 2 for s in sub["signs"])),
                   texts_list={f"{r.site} ({r.object_type})": list(r.signs) for r in sub.itertuples()})
        out["abroad"][g] = res
        print(f"   {g}: {res['texts']} texts; with an opener {res['with_opener']}, with a closer {res['with_closer']}, "
              f"ending in a closer {res['ends_in_closer']}")
    home = df[df.site.isin(sites)]
    out["home_rates"] = dict(with_opener=float(np.mean([any(roles.get(x) == 0 for x in s) for s in home.signs])),
                             with_closer=float(np.mean([any(roles.get(x) == 2 for x in s) for s in home.signs])),
                             ends_in_closer=float(np.mean([roles.get(s[-1]) == 2 for s in home.signs])))
    print("   at the six home sites: " + ", ".join(f"{k} {v:.0%}" for k, v in out["home_rates"].items()))

    (ROOT / "results" / "sign_travel_water.json").write_text(json.dumps(out, indent=1, default=float))


if __name__ == "__main__":
    main()
