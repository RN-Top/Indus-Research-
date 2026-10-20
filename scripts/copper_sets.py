"""Copper tablets as a text-image key (EXPLORATION split only; holdout copper tablets not read).

1. Group copper tablets into sets of identical texts and list each set's image (motif).
2. Is the text -> image mapping more fixed than chance? (same-text pairs share a motif vs motif labels permuted)
3. Which signs are shared across images (formula) and which are confined to one image (candidate names)?
"""
import json, sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
from indus_workbench import data  # noqa: E402

VAGUE = {"Othr", "unknown", "nan", "", "-", "None"}
RNG = np.random.default_rng(20261020)


def main():
    raw, _ = data.load_raw("indus_website")
    a = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"),
                          drop_damaged=False, dedupe=False, drop_unidentified=False).df
    cu = a[a.material.astype(str).str.contains("opper", case=False) & (a.split == "explore")].copy()
    cu["text"] = cu.signs.map(" ".join); cu["motif"] = cu.motif.astype(str)
    sets = cu.groupby("text").agg(n=("text_id", "size"), motifs=("motif", lambda x: dict(Counter(x))),
                                  refs=("source_ref", lambda x: sorted(set(map(str, x)))[:6])).sort_values("n", ascending=False)
    print(f"Copper objects (exploration): {len(cu)}; distinct texts: {len(sets)}; texts seen 2+ times: {(sets.n >= 2).sum()}")
    print("\n1. Sets of identical texts (n >= 2):")
    for t, r in sets[sets.n >= 2].iterrows():
        print(f"   x{r.n:<3} {t:45} {r.motifs}  {r.refs}")

    # 2. determinism on specific motifs
    sp = cu[~cu.motif.isin(VAGUE)].reset_index(drop=True)
    def same_text_agreement(motifs):
        hit = tot = 0
        for _, g in sp.groupby("text").groups.items():
            idx = list(g)
            for i, j in combinations(idx, 2):
                tot += 1; hit += motifs[i] == motifs[j]
        return hit / tot if tot else float("nan"), tot
    obs, pairs = same_text_agreement(list(sp.motif))
    null = [same_text_agreement(list(RNG.permutation(sp.motif)))[0] for _ in range(5000)]
    p = (1 + sum(n >= obs for n in null)) / 5001
    print(f"\n2. Tablets with a specific image: {len(sp)}; same-text pairs: {pairs}; "
          f"share with the same image {obs:.0%} vs {np.mean(null):.0%} if images were shuffled (p = {p:.4f})")

    # 3. formula vs distinctive signs among specific images
    by_motif = defaultdict(list)
    for t, m in zip(sp.text, sp.motif):
        by_motif[m].append(t.split())
    sign_motifs = defaultdict(set)
    for m, texts in by_motif.items():
        for s in texts:
            for x in s: sign_motifs[x].add(m)
    print(f"\n3. Images with specific labels: {dict((m, len(v)) for m, v in by_motif.items())}")
    formula = sorted([x for x, ms in sign_motifs.items() if len(ms) >= 3], key=lambda x: -len(sign_motifs[x]))
    print("   Formula-like signs (on 3+ different images):", [(x, len(sign_motifs[x])) for x in formula])
    out = {"sets": {t: dict(n=int(r.n), motifs=r.motifs, refs=r.refs) for t, r in sets.iterrows()},
           "determinism": dict(obs=obs, null=float(np.mean(null)), p=p, pairs=pairs), "by_image": {}}
    for m, texts in sorted(by_motif.items(), key=lambda kv: -len(kv[1])):
        uniq = sorted({x for s in texts for x in s if sign_motifs[x] == {m}})
        in_all = [x for x in uniq if all(x in s for s in texts)]
        print(f"   {m:8} ({len(texts)} tablets, {len(set(map(tuple, texts)))} distinct texts): only-here signs {uniq}; in every text {in_all}")
        out["by_image"][m] = dict(tablets=len(texts), distinct=len(set(map(tuple, texts))), only_here=uniq, in_all=in_all)
    (ROOT / "results" / "copper_sets.json").write_text(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
