"""Profiles of counted item signs (scouting). For each sign often preceded by a short-stroke numeral:
objects it is counted on, the numeral values it takes (mean, spread), whether it ever stands in the measure
slot (next to long strokes / G700), and its seal animals. Merged ICIT corpus."""
import json, collections, statistics as st
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
d = json.load(open(ROOT / "data/icit_merged_paragorth/merged-corpus-canonical.json"))
SV = {1:1,2:2,3:3,4:4,5:5,6:6,7:7,13:3,14:4,15:5,16:6,17:7,18:8,19:9,27:7,28:8,29:9,55:12}
LONG = {31,32,33,34,35,36}
def kind(t):
    t = str(t); return "seal" if t.startswith("SEAL") else "pot" if t.startswith("PO") else "tag" if t.startswith("TAG") else "tablet" if t.startswith("TAB") else "other"
cnt = collections.defaultdict(list); obj = collections.defaultdict(collections.Counter); longn = collections.Counter(); anim = collections.defaultdict(collections.Counter); total = collections.Counter()
for x in d:
    s = x["seq"]; k = kind(x["type"])
    for t in s: total[t] += 1
    for i in range(1, len(s)):
        if s[i-1] in SV and s[i] not in SV and s[i] not in LONG:
            cnt[s[i]].append(SV[s[i-1]]); obj[s[i]][k] += 1
            if k == "seal" and x.get("symbol"): anim[s[i]][x["symbol"].split(":")[0]] += 1
        if s[i-1] in LONG and s[i] not in SV and s[i] not in LONG: longn[s[i]] += 1
print(f"{'sign':6s} {'counted':>7s} {'of uses':>7s} {'mean N':>6s} {'max':>4s} {'values':28s} {'objects':34s} after-long-stroke")
for g, v in sorted(cnt.items(), key=lambda kv: -len(kv[1]))[:14]:
    if len(v) < 10: continue
    vals = collections.Counter(v)
    print(f"G{g:<5d} {len(v):7d} {len(v)/total[g]:7.0%} {st.mean(v):6.1f} {max(v):4d} {str(dict(sorted(vals.items()))):28s} {str(dict(obj[g].most_common(3))):34s} {longn[g]}")
print("\nseal animals with counted signs:", {f"G{g}": dict(anim[g].most_common(3)) for g, v in sorted(cnt.items(), key=lambda kv: -len(kv[1]))[:6]})
