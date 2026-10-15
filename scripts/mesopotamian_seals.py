"""Function theory, second comparison: Mesopotamian seal legends. (EXPLORATORY.)

Mesopotamian seal inscriptions are labels whose meaning is known, typically
"[name] / [title] / son of [name2] / servant of [god or king]". Does the same
blind role rule used for the Indus script (results/functional_by_site.md D.1)
find openers and closers there, and do the slot profiles look like the Indus ones?

Data: CDLI bulk dump (github.com/cdli-gh/data, August 2022): transliterations
(ATF) and catalogue. Reused under CDLI terms with citation; NOT copied into this
repository. Pass the folder holding cdliatf_unblocked.atf and cdli_cat.csv.

Units: a token is one transliterated word (Indus signs are thought to be largely
word-level signs, so words are the closest unit; this is an assumption).
Legends: '@seal N' sections on tablets (impressions) plus inscribed seal objects,
from the Old Akkadian to Old Babylonian periods (about 2340-1600 BCE, overlapping
the Mature Harappan). Identical legends are reduced to one, as for Indus.
A 20% holdout (hash of the legend text, salt 'mes-seal-holdout-v1') is never read.

    python scripts/mesopotamian_seals.py /path/to/cdli_data
"""

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from functional_skeleton import RULE  # noqa: E402
from proto_elamite_skeleton import assign, conformance  # noqa: E402  (same rule and test)

SALT = "mes-seal-holdout-v1"
PERIODS = ("Old Akkadian", "Lagash II", "Ur III", "Early Old Babylonian", "Old Babylonian")
NUM = re.compile(r"^\d+(\(\w+\))?$|^\d+/\d+")


def norm(w):
    w = re.sub(r"[#?!*\[\]<>_]", "", w).lower()
    # broken words (any '...' or an illegible 'x' component) are dropped, like damaged Indus signs
    if not w or "..." in w or re.search(r"(^|[-{}.])x([-{}.]|$)", w):
        return None
    if NUM.match(w):
        return "NUM"
    return w


def parse(atf_path):
    """Yield (P-number, kind, list of lines) for each seal legend."""
    pnum, in_seal, lines, obj_seal_text = None, False, [], {}
    cur_text = []
    with open(atf_path, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            s = raw.strip()
            if s.startswith("&P"):
                if pnum and in_seal and lines:
                    yield pnum, "impression", lines
                if pnum and cur_text:
                    obj_seal_text[pnum] = cur_text
                pnum, in_seal, lines, cur_text = s[1:8], False, [], []
                continue
            if s.startswith("@"):
                if in_seal and lines:
                    yield pnum, "impression", lines
                in_seal, lines = s.startswith("@seal"), []
                continue
            m = re.match(r"^\d+'?\.\s+(.*)$", s)
            if not m:
                continue
            words = [w for w in (norm(x) for x in m.group(1).split()) if w]
            if not words:
                continue
            if in_seal:
                lines.append(words)
            cur_text.append(words)
        if pnum and in_seal and lines:
            yield pnum, "impression", lines
        if pnum and cur_text:
            obj_seal_text[pnum] = cur_text
    for p, t in obj_seal_text.items():
        yield p, "object", t


def main(folder):
    folder = Path(folder)
    cat = pd.read_csv(folder / "cdli_cat.csv", usecols=["id_text", "period", "object_type", "provenience"],
                      dtype=str, low_memory=False)
    cat["P"] = "P" + cat["id_text"].str.zfill(6)
    info = cat.set_index("P")[["period", "object_type", "provenience"]].to_dict("index")

    legends = {}
    n_imp = n_obj = 0
    for p, kind, lines in parse(folder / "cdliatf_unblocked.atf"):
        meta = info.get(p, {})
        period = str(meta.get("period", ""))
        if not period.startswith(PERIODS):
            continue
        if kind == "object" and "seal" not in str(meta.get("object_type", "")):
            continue
        toks = [w for ln in lines for w in ln]
        if len(toks) < 2:
            continue
        key = " ".join(toks)
        n_imp += kind == "impression"
        n_obj += kind == "object"
        legends.setdefault(key, dict(toks=toks, lines=lines, period=period.split(" (")[0], kind=kind, p=p))
    leg = list(legends.values())
    for l in leg:
        h = int(hashlib.sha256(f"{SALT}:{' '.join(l['toks'])}".encode()).hexdigest(), 16)
        l["split"] = "holdout" if h % 100 < 20 else "explore"
    ex = [l for l in leg if l["split"] == "explore"]
    print(f"seal legends found (Old Akkadian to Old Babylonian): {n_imp} impressions + {n_obj} seal objects; "
          f"{len(leg)} distinct; exploration {len(ex)}; holdout {len(leg) - len(ex)} (not read)")
    print("   by period (exploration):", dict(Counter(l["period"] for l in ex).most_common()))
    L = [len(l["toks"]) for l in ex]
    print(f"   words per legend: median {np.median(L):.0f}, mean {np.mean(L):.1f}")
    out = {"rule": RULE, "distinct_legends": len(leg), "explore": len(ex), "median_length": float(np.median(L))}

    seqs = [l["toks"] for l in ex]
    roles, table = assign(seqs)
    print("\n== 1. Roles found by the unchanged Indus rule (words) ==")
    for r in sorted(table, key=lambda r: (r["role"], -r["uses"]))[:30]:
        k = "starts" if r["role"] == "opener" else "ends"
        print(f"   {r['role']:6} {r['sign']:24} uses {r['uses']:5}  {k} {r['share']:.0%}  (shuffled {r['shuffled']:.0%})")
    out["roles"] = table

    c = conformance(seqs, roles, n_null=200)
    print(f"\n== 2. Slot order: {c['observed']:.1%} of {c['n']} legends in order; shuffled {c['shuffled']:.1%}; p={c['p']:.4f}")
    out["conformance"] = c

    # 3. Slot profiles, as computed for Indus in functional_meaning.md
    op_f, mid_f, cl_f = Counter(), Counter(), Counter()
    for s in seqs:
        op = [x for x in s if roles.get(x) == 0]
        cl = [x for x in s if roles.get(x) == 2]
        mid = [x for x in s if roles.get(x) not in (0, 2)]
        if op:
            op_f[" ".join(op)] += 1
        if cl:
            cl_f[" ".join(cl)] += 1
        if mid:
            mid_f[" ".join(mid)] += 1

    def prof(c):
        n = sum(c.values())
        return dict(texts=n, distinct=len(c), unique_share=sum(v for v in c.values() if v == 1) / n if n else float("nan"),
                    top=c.most_common(5))
    out["profiles"] = {"opener": prof(op_f), "content": prof(mid_f), "closer": prof(cl_f)}
    print("\n== 3. Slot profiles (Indus for comparison: opener 29 forms, content 86% unique, closer 65 forms) ==")
    for k, v in out["profiles"].items():
        print(f"   {k:8} {v['texts']:5} legends, {v['distinct']:5} different fillers, {v['unique_share']:.0%} of legends have a one-off filler; top {v['top'][:3]}")

    last_num = np.mean([s[-1] == "NUM" for s in seqs])
    print(f"\n== 4. Ends in a number: {last_num:.1%} of legends (Indus 3-5%, Proto-Elamite 80%)")
    out["ends_in_number"] = float(last_num)

    (ROOT / "results" / "mesopotamian_seals.json").write_text(json.dumps(out, indent=1, default=float, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
