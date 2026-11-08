"""Pre-registered (2 Nov 2026, before running): the G700 long-stroke effect holds within each
object family. Prediction: in every family with enough texts, a long stroke (G31-G36) is more
often immediately followed by G700 than a short stroke (G1-G7) is, and the difference is in the
same direction. Falsified if any large family shows no difference or the opposite direction.
Test: Fisher exact, one-sided, per family; long vs short stroke followed by G700.
"""
import json, ast, pathlib
from scipy.stats import fisher_exact
ROOT = pathlib.Path(__file__).resolve().parent.parent
rows = json.load(open(ROOT / "data/icit_merged_paragorth/merged-corpus-canonical.json"))
LONG = {f"{i}" for i in range(31, 37)}
SHORT = {f"{i}" for i in range(1, 8)}
def fam(t):
    if t.startswith("SEAL"): return "SEAL"
    if t in ("TAB:B", "TAB:I"): return t
    if t.startswith("POT"): return "POT"
    return None
stats = {}
for r in rows:
    f = fam(r["type"])
    if not f: continue
    s = r["seq_strong"]; s = ast.literal_eval(s) if isinstance(s, str) else s
    s = [str(x) for x in s]
    d = stats.setdefault(f, {"long": [0, 0], "short": [0, 0]})
    for a, b in zip(s, s[1:]):
        if a in LONG:
            d["long"][0] += 1; d["long"][1] += (b == "700")
        elif a in SHORT:
            d["short"][0] += 1; d["short"][1] += (b == "700")
out = {}
for f, d in stats.items():
    lt, lk = d["long"]; st, sk = d["short"]
    if lt == 0 or st == 0: out[f] = "too few"; continue
    odds, p = fisher_exact([[lk, lt - lk], [sk, st - sk]], alternative="greater")
    out[f] = {"long_then_G700": f"{lk}/{lt}", "short_then_G700": f"{sk}/{st}",
              "odds_ratio": round(odds, 1), "p_one_sided": float(f"{p:.2e}")}
print(json.dumps(out, indent=2))
