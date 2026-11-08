"""ICIT-based Indus structural profile (EXPLORATORY).

ICIT is metadata-only under RULES amendment item 4. This script computes the four
P20 structural features from ICIT sign sequences, as a labelled reference profile.
Its output is not a reading source and does not enter the corpus or the registry.
Sign tokens are the 'seq' field (integer sign ids), texts of 3-8 units.
"""
import json
import sys
from datetime import date

sys.path.insert(0, "scripts")
from structure_battery import features, load_corpus  # noqa: E402

SRC = "data/icit_merged_paragorth/merged-corpus-canonical.json"
OUT = "results/icit_indus_profile_2026-11-07.md"
MIN_LEN, MAX_LEN = 3, 8


def texts_from_icit(recs, label):
    out = []
    for r in recs:
        seq = r.get("seq") or []
        if MIN_LEN <= len(seq) <= MAX_LEN:
            out.append([str(s) for s in seq])
    return out


def main():
    recs = json.load(open(SRC, encoding="utf-8"))
    groups = {
        "All ICIT objects": recs,
        "Seals only": [r for r in recs if str(r.get("type", "")).upper().startswith("SEAL")],
        "Mohenjo-daro seals only": [r for r in recs if str(r.get("type", "")).upper().startswith("SEAL")
                                    and r.get("site") == "Mohenjo-daro"],
    }
    lines = [f"# ICIT-based Indus structural profile (exploratory) {date.today().isoformat()}",
             "",
             "**Label: ICIT-based.** ICIT is metadata-only under RULES amendment item 4. These "
             "values describe ICIT's sign sequences; they are not a reading source and are not "
             "in the corpus or the registry. Using ICIT as the structural baseline needs a dated "
             "amendment to RULES before any result counts for the battery.",
             "",
             f"Source: `{SRC}`. Texts of {MIN_LEN}-{MAX_LEN} units, sign ids from `seq`.",
             "",
             "| group | texts | F1 first repeat | F2 last repeat | F3 entropy | F4 shared units |",
             "|---|---|---|---|---|---|"]
    for name, rs in groups.items():
        t = texts_from_icit(rs, name)
        f = features(t)
        lines.append(f"| {name} | {len(t)} | " + " | ".join(f"{x:.3f}" for x in f) + " |")
    lines += ["", "Caveat: this profile has no null yet. Compare each comparison language against the "
              "shuffled-Indus null in the battery, once a comparison corpus is checked and has units."]
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
