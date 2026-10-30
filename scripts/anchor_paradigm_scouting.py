"""Which signs stand in the same slots as an anchor sign? (scouting, descriptive)
For an anchor sign X: collect every frame (left neighbour, right neighbour) around X in the merged ICIT corpus,
then count which other signs occur in the same frames (paradigm mates). Also exact-text substitutions:
texts identical to an X-text except that X is replaced by one other sign.
Usage: python3 scripts/anchor_paradigm_scouting.py 706 [more anchors]"""
import json, sys, collections
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
d = json.load(open(ROOT / "data/icit_merged_paragorth/merged-corpus-canonical.json"))
S = [(x["seq"], str(x["type"]).split(":")[0], x["site"], x.get("symbol", "")) for x in d if len(x["seq"]) >= 2]
B = "#"
def frames(seq):
    s = [B] + seq + [B]
    for i in range(1, len(s) - 1): yield s[i], (s[i-1], s[i+1])
by_frame = collections.defaultdict(collections.Counter)
for seq, *_ in S:
    for t, f in frames(seq): by_frame[f][t] += 1
texts = collections.Counter(tuple(seq) for seq, *_ in S)
for a in map(int, sys.argv[1:]):
    uses = [(seq, ty, si, sy) for seq, ty, si, sy in S if a in seq]
    fr = collections.Counter(f for seq, *_ in uses for t, f in frames(seq) if t == a)
    mates = collections.Counter()
    for f, n in fr.items():
        for t, m in by_frame[f].items():
            if t != a: mates[t] += m
    subs = collections.Counter()
    for seq, *_ in uses:
        for i, t in enumerate(seq):
            if t != a: continue
            for u in range(1, 1000):
                if u == a: continue
                alt = tuple(seq[:i] + [u] + seq[i+1:])
                if alt in texts: subs[(u, " ".join(f"G{v}" for v in seq))] += texts[alt]
    print(f"\n=== G{a}: {len(uses)} texts; objects {dict(collections.Counter(ty for _, ty, _, _ in uses))}")
    print("  commonest frames (left, right):", [(f"G{l}" if l != B else "START", f"G{r}" if r != B else "END", n) for (l, r), n in fr.most_common(8)])
    print("  paradigm mates (same frames):", [(f"G{t}", n) for t, n in mates.most_common(12)])
    print("  exact one-sign substitutions:", [(f"G{u}", ctx, n) for (u, ctx), n in subs.most_common(12)])
    print("  animals on seals:", dict(collections.Counter(sy for _, ty, _, sy in uses if ty == "SEAL")))
