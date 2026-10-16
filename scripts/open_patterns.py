"""Open-minded pattern discovery and prediction. (EXPLORATION ONLY: description and in-sample cross-validation.)

No prior hypothesis. Part A lets sign classes emerge from contexts alone (PPMI of
left and right neighbours, SVD, k-means) and lists recurring motifs and templates,
then checks afterwards which match things already believed (heading, numerals,
closers, end-of-middle slot). Part B asks whether structure predicts: five-fold
cross-validation over exploration texts, comparing a frequency-only baseline with
a bigram model (next sign) and a two-sided model (masked sign from both
neighbours), and reports accuracy by position. The holdout is never read.

    python scripts/open_patterns.py
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from sklearn.cluster import KMeans

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from functional_skeleton import assign  # noqa: E402
from functional_slots import NUMERALS, load  # noqa: E402

RNG = np.random.default_rng(20261016)
MIN_TOK = 10
K = 12
END_SLOT = {"G100", "G760", "G142", "G923"}
BOS, EOS = "<s>", "</s>"


def part_a(seqs, roles, out):
    tok = Counter(x for s in seqs for x in s)
    vocab = [x for x, n in tok.most_common() if n >= MIN_TOK]
    vi = {x: i for i, x in enumerate(vocab)}
    feats = {}
    rows, cols = [], []
    for s in seqs:
        p = [BOS] + s + [EOS]
        for k in range(1, len(p) - 1):
            x = p[k]
            if x not in vi:
                continue
            for f in ("L:" + p[k - 1], "R:" + p[k + 1]):
                j = feats.setdefault(f, len(feats))
                rows.append(vi[x]); cols.append(j)
    M = np.zeros((len(vocab), len(feats)))
    np.add.at(M, (rows, cols), 1)
    tot = M.sum()
    pr, pc = M.sum(1, keepdims=True) / tot, M.sum(0, keepdims=True) / tot
    with np.errstate(divide="ignore"):
        pmi = np.log((M / tot) / (pr * pc))
    ppmi = np.where(np.isfinite(pmi) & (pmi > 0), pmi, 0)
    U, S, _ = np.linalg.svd(ppmi, full_matrices=False)
    E = U[:, :20] * S[:20]
    E /= np.linalg.norm(E, axis=1, keepdims=True) + 1e-9
    lab = KMeans(n_clusters=K, n_init=20, random_state=0).fit_predict(E)

    # positional profile per sign
    st, en, rel = Counter(), Counter(), defaultdict(list)
    for s in seqs:
        if len(s) < 2:
            continue
        for k, x in enumerate(s):
            st[x] += k == 0; en[x] += k == len(s) - 1; rel[x].append(k / (len(s) - 1))
    known = lambda x: ("opener" if roles.get(x) == 0 else "closer" if roles.get(x) == 2 else  # noqa: E731
                       "numeral" if x in NUMERALS else "end-slot" if x in END_SLOT else "-")
    clusters = []
    print(f"== A1. {K} sign classes from context alone ({len(vocab)} signs used >= {MIN_TOK} times; PPMI of neighbours, SVD 20, k-means) ==")
    for c in range(K):
        mem = [vocab[i] for i in np.flatnonzero(lab == c)]
        n = sum(tok[x] for x in mem)
        prof = dict(signs=len(mem), tokens=n,
                    start=sum(st[x] for x in mem) / n, end=sum(en[x] for x in mem) / n,
                    mean_pos=float(np.mean([p for x in mem for p in rel[x]])) if any(rel[x] for x in mem) else float("nan"),
                    known=dict(Counter(known(x) for x in mem)), top=mem[:12])
        clusters.append(prof)
    for c, p in sorted(enumerate(clusters), key=lambda t: t[1]["mean_pos"]):
        kn = ", ".join(f"{k} {v}" for k, v in p["known"].items() if k != "-")
        print(f"   class {c:2}: {p['signs']:3} signs, {p['tokens']:5} uses | starts {p['start']:.0%} ends {p['end']:.0%} "
              f"mean pos {p['mean_pos']:.2f} | known roles: {kn or 'none'} | {' '.join(p['top'])}")
    out["classes"] = clusters
    cls_of = {vocab[i]: int(lab[i]) for i in range(len(vocab))}

    # motifs
    ng = Counter()
    for s in seqs:
        for n in (2, 3, 4):
            for k in range(len(s) - n + 1):
                ng[tuple(s[k:k + n])] += 1
    N = sum(tok.values())

    def pmi_ng(g):
        return np.log(ng[g] / N) - sum(np.log(tok[x] / N) for x in g)
    motifs = [(g, ng[g], pmi_ng(g)) for g in ng if ng[g] >= 8 and len(g) >= 3]
    motifs.sort(key=lambda t: -t[1])
    print("\n== A2. Recurring motifs of 3-4 signs (>= 8 uses) ==")
    print("   " + "; ".join(f"{' '.join(g)} ×{n}" for g, n, _ in motifs[:20]))
    out["motifs"] = [dict(motif=" ".join(g), n=n, pmi=float(p)) for g, n, p in motifs[:40]]

    # templates of whole inscriptions in class letters
    letters = "ABCDEFGHIJKL"
    tpl = Counter("".join(letters[cls_of[x]] if x in cls_of else "." for x in s) for s in seqs)
    cov = sum(n for t, n in tpl.most_common(20)) / len(seqs)
    print(f"\n== A3. Whole inscriptions as class templates: {len(tpl)} distinct among {len(seqs)} texts; "
          f"top 20 cover {cov:.0%} ==")
    print("   " + "; ".join(f"{t} ×{n}" for t, n in tpl.most_common(15)))
    out["templates"] = dict(distinct=len(tpl), top20_cover=cov, top=tpl.most_common(30), letters={letters[c]: c for c in range(K)})
    return cls_of


def part_b(seqs, roles, out):
    idx = RNG.permutation(len(seqs))
    folds = np.array_split(idx, 5)
    res = defaultdict(lambda: defaultdict(lambda: [0, 0, 0, 0.0]))  # model -> slot -> [n, top1, top5, logp]

    def slot(s, k):
        if k == 0:
            return "1 first sign"
        if k == len(s) - 1:
            return "6 last sign" if roles.get(s[k]) != 2 else "5 closer (last)"
        if roles.get(s[k - 1]) == 0:
            return "2 right after an opener"
        if k + 1 < len(s) and roles.get(s[k + 1]) == 2 and all(roles.get(y) == 2 for y in s[k + 1:]):
            return "4 just before the closer"
        return "3 middle"

    for f in range(5):
        test = set(folds[f].tolist())
        train = [seqs[i] for i in range(len(seqs)) if i not in test]
        uni = Counter(x for s in train for x in s + [EOS])
        V = sorted(set(uni) | {"<unk>"})
        big = defaultdict(Counter)
        for s in train:
            p = [BOS] + s + [EOS]
            for a, b in zip(p, p[1:]):
                big[a][b] += 1
        tot = sum(uni.values())
        pu = {x: (uni[x] + 0.5) / (tot + 0.5 * len(V)) for x in V}
        uni_rank = sorted(V, key=lambda x: -pu[x])

        def p_next(a):
            c = big.get(a, Counter()); n = sum(c.values()); lam = n / (n + 5)
            return lambda x: lam * c[x] / n + (1 - lam) * pu[x] if n else pu[x]

        def p_prev_given(x, b):  # P(b | x)
            c = big.get(x, Counter()); n = sum(c.values()); lam = n / (n + 5)
            return lam * c[b] / n + (1 - lam) * pu.get(b, pu["<unk>"]) if n else pu.get(b, pu["<unk>"])
        for i in folds[f]:
            s = seqs[i]
            p = [BOS] + s + [EOS]
            for k in range(len(s)):
                truth = s[k] if s[k] in pu else "<unk>"
                sl = slot(s, k)
                pn = p_next(p[k])
                cands = [x for x in V if x != EOS]
                sc_next = np.array([pn(x) for x in cands])
                sc_two = sc_next * np.array([p_prev_given(x, p[k + 2]) for x in cands])
                sc_uni = np.array([pu[x] for x in cands])
                for name, sc in [("frequency only", sc_uni), ("bigram (next sign)", sc_next), ("two-sided (masked sign)", sc_two)]:
                    order = np.argsort(-sc)
                    top = [cands[j] for j in order[:5]]
                    pr = sc[cands.index(truth)] / sc.sum()
                    for key in (sl, "ALL"):
                        r = res[name][key]
                        r[0] += 1; r[1] += top[0] == truth; r[2] += truth in top; r[3] += np.log2(pr)
    print("\n== B. Predicting a hidden sign: five-fold cross-validation inside the exploration split ==")
    table = {}
    for name in res:
        table[name] = {}
        for key in sorted(res[name]):
            n, t1, t5, lp = res[name][key]
            table[name][key] = dict(n=n, top1=t1 / n, top5=t5 / n, perplexity=float(2 ** (-lp / n)))
    slots = sorted(table["frequency only"])
    print(f"   {'position':28}" + "".join(f"{m:>30}" for m in table))
    for sl in slots:
        print(f"   {sl:28}" + "".join(f"   top1 {table[m][sl]['top1']:5.0%} top5 {table[m][sl]['top5']:5.0%} ppl {table[m][sl]['perplexity']:5.0f}" for m in table)
              + f"   (n {table['frequency only'][sl]['n']})")
    out["prediction"] = table


def main():
    df = load()
    seqs = [list(s) for s in df["signs"] if len(s)]
    roles, _ = assign(seqs)
    out = {}
    part_a(seqs, roles, out)
    part_b(seqs, roles, out)
    (ROOT / "results" / "open_patterns.json").write_text(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
