"""Lothal sealings as a network of seal holders (scouting, descriptive).
Each Lothal sealing (CISI L-number) may carry 1-5 seal impressions; the merged ICIT corpus (paragorth) lists each
impression's text as a separate entry under the same CISI number. Closure types and find context from Frenez & Tosi
2005, Table 1 (paragorth derived/lothal-sealings-frenez-tosi2005.json; W = warehouse, W1 = same seals as W).
Nodes = distinct seal texts (identical impressions = one seal); edges = stamped together on one sealing."""
import json, sys
from collections import Counter, defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
d = json.load(open(ROOT / "data/icit_merged_paragorth/merged-corpus-canonical.json"))
FT = {r[0]: r for r in json.load(open(Path.home() / "ext2/pg/data/derived/lothal-sealings-frenez-tosi2005.json"))["rows"]}
sl = defaultdict(list)
for x in d:
    if x["site"] == "Lothal" and x["cisi"].startswith("L-") and x["type"].startswith("TAG"):
        sl[x["cisi"]].append(" ".join(f"G{s}" for s in x["seq"]))
uses = defaultdict(set); co = defaultdict(Counter); types = defaultdict(Counter); ctx = defaultdict(Counter)
for L, seals in sl.items():
    S = sorted(set(seals))
    for s in S:
        uses[s].add(L)
        if L in FT: types[s][FT[L][2]] += 1; ctx[s][FT[L][3]] += 1
        for t in S:
            if t != s: co[s][t] += 1
out = [f"Lothal sealings in the merged corpus: {len(sl)}; distinct seal texts: {len(uses)}; "
       f"sealings with 2+ seals: {sum(len(set(v)) > 1 for v in sl.values())}", "",
       "seal text | sealings | distinct co-sealers | closure types (Frenez & Tosi) | contexts"]
rank = sorted(uses, key=lambda s: (-len(uses[s]), -len(co[s])))
for s in rank[:12]:
    out.append(f"{s:42} {len(uses[s]):3}  {len(co[s]):2}  {dict(types[s])}  {dict(ctx[s])}")
T = "G705 G500 G741 G1 G55 G220 G740 G90"
out += ["", f"The twelve seal ({T}):", "  sealings: " + ", ".join(sorted(uses[T], key=lambda x: int(x[2:]))),
        "  co-sealers: " + "; ".join(f"[{k}] x{v}" for k, v in co[T].most_common())]
for L in sorted(uses[T], key=lambda x: int(x[2:])):
    if len(set(sl[L])) > 1: out.append(f"    {L}: {FT.get(L, ['', '', '?', '?'])[2]}/{FT.get(L, ['', '', '', '?'])[3]}  with " + " + ".join(s for s in set(sl[L]) if s != T))
g55 = [s for s in uses if "G55" in s.split()]
out.append("  other Lothal seal texts containing G55: " + "; ".join(f"[{s}] on {sorted(uses[s])}" for s in g55 if s != T))
deg = sorted(((len(co[s]), s) for s in uses), reverse=True)[:5]
out.append("\nMost connected seals (distinct co-sealers): " + "; ".join(f"[{s}] {n}" for n, s in deg))
print("\n".join(out)); (ROOT / "results/lothal_cosealing_output.txt").write_text("\n".join(out) + "\n")
