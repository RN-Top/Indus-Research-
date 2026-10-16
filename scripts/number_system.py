"""Do the Indus stroke signs behave like a number system? (EXPLORATION ONLY: description, no tests.)

Stroke values are read from the sign drawings in the SK Indus Script font (see
results/number_system_scouting.md): short strokes G1-G7 = 1-7; stacked strokes
G13 3, G14 4, G15 5, G16 6, G17 7, G18 8, G19 9, G27 7 (2+3+2), G28 8 (3+3+2),
G29 9 (3+3+3), G55 12 (4+4+4); long strokes G31-G33 = 1-3, G35 = 5 (G34, likely
4, is not in the font). G2 straight after an opener is set aside (the heading's
cluster-closer, results/heading_types.md). Exploration split only.

    python scripts/number_system.py
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from functional_skeleton import assign  # noqa: E402
from functional_slots import load  # noqa: E402

VAL = {"G1": 1, "G2": 2, "G3": 3, "G4": 4, "G5": 5, "G6": 6, "G7": 7,
       "G13": 3, "G14": 4, "G15": 5, "G16": 6, "G17": 7, "G18": 8, "G19": 9,
       "G27": 7, "G28": 8, "G29": 9, "G55": 12,
       "G31": 1, "G32": 2, "G33": 3, "G34": 4, "G35": 5}
SERIES = {**{s: "short" for s in ["G1", "G2", "G3", "G4", "G5", "G6", "G7"]},
          **{s: "stacked" for s in ["G13", "G14", "G15", "G16", "G17", "G18", "G19", "G27", "G28", "G29", "G55"]},
          **{s: "long" for s in ["G31", "G32", "G33", "G34", "G35"]}}


def main():
    df = load()
    roles, _ = assign(list(df["signs"]))
    out = {}
    tok = Counter()
    runs = []  # (text index, start, run signs)
    for ti, s in enumerate(df["signs"]):
        k = 0
        while k < len(s):
            if s[k] in VAL and not (s[k] == "G2" and k > 0 and roles.get(s[k - 1]) == 0):
                j = k
                while j < len(s) and s[j] in VAL and not (s[j] == "G2" and j > 0 and roles.get(s[j - 1]) == 0):
                    tok[s[j]] += 1
                    j += 1
                runs.append((ti, k, s[k:j]))
                k = j
            else:
                k += 1
    # 1-2: counts by series and value
    print("== 1-2. Numeral tokens by series and value (G2 after an opener set aside) ==")
    table = {}
    for ser in ["short", "stacked", "long"]:
        byv = Counter()
        for x, n in tok.items():
            if SERIES[x] == ser:
                byv[VAL[x]] += n
        table[ser] = dict(sorted(byv.items()))
        print(f"   {ser:8}", ", ".join(f"{v}: {n}" for v, n in sorted(byv.items())), f"  (total {sum(byv.values())})")
    out["tokens_by_series_value"] = table
    out["tokens_by_sign"] = dict(tok.most_common())

    # 3: run shapes
    L = Counter(len(r[2]) for r in runs)
    shapes = Counter(" ".join(r[2]) for r in runs if len(r[2]) > 1)
    mixed = Counter(tuple(sorted({SERIES[x] for x in r[2]})) for r in runs if len(r[2]) > 1)
    desc = sum(all(VAL[a] >= VAL[b] for a, b in zip(r[2], r[2][1:])) for r in runs if len(r[2]) > 1)
    multi = sum(len(r[2]) > 1 for r in runs)
    print(f"\n== 3. Numeral runs (consecutive stroke signs): {len(runs)}; length {dict(sorted(L.items()))}")
    print(f"   multi-sign runs: {multi}; series mixed in them: {dict(mixed)}; values never increasing: {desc} of {multi}")
    print("   commonest multi-sign runs:", shapes.most_common(12))
    out["runs"] = dict(n=len(runs), length=dict(L), multi=multi, mixed={"+".join(k): v for k, v in mixed.items()},
                       nonincreasing=desc, top=shapes.most_common(20))

    # 4: what is counted (sign right after a single-sign run)
    after = defaultdict(Counter)
    for ti, k, r in runs:
        s = df["signs"].iloc[ti]
        nxt = s[k + len(r)] if k + len(r) < len(s) else "END"
        after[nxt][(SERIES[r[0]], VAL[r[0]]) if len(r) == 1 else ("run", "+".join(r))] += 1
    counted = sorted(after.items(), key=lambda kv: -sum(kv[1].values()))
    print("\n== 4. What follows a numeral run (the counted item?) ==")
    rows = []
    for x, c in counted[:15]:
        n = sum(c.values())
        vals = sorted({v for (ser, v) in c if ser != "run"})
        rows.append(dict(sign=x, n=n, role={0: "opener", 2: "closer"}.get(roles.get(x), "middle") if x != "END" else "end",
                         distinct_values=len(vals), values=vals, top=[(f"{a} {b}", m) for (a, b), m in c.most_common(4)]))
        print(f"   {x:5} after {n:3} runs ({rows[-1]['role']}); single-sign values seen: {vals}; top {rows[-1]['top']}")
    out["counted"] = rows

    # 5: position
    rel = []
    for ti, k, r in runs:
        s = df["signs"].iloc[ti]
        if len(s) > 1:
            rel.append(k / (len(s) - 1))
    rel = np.array(rel)
    before_closer = sum(1 for ti, k, r in runs if k + len(r) < len(df["signs"].iloc[ti]) and roles.get(df["signs"].iloc[ti][k + len(r)]) == 2)
    at_end = sum(1 for ti, k, r in runs if k + len(r) == len(df["signs"].iloc[ti]))
    print(f"\n== 5. Position of runs: relative start mean {rel.mean():.2f}; first third {np.mean(rel < 1/3):.0%}, "
          f"middle {np.mean((rel >= 1/3) & (rel <= 2/3)):.0%}, last third {np.mean(rel > 2/3):.0%}; "
          f"right before a closer {before_closer}; text-final {at_end} of {len(runs)}")
    out["position"] = dict(mean=float(rel.mean()), first_third=float(np.mean(rel < 1/3)), last_third=float(np.mean(rel > 2/3)),
                           before_closer=before_closer, text_final=at_end)
    (ROOT / "results" / "number_system.json").write_text(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
