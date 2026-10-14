"""Build a crosswalk from the full corpus's G-numbers to the CISI P-numbers.

Method: the same physical seals appear in both corpora (matched by CISI
catalogue number). Where both transcriptions of a seal have the same number of
signs, signs are paired position by position, in reading order. Each G-number
is mapped to the P-number it pairs with most often.

This is an empirical crosswalk between two independent transcriptions, not an
official concordance. The agreement rate measures how far the two agree; each
row records how many pairings support it so weak mappings can be ignored.

Run:  python scripts/build_crosswalk.py
"""

import collections
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from indus_workbench import data  # noqa: E402

CONFIDENT_MIN_PAIRS = 3
CONFIDENT_MIN_SHARE = 0.9


def main() -> None:
    w = pd.read_csv(ROOT / "data/indus_website_real_corpus.csv", dtype=str, keep_default_na=False)
    c = pd.read_csv(ROOT / "data/cisi_real_corpus_allograph.csv", dtype=str, keep_default_na=False)
    c["num"] = c["inscription_id"].str.replace(r"[A-Za-z]$", "", regex=True)

    by_num: dict[str, list[list[str]]] = {}
    for r in w.itertuples():
        by_num.setdefault(r.cisi_number, []).append(data.orient(r.sign_sequence.split(), r.reading_direction))

    pairs: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    seals_found = seals_aligned = 0
    for r in c.itertuples():
        if r.num not in by_num:
            continue
        seals_found += 1
        p = [data.base_sign(s) for s in data.orient(r.sign_sequence.split(), r.reading_direction)]
        same = [g for g in by_num[r.num] if len(g) == len(p)]
        if len(same) != 1:
            continue
        seals_aligned += 1
        for g_sign, p_sign in zip(same[0], p):
            pairs[g_sign][p_sign] += 1

    rows = []
    for g_sign, counts in pairs.items():
        n = sum(counts.values())
        p_sign, k = counts.most_common(1)[0]
        rows.append({
            "g_sign": g_sign, "p_sign": p_sign, "pairs": n, "share": round(k / n, 3),
            "alternatives": "; ".join(f"{s}×{m}" for s, m in counts.most_common()[1:]),
            "confident": n >= CONFIDENT_MIN_PAIRS and k / n >= CONFIDENT_MIN_SHARE and p_sign != "P000",
        })
    out = pd.DataFrame(rows).sort_values(["pairs", "g_sign"], ascending=[False, True])
    out.to_csv(ROOT / "data/crosswalk_G_to_P.csv", index=False)

    tokens = int(out["pairs"].sum())
    agree = int((out["pairs"] * out["share"]).round().sum())
    print(f"CISI seals found in full corpus: {seals_found} of {len(c)}")
    print(f"Seals with equal-length transcriptions (aligned): {seals_aligned}")
    print(f"Aligned sign pairs: {tokens}; agreement with majority mapping: {agree / tokens:.1%}")
    print(f"G-numbers mapped: {len(out)}; confident: {int(out['confident'].sum())}")


if __name__ == "__main__":
    main()
