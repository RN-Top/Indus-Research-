"""Transcription robustness: rerun the supported internal confirmatory tests on Mahadevan's independent corpus (IM77).

Usage: python3 scripts/im77_robustness.py <im77_corpus_lines.csv> <bridge_extended.json> [--no-doubtful]
Sources (not copied here): github.com/paragorth/Indus- data/im77 (exported from indusscript.in) and
data/derived/bridge_extended.json (an unvalidated Wells/ICIT -> Mahadevan sign bridge, 145 signs).
This is NOT a confirmatory test: IM77 covers largely the same objects as ICIT, including the exploration split.
It asks only whether each result survives a different scholar's reading of the signs. Signs without a bridge entry
are dropped from the parameter lists (coverage is reported); a G sign mapped to several M signs becomes all of them."""
import sys, json, itertools, argparse
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from indus_workbench import hypotheses as hy

ap = argparse.ArgumentParser(); ap.add_argument("lines"); ap.add_argument("bridge"); ap.add_argument("--no-doubtful", action="store_true")
a = ap.parse_args()
B = {"G" + k: ["M%d" % m for m in v] for k, v in json.load(open(a.bridge)).items() if v}

L = pd.read_csv(a.lines, dtype=str, keep_default_na=False)
L = L[L.line != "9"]
L["ln"] = L.line.astype(int)
OBJ = {"seal": "seal", "sealing": "tag", "miniature tablet": "tablet", "copper tablet": "tablet", "pottery graffito": "pottery",
       "bronze implement": "other", "ivory/bone rod": "rod", "miscellaneous": "other"}
rows = []
for (tn, side), g in L.sort_values("ln").groupby(["text_no", "side"]):
    toks = " ".join(g.signs_clean).split()
    doubtful = any(x.strip() for x in g.doubtful_positions)
    r0 = g.iloc[0]
    fs = r0.fs_description
    rows.append({"text_id": f"IM{tn}.{side}", "signs": ["M" + t for t in toks], "damaged": "0" in toks, "doubtful": doubtful,
                 "object_type": OBJ.get(r0.object_type, "other"), "material": "Copper" if r0.object_type == "copper tablet" else "",
                 "site": {"Mohenjodaro": "Mohenjo-daro", "Chanhudaro": "Chanhujo-daro"}.get(r0.site, r0.site), "motif": fs,
                 "is_unicorn": "yes" if fs.startswith("Unicorn") else ("no" if fs not in ("", "None", "0") else ""),
                 "motif_group": "unicorn" if fs.startswith("Unicorn") else "other"})
df = pd.DataFrame(rows)
df = df[(~df.damaged) & (df.signs.map(len) >= 1)]
if a.no_doubtful:
    df = df[~df.doubtful]
print(f"IM77 texts after dropping damaged{' and doubtful' if a.no_doubtful else ''}: {len(df)}")

def tr_list(lst):
    out, miss = [], []
    for x in lst:
        if isinstance(x, str) and x.startswith("G"):
            (out.extend(B[x]) if x in B else miss.append(x))
        else:
            out.append(x)
    return list(dict.fromkeys(out)), miss

def tr_units(units):
    out, lost = [], 0
    for u in units:
        if all(g in B for g in u):
            out += [list(c) for c in itertools.product(*[B[g] for g in u])]
        else:
            lost += 1
    return out, lost

results = []
for f in sorted(Path("results").glob("confirmatory_*.json")):
    for x in json.loads(f.read_text()):
        if isinstance(x, dict) and x.get("verdict") == "Supported":
            results.append(x["id"])
for hid in results:
    path = Path("hypotheses") / f"{hid}.json"
    h = json.loads(path.read_text())
    if h.get("type") == "external" or h["kind"] in ("text_image_lookup",):
        print(f"{hid} {h['kind']}: not translatable here (external or image labels)"); continue
    p = json.loads(json.dumps(h["params"])); cov = []
    for k, v in list(p.items()):
        if k in ("units",):
            p[k], lost = tr_units(v); cov.append(f"{k}: {len(v)-lost}/{len(v)} units")
        elif k == "pairs":
            keep = [[B[x][0], B[y][0]] for x, y in v if x in B and y in B and len(B[x]) == 1 and len(B[y]) == 1 and B[x] != B[y]]
            p[k] = keep; cov.append(f"pairs: {len(keep)}/{len(v)}")
        elif isinstance(v, list) and v and isinstance(v[0], str):
            p[k], miss = tr_list(v); cov.append(f"{k}: {len(v)-len(miss)}/{len(v)}")
        elif isinstance(v, str) and v.startswith("G"):
            if v in B and len(B[v]) == 1: p[k] = B[v][0]; cov.append(f"{k}: ok")
            elif v in B: p[k] = B[v]; cov.append(f"{k}: {len(B[v])} M signs")
            else: p[k] = None; cov.append(f"{k}: UNMAPPED")
    if any(v is None or v == [] for v in p.values()):
        print(f"{hid} {h['kind']}: a required sign set is unmapped ({'; '.join(cov)})"); continue
    d = df
    if h["data_settings"].get("dedupe"):
        d = d.assign(_k=d.signs.map(tuple)).drop_duplicates("_k").drop(columns="_k")
    h2 = dict(h); h2["params"] = p
    try:
        r = hy.run_test(h2, d, n_perm=2000)
    except Exception as e:
        print(f"{hid} {h['kind']}: error {e}"); continue
    print(f"{hid} {h['kind']:18s} obs {r.observed:.3f} null {r.null_mean:.3f} p {r.p_value:.4f} support {r.n_support}  [{'; '.join(cov)}]")
