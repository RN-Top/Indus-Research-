"""Where else do the texts on unit tablets (the side opposite 'N long strokes + G700') occur? (scouting)
If they name recipients or offices, they should recur as whole texts or segments on seals; if they name
commodities, they might recur on pots/tags. Compare with a control: texts on Harappa tablets WITHOUT a unit side."""
import json, collections
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
d = json.load(open(ROOT / "data/icit_merged_paragorth/merged-corpus-canonical.json"))
LONG = {31,32,33,34,35,36}
by = collections.defaultdict(list)
for x in d:
    if x["cisi"] not in ("", "-"): by[x["cisi"]].append(x)
def is_unit(s): return len(s) == 2 and ((s[1] == 700 and s[0] in LONG) or (s[0] == 700 and s[1] in LONG))
chit, ctrl = [], []
for cisi, xs in by.items():
    if not str(xs[0]["type"]).startswith("TAB") or xs[0]["site"] != "Harappa": continue
    u = [x for x in xs if is_unit(x["seq"])]; o = [tuple(x["seq"]) for x in xs if not is_unit(x["seq"]) and len(x["seq"]) >= 2]
    (chit if u else ctrl).extend(o)
def kind(t):
    t = str(t)
    return "seal" if t.startswith("SEAL") else "pot" if t.startswith("PO") else "tag" if t.startswith("TAG") else "tablet" if t.startswith("TAB") else "other"
whole = collections.defaultdict(collections.Counter)
for x in d:
    if len(x["seq"]) >= 2: whole[tuple(x["seq"])][kind(x["type"])] += 1
def contained(t, s): return any(tuple(s[i:i+len(t)]) == t for i in range(len(s)-len(t)+1))
seals = [x["seq"] for x in d if kind(x["type"]) == "seal"]
def profile(texts, label):
    U = set(texts)
    on_seal_whole = sum(1 for t in U if whole[t]["seal"] > 0)
    on_seal_part = sum(1 for t in U if any(contained(t, s) for s in seals))
    print(f"{label}: {len(U)} distinct texts; whole text also a seal text: {on_seal_whole} ({on_seal_whole/len(U):.0%}); inside some seal text: {on_seal_part} ({on_seal_part/len(U):.0%})")
    return U
C = profile(chit, "unit-tablet texts"); K = profile(ctrl, "other Harappa tablet texts (control)")
print("\nunit-tablet texts found inside seal texts (examples):")
n = 0
for t in sorted(C, key=lambda t: -sum(1 for s in seals if contained(t, s))):
    k = sum(1 for s in seals if contained(t, s))
    if k and n < 12: print("  ", " ".join(f"G{v}" for v in t), "-> in", k, "seal texts"); n += 1
# sign profile: share of tokens that are 'closer' signs vs others
from collections import Counter
ct = Counter(v for t in C for v in t); kt = Counter(v for t in K for v in t)
print("\ncommonest signs on unit-tablet texts:", [(f"G{a}", b) for a, b in ct.most_common(10)])
print("commonest signs on control tablet texts:", [(f"G{a}", b) for a, b in kt.most_common(10)])
