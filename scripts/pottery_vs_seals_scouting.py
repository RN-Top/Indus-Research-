"""Pottery inscriptions vs seal texts (scouting, descriptive).

Data: paragorth merged ICIT corpus (MIT), which holds 543 pottery inscriptions. The project corpus has only 59.
POT:T:g = graffito (scratched), POT:T:s = stamped, POT:T:p = third pottery code (meaning not confirmed).
Question (Nath 2014: scratched marks on pot bellies 'may be the owner's name'):
do multi-sign pottery texts look like the name part of a seal text, i.e. the seal vocabulary without the seal formula?
Measures, for texts of 2+ signs, against seals (SEAL:*):
  - share ending in one of the 5 commonest seal-final signs ("seal closers");
  - share starting with one of the 5 commonest seal-initial signs ("seal openers");
  - share of tokens that are numerals (G1-G35 stroke signs, as in the project);
  - share of pottery sign types also used on seals.
Seq order: 'seq' as stored (reading order as given by paragorth canonical).
"""
import json, collections, random
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
d = json.load(open(ROOT / "data/icit_merged_paragorth/merged-corpus-canonical.json"))
NUM = set(range(1, 36))
def grp(x):
    t = str(x["type"])
    if t.startswith("SEAL"): return "seal"
    if t.startswith("POT:T:g"): return "pot graffito"
    if t.startswith("POT:T:s") or t.startswith("POT:T:S"): return "pot stamped"
    if t.startswith("POT:T:p"): return "pot (p)"
    if t.startswith("TAB"): return "tablet"
    return None
G = collections.defaultdict(list)
for x in d:
    g = grp(x)
    if g and len(x["seq"]) >= 2: G[g].append(x["seq"])
fin = collections.Counter(s[-1] for s in G["seal"]); ini = collections.Counter(s[0] for s in G["seal"])
CL = {k for k, _ in fin.most_common(5)}; OP = {k for k, _ in ini.most_common(5)}
seal_types = {t for s in G["seal"] for t in s}
print("seal closers (top-5 final):", sorted(CL), " seal openers (top-5 initial):", sorted(OP))
print(f"{'group':14s} {'n':>5s} {'mean len':>8s} {'ends in closer':>15s} {'starts w/ opener':>17s} {'numeral tokens':>15s} {'types on seals':>15s}")
rng = random.Random(1)
for g in ["seal", "tablet", "pot stamped", "pot graffito", "pot (p)"]:
    S = G[g]
    if not S: continue
    n = len(S); toks = [t for s in S for t in s]; types = set(toks)
    print(f"{g:14s} {n:5d} {sum(map(len,S))/n:8.2f} {sum(s[-1] in CL for s in S)/n:15.0%} {sum(s[0] in OP for s in S)/n:17.0%} "
          f"{sum(t in NUM for t in toks)/len(toks):15.0%} {len(types & seal_types)/len(types):15.0%}")
# commonest multi-sign graffiti sequences
print("\ncommonest graffito texts (2+ signs):", collections.Counter(tuple(s) for s in G["pot graffito"]).most_common(10))
print("commonest stamped texts:", collections.Counter(tuple(s) for s in G["pot stamped"]).most_common(8))

print("\nLength-matched (texts of exactly 2 and 3 signs):")
for L in (2, 3):
    for g in ["seal", "tablet", "pot graffito", "pot stamped"]:
        S = [s for s in G[g] if len(s) == L]
        if len(S) < 5: continue
        toks = [t for s in S for t in s]
        print(f"  len {L} {g:13s} n {len(S):4d}  ends in closer {sum(s[-1] in CL for s in S)/len(S):4.0%}  "
              f"starts w/ opener {sum(s[0] in OP for s in S)/len(S):4.0%}  numeral tokens {sum(t in NUM for t in toks)/len(toks):4.0%}")
# Fisher test: graffito vs seal, closer-final, pooled over length 2-3 with Mantel-Haenszel
from scipy.stats import fisher_exact
for L in (2, 3):
    a = sum(s[-1] in CL for s in G["pot graffito"] if len(s) == L); b = sum(len(s) == L for s in G["pot graffito"]) - a
    c = sum(s[-1] in CL for s in G["seal"] if len(s) == L); e = sum(len(s) == L for s in G["seal"]) - c
    print(f"  len {L}: graffito closer {a}/{a+b} vs seal {c}/{c+e}, Fisher p = {fisher_exact([[a,b],[c,e]])[1]:.4f}")
