"""Do added marks shift signs in a consistent direction across base signs? (EXPLORATION split only)

Input: a mark annotation CSV (sign, base, marks, confidence, note), made blind to positions from glyph drawings.
For each mark type: every (variant, base) pair where both occur in exploration texts; compare the variant's
position profile with its base's:
  start share (first sign of the text), end-region share (text-final or right before the closers),
  mean relative position (0 = first, 1 = last; texts of 2+ signs).
Consistency across bases: in how many pairs does the variant move later (or earlier)? Two-sided sign test.

    python scripts/marks_profile.py <marks.csv>
"""
import csv, json, sys
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
from scipy.stats import binomtest
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "scripts"))
from functional_slots import load  # noqa: E402

def main(path):
    H = json.load(open(ROOT / "hypotheses/H-2026-10-16-51b7445b.json"))["params"]; C = set(H["closers"])
    tok, st, endr, rel = Counter(), Counter(), Counter(), defaultdict(list)
    for s in load()["signs"]:
        s = list(s)
        if len(s) < 2: continue
        j = len(s)
        while j > 0 and s[j - 1] in C: j -= 1
        for i, x in enumerate(s):
            tok[x] += 1; st[x] += i == 0
            endr[x] += (i == len(s) - 1) or (i == j - 1 and j < len(s))
            rel[x].append(i / (len(s) - 1))
    rows = list(csv.DictReader(open(path)))
    by_mark = defaultdict(list)
    for r in rows:
        b = r["base"].strip()
        if not b or b == "self" or b not in tok or r["sign"] not in tok: continue
        for m in [m.strip() for m in r["marks"].split(";") if m.strip()]:
            key = "top_strokes" if m.startswith("top_strokes") else ("side_strokes" if m.startswith("side_strokes") else m)
            by_mark[key].append((r["sign"], b))
    out = {}
    for m, pairs in sorted(by_mark.items(), key=lambda kv: -len(kv[1])):
        d = []
        for v, b in pairs:
            d.append(dict(variant=v, base=b, n_v=tok[v], n_b=tok[b], end_v=endr[v] / tok[v], end_b=endr[b] / tok[b],
                          start_v=st[v] / tok[v], start_b=st[b] / tok[b], pos_v=float(np.mean(rel[v])), pos_b=float(np.mean(rel[b]))))
        later = sum(x["pos_v"] > x["pos_b"] for x in d); earlier = sum(x["pos_v"] < x["pos_b"] for x in d)
        p = binomtest(later, later + earlier).pvalue if later + earlier else float("nan")
        tv = sum(x["n_v"] for x in d)
        pooled_end_v = sum(x["end_v"] * x["n_v"] for x in d) / tv
        pooled_end_b = sum(x["end_b"] * x["n_v"] for x in d) / tv   # base weighted by variant count
        print(f"{m:18} pairs {len(d):3}  later {later:2} / earlier {earlier:2} (sign test p={p:.3f})  "
              f"variant tokens {tv:4}  end-region variant {pooled_end_v:.0%} vs base {pooled_end_b:.0%}")
        out[m] = dict(pairs=d, later=later, earlier=earlier, p=p, end_v=pooled_end_v, end_b=pooled_end_b, variant_tokens=tv)
    (ROOT / "results" / "marks_profile.json").write_text(json.dumps(out, indent=1))

if __name__ == "__main__":
    main(sys.argv[1])
