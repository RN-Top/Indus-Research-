"""Which numeral signs act like counts and which like words? Scouting, EXPLORATION split only.
Follow-up to G55 (g55_closer_2026-10-26.md). For every sign in number_system.VAL with 10+ uses (distinct texts,
incomplete kept): share of uses whose next sign is a content (middle) sign = 'count-like', next is a closer,
next is another numeral, and the text edge. A numeral that rarely precedes a content sign is a candidate word."""
import sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
from indus_workbench import data  # noqa: E402
from functional_skeleton import assign  # noqa: E402
from number_system import VAL  # noqa: E402
raw, _ = data.load_raw("indus_website"); md = data.load_metadata("indus_website")
comp = data.explore_only(data.build_corpus(raw, "indus_website", drop_damaged=True, metadata=md)).df
roles, _ = assign([list(s) for s in comp.signs])
full = data.explore_only(data.build_corpus(raw, "indus_website", drop_damaged=False, metadata=md)).df
seqs = list({tuple(s) for s in full.signs})
def nxt(x): return "edge" if x is None else "numeral" if x in VAL else {0: "opener", 1: "middle", 2: "closer"}.get(roles.get(x), "other")
rows = []
for g in VAL:
    c = Counter(); top = Counter()
    for s in seqs:
        for k, x in enumerate(s):
            if x == g:
                y = s[k + 1] if k + 1 < len(s) else None; c[nxt(y)] += 1; top[y] += 1
    n = sum(c.values())
    if n >= 10: rows.append((c["middle"] / n, g, VAL[g], n, c, top.most_common(3)))
out = ["sign value uses  ->content ->closer ->numeral ->edge  commonest next"]
for m, g, v, n, c, t in sorted(rows):
    out.append(f"{g:5} {v:3} {n:5}  {m:.2f}  {c['closer']/n:.2f}  {c['numeral']/n:.2f}  {c['edge']/n:.2f}  {t}")
print("\n".join(out)); (ROOT / "results/numeral_word_scouting_output.txt").write_text("\n".join(out) + "\n")
