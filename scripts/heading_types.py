"""Are the Indus openers different kinds of heading? (EXPLORATORY; exploration split only.)

In Mesopotamian seal legends the opening slot holds either 'seal of' (kishib) or an
overlord's name, and each goes with a different kind of legend. Do the main Indus
opener signs likewise go with different endings, objects, sites, lengths or middle
content? Texts are grouped by their first sign when it is an opener (frozen rule).
Chi-square / Jensen-Shannon statistics against 5,000 label shuffles, Cramer's V,
Benjamini-Hochberg across the tests. Nothing reads the holdout or is registered.

    python scripts/heading_types.py
"""

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from closer_categories import bh, chi2  # noqa: E402
from functional_skeleton import assign  # noqa: E402
from functional_slots import NUMERALS, load  # noqa: E402

N = 5000
RNG = np.random.default_rng(20261016)
MIN = 15


def jsd(a, b):
    keys = set(a) | set(b)
    p = np.array([a[k] for k in keys], float); q = np.array([b[k] for k in keys], float)
    p /= p.sum(); q /= q.sum(); m = (p + q) / 2
    f = lambda x: np.sum(np.where(x > 0, x * np.log2(np.where(x > 0, x, 1) / m), 0))  # noqa: E731
    return float((f(p) + f(q)) / 2)


def main():
    df = load()
    roles, _ = assign(list(df["signs"]))
    first = [s[0] if s and roles.get(s[0]) == 0 else None for s in df["signs"]]
    c = Counter(x for x in first if x)
    ops = [o for o, n in c.most_common() if n >= MIN]
    keep = np.array([f in ops for f in first])
    sub = df[keep].reset_index(drop=True)
    lab = np.array([f for f, k in zip(first, keep) if k])
    _, code = np.unique(lab, return_inverse=True)
    print(f"Texts starting with an opener used >= {MIN} times: {len(sub)}; openers {dict((o, c[o]) for o in ops)}")

    def last_role(s):
        return s[-1] if roles.get(s[-1]) == 2 else ("numeral" if s[-1] in NUMERALS else "no closer")
    fields = {
        "ending (which closer, or none)": [last_role(s) for s in sub["signs"]],
        "object type": list(sub["object_type"].astype(str)),
        "site": list(sub["site"].astype(str)),
        "seal animal (seals with one)": None,
        "length (signs)": [str(min(len(s), 7)) for s in sub["signs"]],
        "has a numeral": [str(any(x in NUMERALS for x in s)) for s in sub["signs"]],
    }
    out = {"openers": {o: c[o] for o in ops}, "tests": []}
    for name, vals in fields.items():
        if vals is None:
            m = (sub["object_type"] == "seal").to_numpy() & ~sub["motif_group"].astype(str).isin(["none", "unknown", "nan"]).to_numpy()
            vals_arr, cod = np.array(sub["motif_group"].astype(str))[m], code[m]
        else:
            vals_arr, cod = np.array(vals), code
        cnt = Counter(vals_arr)
        vals_arr = np.array([v if cnt[v] >= 8 else "other" for v in vals_arr])
        _, y = np.unique(vals_arr, return_inverse=True)
        k = cod.max() + 1
        mem = np.eye(k, dtype=bool)[cod]  # not used; chi2 below on full table
        t = np.zeros((k, y.max() + 1)); np.add.at(t, (cod, y), 1)
        def stat(yy):
            tt = np.zeros_like(t); np.add.at(tt, (cod, yy), 1)
            e = tt.sum(1, keepdims=True) * tt.sum(0, keepdims=True) / tt.sum()
            with np.errstate(divide="ignore", invalid="ignore"):
                return float(np.nansum((tt - e) ** 2 / e))
        obs = stat(y); null = np.array([stat(RNG.permutation(y)) for _ in range(N)])
        v = float(np.sqrt(obs / (len(y) * (min(t.shape) - 1))))
        vx = float(np.sqrt(max(obs - null.mean(), 0) / (len(y) * (min(t.shape) - 1))))
        cats = np.unique(vals_arr)
        prof = {}
        for i, o in enumerate(sorted(set(lab[:len(cod)]) if vals is not None else sorted(set(lab)))):
            pass
        rows = {}
        for i, o in enumerate(np.unique(lab)):
            r = t[i]; 
            if r.sum():
                top = np.argsort(-r)[:3]
                rows[o] = [(str(cats[j]), int(r[j]), round(float(r[j] / r.sum()), 2)) for j in top]
        out["tests"].append(dict(test=name, n=int(len(y)), V=v, V_excess=vx, p=float((1 + (null >= obs).sum()) / (N + 1)), top_by_opener=rows))
    # middle content: JSD between each opener's middle-sign distribution and the rest
    mid = [[x for x in s[1:] if roles.get(x) not in (0, 2)] for s in sub["signs"]]
    def jsd_stat(l):
        out_ = []
        for o in ops:
            a = Counter(x for m_, L in zip(mid, l) if L == o for x in m_); b = Counter(x for m_, L in zip(mid, l) if L != o for x in m_)
            out_.append(jsd(a, b))
        return np.mean(out_)
    obs = jsd_stat(lab); null = np.array([jsd_stat(RNG.permutation(lab)) for _ in range(1000)])
    tops = {o: Counter(x for m_, L in zip(mid, lab) if L == o for x in m_).most_common(4) for o in ops}
    out["tests"].append(dict(test="middle content (sign mix)", n=int(len(lab)), V=float("nan"), V_excess=float("nan"),
                             jsd=float(obs), null_mean=float(null.mean()), p=float((1 + (null >= obs).sum()) / 1001), top_by_opener=tops))
    for t, q in zip(out["tests"], bh([t["p"] for t in out["tests"]])):
        t["q"] = float(q)
    for t in out["tests"]:
        extra = f"V {t['V']:.2f} (excess {t['V_excess']:.2f})" if t["V"] == t["V"] else f"JSD {t['jsd']:.3f} vs shuffled {t['null_mean']:.3f}"
        print(f"\n== {t['test']}: n={t['n']}  {extra}  p={t['p']:.4f}  q={t['q']:.4f}")
        for o, r in t["top_by_opener"].items():
            print(f"   {o:6} {r}")
    (ROOT / "results" / "heading_types.json").write_text(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
