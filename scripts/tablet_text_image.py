"""Do other tablet genres (mainly Harappa moulded/incised tablets) show the copper-tablet text->image link?
EXPLORATION split only. Same method as scripts/copper_sets.py: among objects with a specific image label,
pairs that share an exact text -- share of pairs with the same label vs labels permuted (5,000 times).
Pairs from the same object (same text_id, e.g. two sides) are excluded."""
import json, sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from indus_workbench import data  # noqa: E402
VAGUE = {"unknown", "nan", "", "None", "-", "Othr"}
RNG = np.random.default_rng(20261020)

def agreement(rows, labels):
    groups = defaultdict(list)
    for i, (tid, tx) in enumerate(rows): groups[tx].append(i)
    hit = tot = 0
    for idx in groups.values():
        for i, j in combinations(idx, 2):
            if rows[i][0] == rows[j][0]: continue
            tot += 1; hit += labels[i] == labels[j]
    return (hit / tot if tot else float("nan")), tot

def main():
    raw, _ = data.load_raw("indus_website")
    c = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"),
                          drop_damaged=True, dedupe=False, drop_unidentified=True)
    e = data.explore_only(c).df
    e = e[~e.material.astype(str).str.contains("opper", case=False)]
    out = {}
    for name, sub in [("tablets (all sites, not copper)", e[e.object_type == "tablet"]),
                      ("Harappa tablets", e[(e.object_type == "tablet") & (e.site == "Harappa")]),
                      ("seals (control: seals are not expected to pair text with image)", e[e.object_type == "seal"])]:
        sub = sub[~sub.motif.astype(str).isin(VAGUE)]
        rows = [(t, " ".join(s)) for t, s in zip(sub.text_id, sub.signs)]
        labels = list(sub.motif.astype(str))
        obs, pairs = agreement(rows, labels)
        null = [agreement(rows, list(RNG.permutation(labels)))[0] for _ in range(5000)]
        p = (1 + sum(n >= obs for n in null)) / 5001
        print(f"{name}: objects with a specific label {len(sub)}; same-text pairs (different objects) {pairs}; "
              f"same label {obs:.0%} vs {np.nanmean(null):.0%} shuffled; p = {p:.4f}")
        out[name] = dict(objects=len(sub), pairs=pairs, obs=obs, null=float(np.nanmean(null)), p=p)
        if "Harappa" in name:
            sets = defaultdict(Counter)
            for (t, tx), lb in zip(rows, labels): sets[tx][lb] += 1
            big = sorted(((tx, c) for tx, c in sets.items() if sum(c.values()) >= 3), key=lambda kv: -sum(kv[1].values()))
            for tx, c in big[:20]: print(f"   x{sum(c.values()):<3} {tx:40} {dict(c)}")
    (ROOT / "results" / "tablet_text_image.json").write_text(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
