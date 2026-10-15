"""Functional-slot analysis (EXPLORATORY; exploration split only).

Assigns each common sign a functional role from where it sits and what it
sits next to, then describes the common chunks by position and object type.
Never reads the holdout.

    python scripts/functional_slots.py > results/functional_slots_output.txt
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from indus_workbench import controls, data  # noqa: E402

DS = {"drop_damaged": True, "dedupe": True, "drop_unidentified": True}
SHORT = [f"G{i}" for i in range(1, 8)]
STACK = ["G13", "G14", "G15", "G16", "G17", "G18", "G19", "G27", "G28", "G29", "G55"]
LONG = ["G31", "G32", "G33", "G35"]
NUMERALS = set(SHORT + STACK + LONG)
MIN_TOKENS = 15


def load():
    raw, _ = data.load_raw("indus_website")
    c = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"), **DS)
    return data.explore_only(c).df.reset_index(drop=True)


def positional_profile(seqs):
    """Start/end share per sign, with the share expected if signs were shuffled
    within their texts (each token's chance of landing first is 1/len)."""
    tok, start, end, exp = Counter(), Counter(), Counter(), Counter()
    after_num = Counter()
    for s in seqs:
        if len(s) < 2:
            continue
        for i, x in enumerate(s):
            tok[x] += 1
            exp[x] += 1 / len(s)
            start[x] += i == 0
            end[x] += i == len(s) - 1
            if i > 0 and s[i - 1] in NUMERALS and x not in NUMERALS:
                after_num[x] += 1
    rows = {}
    for x, n in tok.items():
        if n < MIN_TOKENS:
            continue
        rows[x] = dict(tokens=n, start=start[x] / n, end=end[x] / n, expected=exp[x] / n,
                       after_numeral=after_num[x] / n)
    return rows


def role(x, r):
    if x in NUMERALS:
        return "N"
    e = r["expected"]
    if r["end"] >= 0.5 and r["end"] >= 1.8 * e:
        return "C"  # closer
    if r["start"] >= 0.4 and r["start"] >= 1.8 * e:
        return "O"  # opener
    if r["after_numeral"] >= 0.3:
        return "Q"  # counted item (follows a numeral)
    return "B"  # body / unassigned


def order_score(seqs, roles, a, b):
    """Share of (a-role, b-role) sign pairs in the same text where the a sign comes first."""
    before = total = 0
    for s in seqs:
        pa = [i for i, x in enumerate(s) if roles.get(x) == a]
        pb = [i for i, x in enumerate(s) if roles.get(x) == b]
        for i in pa:
            for j in pb:
                total += 1
                before += i < j
    return before / total if total else float("nan"), total


def main():
    df = load()
    seqs = list(df["signs"])
    prof = positional_profile(seqs)
    roles = {x: role(x, r) for x, r in prof.items()}
    for n in NUMERALS:
        roles.setdefault(n, "N")
    out = {"texts": len(seqs), "roles": {}, "profile": prof}

    print(f"Exploration split, duplicates removed: {len(seqs)} texts\n")
    print("== Roles (signs with >= %d tokens) ==" % MIN_TOKENS)
    by_role = defaultdict(list)
    for x, rl in roles.items():
        if x in prof:
            by_role[rl].append(x)
    for rl in "OCNQB":
        xs = sorted(by_role[rl], key=lambda x: -prof[x]["tokens"])
        out["roles"][rl] = xs
        print(rl, len(xs), "signs;", sum(prof[x]["tokens"] for x in xs), "tokens")
        for x in xs[:15]:
            p = prof[x]
            print(f"   {x:6} n={p['tokens']:4}  start {p['start']:.0%}  end {p['end']:.0%}  "
                  f"(shuffle {p['expected']:.0%})  after-numeral {p['after_numeral']:.0%}")

    # Templates
    print("\n== Role templates (runs collapsed; signs below the token threshold shown as '.') ==")
    tmpl = Counter()
    for s in seqs:
        t = []
        for x in s:
            rl = roles.get(x, ".")
            if not t or t[-1] != rl:
                t.append(rl)
        tmpl["".join(t)] += 1
    for t, n in tmpl.most_common(20):
        print(f"   {t:10} {n:4}  {n / len(seqs):.1%}")
    out["templates"] = tmpl.most_common(30)

    # Order between roles, against within-text shuffle
    print("\n== Order between roles (share where the first role comes first) ==")
    rng = controls.rng(1)
    out["order"] = {}
    for a, b in [("O", "C"), ("O", "Q"), ("O", "N"), ("N", "C"), ("Q", "C"), ("B", "C"), ("O", "B")]:
        obs, tot = order_score(seqs, roles, a, b)
        null = [order_score(controls.shuffle_within_texts(seqs, rng), roles, a, b)[0] for _ in range(200)]
        p = (1 + sum(v >= obs for v in null)) / 201
        out["order"][a + b] = dict(observed=obs, pairs=tot, null=float(np.mean(null)), p=p)
        print(f"   {a} before {b}: {obs:.1%} of {tot} pairs (shuffle {np.mean(null):.1%}), p={p:.3f}")

    # Chunks
    print("\n== Frequent chunks (2-3 signs, in >= 6 distinct texts) ==")
    obj_all = Counter(df["object_type"])
    ng_texts = defaultdict(set)
    for ti, s in enumerate(seqs):
        for n in (2, 3):
            for i in range(len(s) - n + 1):
                ng_texts[tuple(s[i:i + n])].add(ti)
    chunks = []
    for g, tis in ng_texts.items():
        if len(tis) < 6 or all(x in NUMERALS for x in g):
            continue
        st = en = 0
        prenum = 0
        for ti in tis:
            s = seqs[ti]
            for i in range(len(s) - len(g) + 1):
                if tuple(s[i:i + len(g)]) == g:
                    st += i == 0
                    en += i + len(g) == len(s)
                    prenum += i > 0 and s[i - 1] in NUMERALS
                    break
        objs = Counter(df.loc[list(tis), "object_type"])
        chunks.append(dict(chunk=" ".join(g), texts=len(tis), start=st / len(tis), end=en / len(tis),
                           after_numeral=prenum / len(tis), roles="".join(roles.get(x, ".") for x in g),
                           seal=objs.get("seal", 0) / len(tis), tablet=objs.get("tablet", 0) / len(tis),
                           objects=dict(objs.most_common(3))))
    # drop 2-grams wholly contained in an equally frequent 3-gram
    chunks.sort(key=lambda c: -c["texts"])

    def label(c):
        if c["end"] >= 0.6:
            return "closer"
        if c["start"] >= 0.6:
            return "opener"
        if c["roles"][0] == "N" or c["after_numeral"] >= 0.5:
            return "quantity + item"
        if c["tablet"] >= 0.6:
            return "tablet-genre phrase"
        return "medial phrase"
    for c in chunks:
        c["function"] = label(c)
    for c in chunks[:40]:
        print(f"   {c['chunk']:18} {c['texts']:3} texts  start {c['start']:.0%} end {c['end']:.0%} "
              f"after-num {c['after_numeral']:.0%} seal {c['seal']:.0%} tablet {c['tablet']:.0%}  "
              f"[{c['roles']}] -> {c['function']}")
    out["chunks"] = chunks[:80]

    # Object-type marker signs
    print("\n== Signs whose texts lean to one object type (>= 15 texts) ==")
    base = {k: v / len(df) for k, v in obj_all.items()}
    print("   baseline:", {k: f"{v:.0%}" for k, v in sorted(base.items(), key=lambda kv: -kv[1])[:5]})
    marks = []
    for x in prof:
        has = df["signs"].map(lambda s: x in s)
        if has.sum() < 15:
            continue
        objs = Counter(df.loc[has, "object_type"])
        top, k = objs.most_common(1)[0]
        share = k / has.sum()
        if top != "seal" and share >= 0.6:
            marks.append((x, int(has.sum()), top, share, base.get(top, 0)))
    for m in sorted(marks, key=lambda m: -m[3]):
        print(f"   {m[0]:6} {m[1]:4} texts  {m[3]:.0%} {m[2]} (baseline {m[4]:.0%})")
    out["object_markers"] = marks

    Path(__file__).resolve().parents[1].joinpath("results", "functional_slots.json").write_text(
        json.dumps(out, indent=1, default=float))


if __name__ == "__main__":
    main()
