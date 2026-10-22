"""Copper tablets as an answer key for marks (EXPLORATION split only; holdout copper tablets not read).

On the Mohenjo-daro copper tablets the text predicts the picture (H-2026-10-20-c3207807). So when two
copper texts differ by one sign, the pictures say whether that one sign changed the meaning.

Pairs of distinct copper texts (specific picture, not "Othr"/unknown) that differ by one substituted sign
at the same position are classed by how the two signs relate, using the blind mark annotation
(data/sign_marks/marks_blind_2026-10-20.csv):
  mark swap  - one sign is a marked variant of the other, or both are marked variants of one base
               (sub-classed by where the differing marks sit: inside / outside / both / top / other)
  unrelated  - the two signs belong to different families
Outcome: do the two texts carry the same picture (majority picture of each text)?
Null for the difference between classes: class labels permuted over the swap pairs (5,000 times).
Also one-sign insertions (text B = text A with one extra sign).
"""
import csv, json, sys
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from indus_workbench import data  # noqa: E402

VAGUE = {"Othr", "unknown", "nan", "", "-", "None"}
RNG = np.random.default_rng(20261022)
OUTER = lambda m: m in ("enclosure_strokes", "brackets") or m.startswith("side_strokes")
INNER = lambda m: m in ("inner_line", "inner_dot", "crossbar")
TOP = lambda m: m in ("roof", "antennae") or m.startswith("top_strokes")

ann = {r["sign"]: r for r in csv.DictReader(open(ROOT / "data/sign_marks/marks_blind_2026-10-20.csv"))}
parent = {s: (s if r["base"] in ("self", "") else r["base"]) for s, r in ann.items()}


def fam(g):
    seen = set()
    while g in parent and parent[g] != g and g not in seen:
        seen.add(g); g = parent[g]
    return g


def marks(g):
    r = ann.get(g)
    return [] if r is None or r["base"] in ("self", "") else [m for m in r["marks"].split(";") if m]


def mclass(ms):
    o, i, t = any(map(OUTER, ms)), any(map(INNER, ms)), any(map(TOP, ms))
    return "both" if o and i else "outside" if o else "inside" if i else "top" if t else "other"


def relation(a, b):
    if a not in ann or b not in ann:
        return "unannotated", None
    if fam(a) != fam(b):
        return "unrelated", None
    # differing marks: marks of the marked one(s) relative to the other
    ma, mb = set(marks(a)), set(marks(b))
    if parent.get(a) == b:
        diff = ma
    elif parent.get(b) == a:
        diff = mb
    else:
        diff = ma ^ mb
    if not diff:  # same kind of mark on both, drawn differently (e.g. two inner lines of different shape)
        return "mark swap", mclass(list(ma | mb)) + " (mark shape)"
    return "mark swap", mclass(list(diff))


def main():
    raw, _ = data.load_raw("indus_website")
    a = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"),
                          drop_damaged=True, dedupe=False, drop_unidentified=True).df
    cu = a[a.material.astype(str).str.contains("opper", case=False) & (a.split == "explore")].copy()
    cu["motif"] = cu.motif.astype(str)
    cu = cu[~cu.motif.isin(VAGUE)]
    pic = {}
    for t, g in cu.groupby(cu.signs.map(tuple)):
        pic[t] = (Counter(g.motif).most_common(1)[0][0], len(g))
    texts = sorted(pic)
    print(f"Copper objects with a specific picture (exploration): {len(cu)}; distinct texts: {len(texts)}")

    rows = []
    for i, s in enumerate(texts):
        for t in texts[i + 1:]:
            if len(s) == len(t):
                d = [k for k in range(len(s)) if s[k] != t[k]]
                if len(d) == 1:
                    k = d[0]; rel, cls = relation(s[k], t[k])
                    rows.append(dict(kind="substitution", a=" ".join(s), b=" ".join(t), sa=s[k], sb=t[k],
                                     relation=rel, mark_class=cls, pic_a=pic[s][0], pic_b=pic[t][0],
                                     same=pic[s][0] == pic[t][0]))
            elif abs(len(s) - len(t)) == 1:
                lo, hi = (s, t) if len(s) < len(t) else (t, s)
                for k in range(len(hi)):
                    if hi[:k] + hi[k + 1:] == lo:
                        rows.append(dict(kind="insertion", a=" ".join(lo), b=" ".join(hi), sa="", sb=hi[k],
                                         relation="insertion", mark_class=None, pic_a=pic[lo][0], pic_b=pic[hi][0],
                                         same=pic[lo][0] == pic[hi][0]))
                        break

    def rate(rs):
        return (sum(r["same"] for r in rs), len(rs))

    subs = [r for r in rows if r["kind"] == "substitution"]
    summary = {}
    print("\nOne-sign substitutions:")
    for rel in ("mark swap", "unrelated", "unannotated"):
        rs = [r for r in subs if r["relation"] == rel]
        h, n = rate(rs); summary[rel] = [h, n]
        print(f"  {rel:12} same picture {h}/{n}" + (f" = {h/n:.0%}" if n else ""))
    for cls in sorted({r["mark_class"] for r in subs if r["mark_class"]}):
        rs = [r for r in subs if r["mark_class"] == cls]
        h, n = rate(rs); summary["mark swap: " + cls] = [h, n]
        if n:
            print(f"     mark swap, {cls:8} same picture {h}/{n}")
    ins = [r for r in rows if r["kind"] == "insertion"]
    h, n = rate(ins); summary["insertion"] = [h, n]
    print(f"  one-sign insertions: same picture {h}/{n}")

    # permutation: mark swap vs unrelated
    test = [r for r in subs if r["relation"] in ("mark swap", "unrelated")]
    lab = np.array([r["relation"] == "mark swap" for r in test]); y = np.array([r["same"] for r in test], float)
    p = None
    if lab.sum() and (~lab).sum():
        obs = y[lab].mean() - y[~lab].mean()
        null = []
        for _ in range(5000):
            q = RNG.permutation(lab); null.append(y[q].mean() - y[~q].mean())
        p = (1 + sum(x >= obs for x in null)) / 5001
        print(f"\n  mark swap minus unrelated: {obs:+.2f}  (one-sided p = {p:.4f}, labels permuted)")
    summary["p_markswap_vs_unrelated"] = p

    print("\nAll pairs (picture A | picture B):")
    for r in sorted(rows, key=lambda r: (r["relation"], r["mark_class"] or "", r["sa"])):
        tag = r["relation"] + (f"/{r['mark_class']}" if r["mark_class"] else "")
        print(f"  [{tag:18}] {r['sa'] or '+'}->{r['sb']:6} {'SAME' if r['same'] else 'DIFF'}  "
              f"{r['a']}  ({r['pic_a']})  |  {r['b']}  ({r['pic_b']})")
    json.dump({"summary": summary, "pairs": rows}, open(ROOT / "results/copper_marks_scouting.json", "w"), indent=1)


if __name__ == "__main__":
    main()
