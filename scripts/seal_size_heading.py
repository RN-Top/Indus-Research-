"""Seal size vs heading, controlling for text length (EXPLORATION split only).
Statistic: within each text length (2-7+), Spearman correlation of seal face area with 'starts with an opener',
averaged over lengths (weighted by count). Null: heading labels permuted within each length, 5,000 times."""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd
from scipy.stats import spearmanr
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "scripts"))
from functional_slots import load  # noqa: E402

def main():
    d = load().merge(pd.read_csv(ROOT / "data/text_metadata.csv")[["text_id", "width_mm", "height_mm"]], on="text_id", how="left")
    s = d[(d.object_type == "seal") & d.width_mm.notna() & d.height_mm.notna()].copy()
    O = set(json.load(open(ROOT / "hypotheses/H-2026-10-16-51b7445b.json"))["params"]["openers"])
    s["area"] = s.width_mm * s.height_mm; s["L"] = s.signs.map(len).clip(upper=7)
    s["head"] = s.signs.map(lambda x: x[0] in O).astype(int); s = s[s.L >= 2]
    groups = [g for _, g in s.groupby("L") if g["head"].nunique() > 1]
    def stat(heads):
        tot = w = 0
        for g, h in zip(groups, heads):
            r = spearmanr(g.area, h).statistic; tot += r * len(g); w += len(g)
        return tot / w
    obs = stat([g["head"].values for g in groups])
    rng = np.random.default_rng(20261020)
    null = [stat([rng.permutation(g["head"].values) for g in groups]) for _ in range(5000)]
    p = (1 + sum(n >= obs for n in null)) / 5001
    print(f"Seals with size: {len(s)}; length-controlled size-heading correlation {obs:.3f}; null mean {np.mean(null):.3f}; one-sided p = {p:.4f}")
    for L, g in s.groupby("L"):
        lo, hi = g.area.quantile([.5]).iloc[0], None
        print(f"   length {L}: n {len(g)}, heading share small half {g[g.area<=lo]['head'].mean():.0%}, large half {g[g.area>lo]['head'].mean():.0%}")
    (ROOT / "results" / "seal_size_heading.json").write_text(json.dumps(dict(obs=obs, null=float(np.mean(null)), p=p, n=len(s))))

if __name__ == "__main__":
    main()
