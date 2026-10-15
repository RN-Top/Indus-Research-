"""Does the slot order survive in an independent transcription? (EXPLORATORY.)

Applies the frozen role lists from drafts/H-skeleton-transfer.DRAFT.json
(learned from Mohenjo-daro exploration texts in the G-number corpus) to the
CISI transcription of Mohenjo-daro seals, translated through the confident
G->P crosswalk.

Holdout protection: CISI seals are dropped if they are in CISI's own holdout
split OR if the same physical seal (CISI number) is in the G-corpus holdout.

    python scripts/cisi_skeleton_check.py
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from indus_workbench import controls, data  # noqa: E402
from indus_workbench.hypotheses import _in_order, _scorable  # noqa: E402

RNG = np.random.default_rng(99)


def main():
    draft = json.loads((ROOT / "drafts" / "H-skeleton-transfer.DRAFT.json").read_text())
    p = draft["params"]
    x = pd.read_csv(ROOT / "data" / "crosswalk_G_to_P.csv")
    x = x[x["confident"]].set_index("g_sign")["p_sign"].to_dict()

    ranks_p, unmapped = {}, {0: [], 1: [], 2: []}
    for rank, lst in ((1, p["middle"]), (0, p["openers"]), (2, p["closers"])):
        for g in lst:
            if g in x:
                ranks_p[x[g]] = rank
            else:
                unmapped[rank].append(g)
    names = {0: "openers", 1: "middle", 2: "closers"}
    for r in (0, 2):
        print(f"{names[r]}: {sum(1 for v in ranks_p.values() if v == r)} mapped to CISI signs; "
              f"unmapped (no confident crosswalk): {unmapped[r]}")

    # G-corpus holdout CISI numbers
    w = pd.read_csv(ROOT / "data" / "indus_website_real_corpus.csv", dtype=str, keep_default_na=False)
    rawg, _ = data.load_raw("indus_website")
    g = data.build_corpus(rawg, "indus_website", drop_damaged=False, drop_unidentified=False)
    split_of = dict(zip(g.df["text_id"], g.df["split"]))
    hold_nums = {r.cisi_number for r in w.itertuples() if split_of.get(r.inscription_id) == "holdout"}

    raw, _ = data.load_raw("cisi_base")
    c = data.build_corpus(raw, "cisi_base", collapse_variants=True).df
    c["num"] = c["text_id"].str.replace(r"[A-Za-z]$", "", regex=True)
    n0 = len(c)
    c = c[(c["split"] == "explore") & (~c["num"].isin(hold_nums))]
    print(f"CISI seals after default cleaning: {n0}; kept after removing both holdouts: {len(c)}")

    seqs = [s for s in c["signs"] if _scorable(s, ranks_p)]
    obs = float(np.mean([_in_order(s, ranks_p) for s in seqs]))
    null = np.array([np.mean([_in_order(s, ranks_p) for s in controls.shuffle_within_texts(seqs, RNG)])
                     for _ in range(2000)])
    pval = float((1 + (null >= obs).sum()) / (len(null) + 1))
    print(f"scorable seals: {len(seqs)}; in slot order {obs:.1%}; shuffled {null.mean():.1%} "
          f"(95th pct {np.quantile(null, .95):.1%}); p={pval:.4f}")
    out = dict(mapped_roles={names[k]: sorted(s for s, v in ranks_p.items() if v == k) for k in (0, 1, 2)},
               unmapped=unmapped, cisi_kept=len(c), scorable=len(seqs), observed=obs,
               shuffled=float(null.mean()), shuffled95=float(np.quantile(null, .95)), p=pval)
    (ROOT / "results" / "cisi_skeleton_check.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
