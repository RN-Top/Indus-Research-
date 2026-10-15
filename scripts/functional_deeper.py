"""Functional structure, second pass (EXPLORATORY; exploration split only).

1. Slot template: how often a whole text follows opener -> middle -> closer,
   whether roles assigned on one half of the exploration split hold on the other.
2. Formula markers vs counted items: which signs behave like G2-after-opener.
3. Does the last sign tell you the object type, beyond G400?

Never reads the holdout.   python scripts/functional_deeper.py
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from functional_slots import NUMERALS, SHORT, load, positional_profile, role  # noqa: E402
from indus_workbench import controls  # noqa: E402

RNG = np.random.default_rng(20261014)
OUT = {}


def roles_from(seqs):
    prof = positional_profile(seqs)
    r = {x: role(x, p) for x, p in prof.items()}
    for n in NUMERALS:
        r[n] = "N"
    return r, prof


RANK = {"O": 0, "N": 1, "Q": 1, "B": 1, "C": 2}


def conforms(s, roles):
    """Known-role signs never step backwards: opener(s), middle, closer(s)."""
    ranks = [RANK[roles[x]] for x in s if x in roles]
    return len(ranks) >= 2 and all(a <= b for a, b in zip(ranks, ranks[1:]))


def eligible(s, roles):
    ranks = {RANK[roles[x]] for x in s if x in roles}
    return len([x for x in s if x in roles]) >= 2 and len(ranks) >= 2


def entropy(c: Counter) -> float:
    n = sum(c.values())
    p = np.array(list(c.values()), float) / n
    return float(-(p * np.log2(p)).sum())


def mutual_info(xs, ys):
    n = len(xs)
    j, a, b = Counter(zip(xs, ys)), Counter(xs), Counter(ys)
    return sum(c / n * np.log2(c * n / (a[x] * b[y])) for (x, y), c in j.items())


def part1(df):
    print("== 1. Slot template ==")
    seqs = list(df["signs"])
    roles, _ = roles_from(seqs)
    elig = [s for s in seqs if eligible(s, roles)]
    obs = np.mean([conforms(s, roles) for s in elig])
    null = []
    for _ in range(200):
        sh = controls.shuffle_within_texts(elig, RNG)
        null.append(np.mean([conforms(s, roles) for s in sh]))
    print(f"   texts with signs from 2+ slots: {len(elig)}; whole text in slot order: {obs:.1%} "
          f"(shuffled {np.mean(null):.1%}, max {np.max(null):.1%})")
    OUT["template"] = dict(eligible=len(elig), conform=obs, shuffled=float(np.mean(null)))

    # Split-half stability of role assignment
    idx = RNG.permutation(len(seqs))
    a = [seqs[i] for i in idx[: len(idx) // 2]]
    b = [seqs[i] for i in idx[len(idx) // 2:]]
    ra, _ = roles_from(a)
    rb, _ = roles_from(b)
    shared = [x for x in ra if x in rb and x not in NUMERALS]
    agree = Counter((ra[x], rb[x]) for x in shared)
    same = sum(v for (p, q), v in agree.items() if p == q)
    print(f"   split-half: {len(shared)} non-numeral signs given roles in both halves; same role {same}/{len(shared)}")
    for rl in "OQC":
        ina = {x for x in shared if ra[x] == rl}
        inb = {x for x in shared if rb[x] == rl}
        print(f"     {rl}: half A {len(ina)}, half B {len(inb)}, both {len(ina & inb)}")
    eb = [s for s in b if eligible(s, ra)]
    cb = np.mean([conforms(s, ra) for s in eb])
    print(f"   roles learned on half A, template on half B: {cb:.1%} of {len(eb)} texts")
    OUT["split_half"] = dict(shared=len(shared), same=same, template_on_B=cb, n_B=len(eb))

    # What does a numeral lead into?
    nxt = Counter()
    for s in seqs:
        for x, y in zip(s, s[1:]):
            if x in NUMERALS:
                nxt[roles.get(y, ".") if y not in NUMERALS else "N"] += 1
    tot = sum(nxt.values())
    print("   numeral followed by: " + ", ".join(f"{k} {v / tot:.0%}" for k, v in nxt.most_common()))
    OUT["after_numeral"] = dict(nxt)
    return roles


def part2(df, roles):
    print("\n== 2. Formula markers vs counted items ==")
    seqs = list(df["signs"])
    openers = {x for x, r in roles.items() if r == "O"}

    # G2 after an opener vs G2 elsewhere: what follows?
    after_o, after_x = Counter(), Counter()
    for s in seqs:
        for i in range(1, len(s) - 1):
            if s[i] == "G2":
                (after_o if s[i - 1] in openers else after_x)[s[i + 1]] += 1
    num_o = sum(v for k, v in after_o.items() if k in NUMERALS) / sum(after_o.values())
    num_x = sum(v for k, v in after_x.items() if k in NUMERALS) / sum(after_x.values())
    print(f"   G2 after an opener ({sum(after_o.values())}): next sign is a numeral {num_o:.0%}; "
          f"G2 elsewhere ({sum(after_x.values())}): {num_x:.0%}")
    toks = [(lab, y) for lab, c in (("o", after_o), ("x", after_x)) for y, n in c.items() for _ in range(n)]
    labs = np.array([t[0] == "o" for t in toks])
    ys = [t[1] for t in toks]

    def jsd(lab):
        from indus_workbench.hypotheses import _jsd
        return _jsd(Counter(y for y, l in zip(ys, lab) if l), Counter(y for y, l in zip(ys, lab) if not l))
    o = jsd(labs)
    nl = [jsd(labs[RNG.permutation(len(labs))]) for _ in range(500)]
    p = (1 + sum(v >= o for v in nl)) / 501
    print(f"   do the two kinds of G2 lead into different signs? JSD {o:.3f} vs shuffled {np.mean(nl):.3f}, p={p:.3f}")
    OUT["g2_split"] = dict(n_after_opener=sum(after_o.values()), n_else=sum(after_x.values()),
                           numeral_next_after_opener=num_o, numeral_next_else=num_x, jsd=o,
                           jsd_null=float(np.mean(nl)), p=p)

    # Profile every common sign: how tied it is to the sign before (attachment),
    # how varied what follows is, and how often it follows a numeral.
    pre, post, tok = defaultdict(Counter), defaultdict(Counter), Counter()
    for s in seqs:
        for i, x in enumerate(s):
            tok[x] += 1
            pre[x][s[i - 1] if i else "<s>"] += 1
            post[x][s[i + 1] if i < len(s) - 1 else "</s>"] += 1
    rows = []
    for x, n in tok.items():
        if n < 20:
            continue
        top, k = pre[x].most_common(1)[0]
        after_num = sum(v for y, v in pre[x].items() if y in NUMERALS) / n
        next_num = sum(v for y, v in post[x].items() if y in NUMERALS) / n
        rows.append(dict(sign=x, tokens=n, top_before=top, attach=k / n, after_numeral=after_num,
                         next_numeral=next_num, post_entropy=entropy(post[x]), role=roles.get(x, ".")))
    # A "hinge" (formula marker): one fixed sign before it, and very often a
    # numeral or varied material after it. A counted item: many different numerals before it.
    hinge = [r for r in rows if r["attach"] >= 0.4 and r["top_before"] not in ("<s>",)
             and r["top_before"] not in NUMERALS]
    print("   signs tied to one particular preceding sign (attach >= 40%, not a numeral, not text start):")
    for r in sorted(hinge, key=lambda r: -r["attach"]):
        print(f"     {r['sign']:6} n={r['tokens']:3} after {r['top_before']:6} {r['attach']:.0%}  "
              f"next is numeral {r['next_numeral']:.0%}  role {r['role']}")
    print("   numerals: share right after an opener, and share followed by another numeral:")
    nrows = []
    for x in sorted(NUMERALS, key=lambda x: -tok[x]):
        if tok[x] < 10:
            continue
        ao = sum(v for y, v in pre[x].items() if y in openers) / tok[x]
        nn = sum(v for y, v in post[x].items() if y in NUMERALS) / tok[x]
        end = post[x]["</s>"] / tok[x]
        nrows.append(dict(sign=x, tokens=tok[x], after_opener=ao, next_numeral=nn, ends=end))
        print(f"     {x:5} n={tok[x]:3}  after opener {ao:.0%}  followed by numeral {nn:.0%}  ends text {end:.0%}")
    OUT["hinges"] = hinge
    OUT["numerals"] = nrows


def part3(df):
    print("\n== 3. Does the closing sign tell you the object? ==")
    d = df[df["signs"].map(len) >= 2]
    d = d[d["object_type"].isin(["seal", "tablet"])]
    first = [s[0] for s in d["signs"]]
    last = [s[-1] for s in d["signs"]]
    mid = [s[len(s) // 2] for s in d["signs"]]
    obj = list(d["object_type"])

    def mi_with_null(xs, ys, n=500):
        o = mutual_info(xs, ys)
        ys = np.array(ys)
        nl = [mutual_info(xs, list(ys[RNG.permutation(len(ys))])) for _ in range(n)]
        return o, float(np.mean(nl)), (1 + sum(v >= o for v in nl)) / (n + 1)

    res = {}
    for name, xs in (("first sign", first), ("middle sign", mid), ("last sign", last)):
        o, nm, p = mi_with_null(xs, obj)
        res[name] = dict(mi=o, null=nm, excess=o - nm, p=p)
        print(f"   {name:12} information about seal vs tablet: {o:.3f} bits (shuffled {nm:.3f}; excess {o - nm:.3f}) p={p:.3f}")
    keep = [i for i, x in enumerate(last) if x != "G400"]
    o, nm, p = mi_with_null([last[i] for i in keep], [obj[i] for i in keep])
    print(f"   last sign, texts ending G400 removed ({len(keep)}): excess {o - nm:.3f} bits, p={p:.3f}")
    res["last_without_G400"] = dict(n=len(keep), excess=o - nm, p=p)

    # Same within one site, so site cannot explain it
    for site in ("Harappa", "Mohenjo-daro"):
        dd = d[d["site"] == site]
        ls = [s[-1] for s in dd["signs"]]
        k = [i for i, x in enumerate(ls) if x != "G400"]
        if len(set(dd["object_type"])) < 2 or len(k) < 30:
            continue
        ob = list(dd["object_type"])
        o, nm, p = mi_with_null([ls[i] for i in k], [ob[i] for i in k])
        print(f"   within {site}, without G400 ({len(k)} texts; tablets {np.mean([ob[i] == 'tablet' for i in k]):.0%}): "
              f"excess {o - nm:.3f} bits, p={p:.3f}")
        res[f"within_{site}_no_G400"] = dict(n=len(k), excess=o - nm, p=p)

    # Which closers lean which way (>= 10 texts)
    base = np.mean([o == "tablet" for o in obj])
    print(f"   baseline tablets {base:.0%}. Closing signs with >= 10 texts:")
    lean = []
    for x, n in Counter(last).most_common():
        if n < 10:
            break
        t = np.mean([o == "tablet" for l, o in zip(last, obj) if l == x])
        sites = Counter(s for l, s in zip(last, d["site"]) if l == x).most_common(2)
        lean.append(dict(sign=x, texts=n, tablet=t, sites=sites))
        print(f"     {x:6} {n:4} texts  tablets {t:.0%}  sites {sites}")
    res["closers"] = lean
    OUT["object_from_closer"] = res


def main():
    df = load()
    print(f"Exploration split, duplicates removed: {len(df)} texts\n")
    roles = part1(df)
    part2(df, roles)
    part3(df)
    Path(__file__).resolve().parents[1].joinpath("results", "functional_deeper.json").write_text(
        json.dumps(OUT, indent=1, default=float))


if __name__ == "__main__":
    main()
