"""Cross-site skeleton, tightened (EXPLORATORY; exploration split only).

One explicit role rule, frozen in RULE below, so it could later be pre-registered:
  - numeral: a stroke sign (fixed list, by shape)
  - opener:  >= min_tokens uses in texts of 2+ signs; starts >= open_share of
             them; and starts >= ratio x the share expected if signs were shuffled
             within their texts
  - closer:  the same, for ending a text (close_share)
  - middle:  every other sign with >= min_tokens uses
A text "conforms" if its role-assigned signs never step backwards
(opener -> middle/numeral -> closer). Only texts with role signs from at least
two different ranks are scored. Never reads the holdout.

    python scripts/functional_skeleton.py
"""

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from functional_slots import DS, NUMERALS  # noqa: E402
from indus_workbench import controls, data  # noqa: E402

RULE = dict(min_tokens=15, open_share=0.4, close_share=0.5, ratio=1.8)
SITES = ["Mohenjo-daro", "Harappa", "Dholavira", "Lothal", "Kalibangan", "Chanhujo-daro"]
RNG = np.random.default_rng(42)
N_NULL = 200
OUT = {"rule": RULE}


def load(dedupe=True):
    raw, _ = data.load_raw("indus_website")
    ds = dict(DS, dedupe=dedupe)
    c = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"), **ds)
    df = data.explore_only(c).df.reset_index(drop=True)
    df["group"] = df["site"].where(df["site"].isin(SITES), "other sites")
    return df


def assign(seqs, rule=RULE):
    tok, st, en, exp = Counter(), Counter(), Counter(), Counter()
    for s in seqs:
        if len(s) < 2:
            continue
        for i, x in enumerate(s):
            tok[x] += 1
            exp[x] += 1 / len(s)
            st[x] += i == 0
            en[x] += i == len(s) - 1
    roles, table = {}, []
    for x, n in tok.items():
        if x in NUMERALS:
            roles[x] = 1
            continue
        if n < rule["min_tokens"]:
            continue
        e = exp[x] / n
        s_, e_ = st[x] / n, en[x] / n
        if e_ >= rule["close_share"] and e_ >= rule["ratio"] * e:
            roles[x] = 2
            table.append(dict(sign=x, role="closer", tokens=n, ends=e_, starts=s_, shuffled=e))
        elif s_ >= rule["open_share"] and s_ >= rule["ratio"] * e:
            roles[x] = 0
            table.append(dict(sign=x, role="opener", tokens=n, starts=s_, ends=e_, shuffled=e))
        else:
            roles[x] = 1
    for n in NUMERALS:
        roles[n] = 1
    return roles, table


def scorable(s, roles):
    return len({roles[x] for x in s if x in roles}) >= 2


def ok(s, roles):
    r = [roles[x] for x in s if x in roles]
    return all(a <= b for a, b in zip(r, r[1:]))


def conformance(seqs, roles):
    el = [s for s in seqs if scorable(s, roles)]
    if len(el) < 10:
        return dict(n=len(el), rate=None)
    obs = float(np.mean([ok(s, roles) for s in el]))
    null = np.array([np.mean([ok(s, roles) for s in controls.shuffle_within_texts(el, RNG)])
                     for _ in range(N_NULL)])
    p = float((1 + (null >= obs).sum()) / (N_NULL + 1))
    kappa = (obs - null.mean()) / (1 - null.mean())  # share of the non-chance range achieved
    return dict(n=len(el), rate=obs, null=float(null.mean()), null95=float(np.quantile(null, 0.95)),
                p=p, kappa=float(kappa))


def fmt(r):
    if r["rate"] is None:
        return f"n={r['n']:3} too few"
    return (f"{r['rate']:5.1%} of {r['n']:3}  shuffled {r['null']:5.1%} (95th pct {r['null95']:5.1%})  "
            f"chance-corrected {r['kappa']:.2f}")


def split_half_self(seqs, rule=RULE):
    idx = RNG.permutation(len(seqs))
    a = [seqs[i] for i in idx[: len(idx) // 2]]
    b = [seqs[i] for i in idx[len(idx) // 2:]]
    ra, _ = assign(a, dict(rule, min_tokens=max(5, rule["min_tokens"] // 2)))
    return conformance(b, ra)


def transfer_table(df, source, label, rule=RULE, quiet=False):
    src = list(df[df["group"] == source]["signs"]) if source != "LOSO" else None
    roles, table = (assign(src, rule) if src is not None else (None, None))
    rows = {}
    for g in SITES + ["other sites"]:
        tgt = list(df[df["group"] == g]["signs"])
        if source == "LOSO":
            r_ = assign(list(df[df["group"] != g]["signs"]), rule)[0]
            rows[g] = conformance(tgt, r_)
        elif g == source:
            rows[g] = split_half_self(tgt, rule)
        else:
            rows[g] = conformance(tgt, roles)
        if not quiet:
            star = " (split-half, own site)" if g == source else ""
            print(f"   {g:14} {fmt(rows[g])}{star}")
    others = [g for g in SITES + ["other sites"] if g != source and rows[g]["rate"] is not None]
    pooled_n = sum(rows[g]["n"] for g in others)
    pooled = sum(rows[g]["rate"] * rows[g]["n"] for g in others) / pooled_n
    pooled_null = sum(rows[g]["null"] * rows[g]["n"] for g in others) / pooled_n
    if not quiet:
        print(f"   {'pooled (not source)':14} {pooled:5.1%} of {pooled_n}  shuffled {pooled_null:5.1%}")
    return dict(roles_table=table, rows=rows, pooled=dict(rate=pooled, n=pooled_n, null=pooled_null))


def main():
    df = load(dedupe=True)
    print(f"Exploration split, duplicates removed: {len(df)} texts; "
          + ", ".join(f"{g} {n}" for g, n in df["group"].value_counts().items()))
    print(f"Rule: {RULE}")

    # 1. Final role lists (from Mohenjo-daro, and from all exploration texts)
    for name, seqs in (("Mohenjo-daro", list(df[df["group"] == "Mohenjo-daro"]["signs"])),
                       ("all sites", list(df["signs"]))):
        _, table = assign(seqs)
        OUT[f"roles_{name}"] = table
        print(f"\n== 1. Openers and closers learned from {name} ==")
        for t in sorted(table, key=lambda t: (t["role"], -t["tokens"])):
            k = "starts" if t["role"] == "opener" else "ends"
            print(f"   {t['role']:6} {t['sign']:6} n={t['tokens']:4}  {k} {t[k]:.0%}  (shuffled {t['shuffled']:.0%})")

    # 2. Transfer
    OUT["transfer"] = {}
    for src, label in (("Mohenjo-daro", "roles from Mohenjo-daro only"),
                       ("Harappa", "roles from Harappa only"),
                       ("LOSO", "roles from all OTHER sites (leave one site out)")):
        print(f"\n== 2. {label} ==")
        OUT["transfer"][src] = transfer_table(df, src, label)

    # 3. Robustness: vary each threshold; roles from Mohenjo-daro, pooled over other sites
    print("\n== 3. Robustness (roles from Mohenjo-daro; pooled over all other sites) ==")
    grid = [RULE,
            dict(RULE, min_tokens=10), dict(RULE, min_tokens=25),
            dict(RULE, open_share=0.3), dict(RULE, open_share=0.5),
            dict(RULE, close_share=0.4), dict(RULE, close_share=0.6),
            dict(RULE, ratio=1.5), dict(RULE, ratio=2.5),
            dict(min_tokens=25, open_share=0.5, close_share=0.6, ratio=2.5)]
    rob = []
    for rule in grid:
        r = transfer_table(df, "Mohenjo-daro", "", rule, quiet=True)
        _, t = assign(list(df[df["group"] == "Mohenjo-daro"]["signs"]), rule)
        no = sum(x["role"] == "opener" for x in t)
        nc = sum(x["role"] == "closer" for x in t)
        diff = {k: v for k, v in rule.items() if RULE.get(k) != v} or "baseline rule"
        print(f"   {str(diff):58} openers {no:2} closers {nc:2}  -> {r['pooled']['rate']:.1%} of "
              f"{r['pooled']['n']} (shuffled {r['pooled']['null']:.1%})")
        rob.append(dict(rule=rule, openers=no, closers=nc, **r["pooled"]))
    OUT["robustness"] = rob

    print("\n== 3b. Duplicates kept ==")
    dk = load(dedupe=False)
    print(f"   texts {len(dk)} (vs {len(df)} with duplicates removed)")
    r = transfer_table(dk, "Mohenjo-daro", "", quiet=False)
    OUT["duplicates_kept"] = r["pooled"] | {"rows": r["rows"]}

    Path(__file__).resolve().parents[1].joinpath("results", "functional_skeleton.json").write_text(
        json.dumps(OUT, indent=1, default=float))


if __name__ == "__main__":
    main()
