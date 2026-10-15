"""Does the function stay the same across sites while the signs vary?
(EXPLORATORY; exploration split only. Never reads the holdout.)

A. Skeleton: learn opener/middle/closer roles at one site, check whether texts at
   another site follow the same slot order (cross-site transfer), against the
   same site's own roles (split-half) and a within-text shuffle.
B. Fillers: compare which signs fill each slot (first sign, last sign, item after
   a numeral) between sites, against a null that permutes site labels among texts
   of the same object type.

    python scripts/functional_by_site.py
"""

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from functional_deeper import conforms, eligible  # noqa: E402
from functional_slots import NUMERALS, load, positional_profile, role  # noqa: E402
from indus_workbench import controls  # noqa: E402
from indus_workbench.hypotheses import _jsd  # noqa: E402

RNG = np.random.default_rng(7)
OUT = {}
SMALL = ["Dholavira", "Lothal", "Kalibangan", "Chanhujo-daro"]


def roles_from(seqs, min_tokens=15):
    import functional_slots as fs
    old = fs.MIN_TOKENS
    fs.MIN_TOKENS = min_tokens
    prof = positional_profile(seqs)
    fs.MIN_TOKENS = old
    r = {x: role(x, p) for x, p in prof.items()}
    for n in NUMERALS:
        r[n] = "N"
    return r


def template_rate(seqs, roles, n_null=100):
    el = [s for s in seqs if eligible(s, roles)]
    if len(el) < 10:
        return None
    obs = float(np.mean([conforms(s, roles) for s in el]))
    null = [np.mean([conforms(s, roles) for s in controls.shuffle_within_texts(el, RNG)]) for _ in range(n_null)]
    return dict(rate=obs, n=len(el), shuffled=float(np.mean(null)))


def groups(df):
    g = {s: df[df["site"] == s] for s in ["Mohenjo-daro", "Harappa"] + SMALL}
    g["other sites"] = df[~df["site"].isin(["Mohenjo-daro", "Harappa"] + SMALL)]
    return g


def part_a(df):
    print("== A. Does the slot order transfer between sites? ==")
    res = {}
    for label, d in (("all objects", df), ("seals only", df[df["object_type"] == "seal"])):
        g = groups(d)
        print(f"\n  [{label}]  texts: " + ", ".join(f"{k} {len(v)}" for k, v in g.items()))
        learn = {
            "Mohenjo-daro": roles_from(list(g["Mohenjo-daro"]["signs"])),
            "Harappa": roles_from(list(g["Harappa"]["signs"])),
        }
        # Own roles via split-half, so a site is never scored on the texts its roles came from
        own = {}
        for site in ("Mohenjo-daro", "Harappa"):
            s = list(g[site]["signs"])
            idx = RNG.permutation(len(s))
            h1, h2 = [s[i] for i in idx[: len(s) // 2]], [s[i] for i in idx[len(s) // 2:]]
            own[site] = template_rate(h2, roles_from(h1, 10))
        rows = {}
        for target, d2 in g.items():
            seqs = list(d2["signs"])
            row = {}
            for src, r in learn.items():
                if src == target:
                    row[f"roles from {src}"] = own[src]
                else:
                    row[f"roles from {src}"] = template_rate(seqs, r)
            rows[target] = row
            cells = []
            for k, v in row.items():
                cells.append(f"{k}: " + (f"{v['rate']:.0%} of {v['n']} (shuffle {v['shuffled']:.0%})" if v else "too few"))
            print(f"   {target:14} " + " | ".join(cells))
        # Do the two big sites' roles agree?
        a, b = learn["Mohenjo-daro"], learn["Harappa"]
        shared = [x for x in a if x in b and x not in NUMERALS]
        same = sum(a[x] == b[x] for x in shared)
        diff = [(x, a[x], b[x]) for x in shared if a[x] != b[x]]
        print(f"   roles agree between Mohenjo-daro and Harappa for {same}/{len(shared)} signs; differ: {diff}")
        res[label] = dict(rows=rows, role_agreement=[same, len(shared)], role_differences=diff,
                          sizes={k: len(v) for k, v in g.items()})
    OUT["skeleton"] = res


def slot_tokens(d, slot):
    out = []  # (text index in d, sign)
    for i, s in enumerate(d["signs"]):
        if len(s) < 2:
            continue
        if slot == "first sign":
            out.append((i, s[0]))
        elif slot == "last sign":
            out.append((i, s[-1]))
        elif slot == "item after a numeral":
            out += [(i, y) for x, y in zip(s, s[1:]) if x in NUMERALS and y not in NUMERALS]
    return out


def part_b(df, a="Mohenjo-daro", b="Harappa", n_perm=500):
    print(f"\n== B. Do different signs fill the slots at {a} and {b}? ==")
    d = df[df["site"].isin([a, b])].reset_index(drop=True)
    res = {}
    for label, dd in (("seals only", d[d["object_type"] == "seal"].reset_index(drop=True)),
                      ("all objects, site labels permuted within object type", d)):
        print(f"  [{label}] texts: {a} {int((dd['site'] == a).sum())}, {b} {int((dd['site'] == b).sum())}")
        site = dd["site"].to_numpy()
        strata = dd["object_type"].to_numpy()
        res[label] = {}
        for slot in ("first sign", "last sign", "item after a numeral"):
            toks = slot_tokens(dd, slot)
            ti = np.array([t for t, _ in toks])
            sg = [x for _, x in toks]

            def jsd_for(lab):
                return _jsd(Counter(x for x, t in zip(sg, ti) if lab[t] == a),
                            Counter(x for x, t in zip(sg, ti) if lab[t] == b))
            obs = jsd_for(site)
            null = []
            for _ in range(n_perm):
                lab = site.copy()
                for s in np.unique(strata):
                    m = np.where(strata == s)[0]
                    lab[m] = lab[m][RNG.permutation(len(m))]
                null.append(jsd_for(lab))
            p = (1 + sum(v >= obs for v in null)) / (n_perm + 1)
            # Site-specific fillers: signs used >= 8 times in the slot, with a lopsided share
            ca = Counter(x for x, t in zip(sg, ti) if site[t] == a)
            cb = Counter(x for x, t in zip(sg, ti) if site[t] == b)
            na, nb = sum(ca.values()), sum(cb.values())
            spec = []
            for x in set(ca) | set(cb):
                if ca[x] + cb[x] < 8:
                    continue
                ra, rb = (ca[x] + 0.5) / (na + 1), (cb[x] + 0.5) / (nb + 1)
                ratio = ra / rb
                if ratio >= 3 or ratio <= 1 / 3:
                    spec.append(dict(sign=x, **{a: ca[x], b: cb[x]}, favours=a if ratio > 1 else b,
                                     ratio=round(ratio if ratio > 1 else 1 / ratio, 1)))
            spec.sort(key=lambda r: -r["ratio"])
            res[label][slot] = dict(jsd=obs, null=float(np.mean(null)), excess=obs - float(np.mean(null)),
                                    p=p, tokens=[na, nb], site_specific=spec)
            print(f"   {slot:22} JSD {obs:.3f} vs permuted {np.mean(null):.3f} (excess {obs - np.mean(null):+.3f}) "
                  f"p={p:.3f}  tokens {na}/{nb}")
            for r in spec[:8]:
                print(f"       {r['sign']:6} {a} {r[a]:3}  {b} {r[b]:3}  favours {r['favours']} x{r['ratio']}")
    OUT["fillers"] = res


def part_c(df):
    """Order-free control: does the overall sign mix differ by site as much as the slot fillers do?"""
    print("\n== C. Control: overall sign mix (any position), seals only ==")
    d = df[(df["site"].isin(["Mohenjo-daro", "Harappa"])) & (df["object_type"] == "seal")].reset_index(drop=True)
    site = d["site"].to_numpy()

    def jsd_for(lab):
        return _jsd(Counter(x for s, l in zip(d["signs"], lab) if l == "Mohenjo-daro" for x in s),
                    Counter(x for s, l in zip(d["signs"], lab) if l == "Harappa" for x in s))
    obs = jsd_for(site)
    null = [jsd_for(site[RNG.permutation(len(site))]) for _ in range(500)]
    p = (1 + sum(v >= obs for v in null)) / 501
    print(f"   JSD {obs:.3f} vs permuted {np.mean(null):.3f} (excess {obs - np.mean(null):+.3f}) p={p:.3f}")
    OUT["overall_mix_seals"] = dict(jsd=obs, null=float(np.mean(null)), excess=obs - float(np.mean(null)), p=p)


def main():
    df = load()
    print(f"Exploration split, duplicates removed: {len(df)} texts")
    part_a(df)
    part_b(df)
    part_c(df)
    Path(__file__).resolve().parents[1].joinpath("results", "functional_by_site.json").write_text(
        json.dumps(OUT, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))


if __name__ == "__main__":
    main()
