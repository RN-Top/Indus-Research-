"""What kind of thing fills each slot, and does the system behave like language?
(EXPLORATORY; exploration split only. Never reads the holdout.)

1. Slot character: for the opener, content and closer slots, how varied are the
   fillers, how many are one-offs, and do they track context (site, object type,
   seal animal)? Names, titles and grammatical markers predict different profiles.
2. Language fingerprints: one 'clause' per text or several; signs that attach to
   many different neighbours (suffix-like glue); how locked signs are to slots;
   whether texts are unique (personal) or repeated (mass-produced).

    python scripts/functional_meaning.py
"""

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from functional_skeleton import RULE, assign, load, ok  # noqa: E402
from functional_slots import NUMERALS  # noqa: E402
from indus_workbench import controls  # noqa: E402

RNG = np.random.default_rng(11)
OUT = {}


def entropy(c):
    p = np.array(list(c.values()), float)
    p /= p.sum()
    return float(-(p * np.log2(p)).sum())


def mi_excess(xs, ys, n=500):
    def mi(a, b):
        N = len(a)
        j, ca, cb = Counter(zip(a, b)), Counter(a), Counter(b)
        return sum(c / N * np.log2(c * N / (ca[x] * cb[y])) for (x, y), c in j.items())
    o = mi(xs, ys)
    ys = np.array(ys, dtype=object)
    null = [mi(xs, list(ys[RNG.permutation(len(ys))])) for _ in range(n)]
    return o - float(np.mean(null)), float((1 + sum(v >= o for v in null)) / (n + 1))


def slots(s, roles):
    """Split a text into opener part, content part and closer part by role."""
    op = [x for x in s if roles.get(x) == 0]
    cl = [x for x in s if roles.get(x) == 2]
    mid = [x for x in s if roles.get(x) != 0 and roles.get(x) != 2]
    return op, mid, cl


def part1(df, roles):
    print("== 1. What kind of thing fills each slot? ==")
    print("   Expected profiles: NAMES = many different fillers, mostly one-offs; "
          "TITLES/CATEGORIES = a few repeated fillers that track context; "
          "GRAMMATICAL MARKERS = very few fillers, everywhere, tracking nothing.")
    res = {}
    for name, idx in (("opener", 0), ("content", 1), ("closer", 2)):
        fillers, ctx_site, ctx_obj, ctx_motif = [], [], [], []
        for t in df.itertuples():
            part = slots(t.signs, roles)[idx]
            if not part:
                continue
            f = " ".join(part)
            fillers.append(f)
            ctx_site.append(t.site)
            ctx_obj.append(t.object_type)
            ctx_motif.append(t.motif_group if t.object_type == "seal" else None)
        c = Counter(fillers)
        once = sum(1 for v in c.values() if v == 1)
        r = dict(texts=len(fillers), distinct=len(c), one_off_share=once / len(c),
                 texts_with_one_off=once / len(fillers), entropy=entropy(c),
                 top=c.most_common(6))
        # context tracking, restricted to fillers seen 3+ times so one-offs do not inflate MI
        keep = [i for i, f in enumerate(fillers) if c[f] >= 3]
        for lbl, ctx in (("site", ctx_site), ("object", ctx_obj)):
            e, p = mi_excess([fillers[i] for i in keep], [ctx[i] for i in keep])
            r[f"tracks_{lbl}"] = dict(excess_bits=e, p=p, n=len(keep))
        km = [i for i in keep if ctx_motif[i] not in (None, "unknown", "nan")]
        e, p = mi_excess([fillers[i] for i in km], [ctx_motif[i] for i in km])
        r["tracks_seal_animal"] = dict(excess_bits=e, p=p, n=len(km))
        res[name] = r
        print(f"\n   {name.upper()}: {len(fillers)} texts, {len(c)} different fillers; "
              f"{r['one_off_share']:.0%} of fillers occur once ({r['texts_with_one_off']:.0%} of texts)")
        print(f"     commonest: {r['top']}")
        for k in ("tracks_site", "tracks_object", "tracks_seal_animal"):
            v = r[k]
            print(f"     {k:20} excess {v['excess_bits']:+.3f} bits  p={v['p']:.3f}  (n={v['n']})")
    OUT["slots"] = res


def part2(df, roles, df_dups):
    print("\n== 2. Language fingerprints ==")
    seqs = list(df["signs"])
    L = np.array([len(s) for s in seqs])
    print(f"   length: mean {L.mean():.1f}, median {np.median(L):.0f}, longest {L.max()}, "
          f"texts over 10 signs {np.mean(L > 10):.1%}")
    OUT["length"] = dict(mean=float(L.mean()), median=float(np.median(L)), max=int(L.max()),
                         over10=float(np.mean(L > 10)))

    # a. Clauses: does a text ever 'restart' (opener after a closer) or carry 2+ closers apart?
    def restarts(s):
        seen_close = False
        for x in s:
            if roles.get(x) == 2:
                seen_close = True
            elif roles.get(x) == 0 and seen_close:
                return True
        return False
    obs = np.mean([restarts(s) for s in seqs])
    null = [np.mean([restarts(s) for s in controls.shuffle_within_texts(seqs, RNG)]) for _ in range(200)]
    print(f"   a. texts that restart (an opener after a closer): {obs:.1%} (shuffled {np.mean(null):.1%})")
    OUT["restarts"] = dict(observed=float(obs), shuffled=float(np.mean(null)))

    # b. Suffix-like glue: signs that follow many different signs
    pre = {}
    tok = Counter()
    for s in seqs:
        for i in range(1, len(s)):
            pre.setdefault(s[i], Counter())[s[i - 1]] += 1
            tok[s[i]] += 1
    print("   b. signs following the widest variety of signs (top 8 by distinct predecessors, >= 40 uses):")
    glue = []
    for x, c in sorted(pre.items(), key=lambda kv: -len(kv[1])):
        if tok[x] < 40 or x in NUMERALS:
            continue
        glue.append(dict(sign=x, uses=tok[x], distinct_before=len(c), ratio=len(c) / tok[x],
                         role={0: "opener", 1: "middle", 2: "closer"}.get(roles.get(x), "?")))
    for g in glue[:8]:
        print(f"      {g['sign']:6} {g['uses']:4} uses after {g['distinct_before']:3} different signs "
              f"({g['ratio']:.2f} per use)  role {g['role']}")
    OUT["glue"] = glue[:15]

    # c. Slot locking: share of frequent signs whose position is locked vs flexible
    prof = {}
    for s in seqs:
        if len(s) < 3:
            continue
        for i, x in enumerate(s):
            p = prof.setdefault(x, Counter())
            p["start" if i == 0 else "end" if i == len(s) - 1 else "middle"] += 1
    locked = flex = 0
    rows = []
    for x, c in prof.items():
        n = sum(c.values())
        if n < 20:
            continue
        top = max(c.values()) / n
        h = entropy(c) / np.log2(3)
        rows.append((x, n, h))
        if c["start"] / n >= 0.6 or c["end"] / n >= 0.6:
            locked += 1
        elif h >= 0.85:
            flex += 1
    print(f"   c. of {len(rows)} signs used 20+ times (texts of 3+ signs): {locked} locked to start or end (>= 60%), "
          f"{flex} spread evenly over start/middle/end, the rest mostly middle")
    OUT["slot_locking"] = dict(signs=len(rows), locked=locked, flexible=flex)

    # d. Unique or repeated texts, by object type (duplicates kept)
    print("   d. are whole inscriptions unique or repeated? (duplicates kept)")
    rep = {}
    for obj in ("seal", "tablet", "pottery"):
        d = df_dups[df_dups["object_type"] == obj]
        keys = Counter(" ".join(s) for s in d["signs"])
        in_rep = sum(v for v in keys.values() if v > 1) / len(d) if len(d) else float("nan")
        rep[obj] = dict(texts=len(d), distinct=len(keys), share_in_repeated_sets=in_rep)
        print(f"      {obj:8} {len(d):4} inscriptions, {len(keys):4} distinct; "
              f"{in_rep:.0%} belong to a set of identical inscriptions")
    OUT["repetition"] = rep


def main():
    df = load(dedupe=True)
    dfd = load(dedupe=False)
    roles, _ = assign(list(df["signs"]), RULE)
    print(f"Exploration split: {len(df)} distinct texts ({len(dfd)} with duplicates). Rule {RULE}")
    part1(df, roles)
    part2(df, roles, dfd)
    Path(__file__).resolve().parents[1].joinpath("results", "functional_meaning.json").write_text(
        json.dumps(OUT, indent=1, default=float))


if __name__ == "__main__":
    main()
