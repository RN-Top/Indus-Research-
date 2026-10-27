"""(4) The jar sign G740: where it sits, what follows, and what precedes it when the man sign follows ('jar + man').
Scouting on exploration texts (deduplicated), descriptive."""
import sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
from indus_workbench import data  # noqa: E402
from number_system import VAL  # noqa: E402
raw, _ = data.load_raw("indus_website"); md = data.load_metadata("indus_website")
full = data.explore_only(data.build_corpus(raw, "indus_website", drop_damaged=True, metadata=md)).df
full["key"] = full.signs.map(tuple); full = full.drop_duplicates("key")
seqs = [list(s) for s in full.signs]; obj = list(full.object_type)
MAN = {"G90", "G91", "G125"}
n = 0; after = Counter(); before = Counter(); pos = Counter()
for s in seqs:
    for k, x in enumerate(s):
        if x != "G740": continue
        n += 1; after[s[k + 1] if k + 1 < len(s) else "END"] += 1; before[s[k - 1] if k else "START"] += 1
        pos["last" if k == len(s) - 1 else "first" if k == 0 else "inside"] += 1
out = [f"G740 uses (complete texts, exploration, distinct): {n}; position {dict(pos)}",
       "After G740: " + ", ".join(f"{k} {v}" for k, v in after.most_common(10)),
       "Before G740: " + ", ".join(f"{k} {v}" for k, v in before.most_common(12))]
# texts ending '... G740 G90' (jar + man) vs '... G740' (jar final): what object types, what precedes
jm = [(s, o) for s, o in zip(seqs, obj) if len(s) >= 2 and s[-2:] == ["G740", "G90"]]
jf = [(s, o) for s, o in zip(seqs, obj) if s and s[-1] == "G740"]
out.append(f"\nTexts ending in jar + man (G740 G90): {len(jm)}; objects {Counter(o for _, o in jm)}")
out.append(f"Texts ending in jar (G740): {len(jf)}; objects {Counter(o for _, o in jf).most_common(4)}")
out.append("Sign before 'G740 G90': " + ", ".join(f"{k} {v}" for k, v in Counter(s[-3] for s, _ in jm if len(s) >= 3).most_common(10)))
out.append("Sign before final 'G740': " + ", ".join(f"{k} {v}" for k, v in Counter(s[-2] for s, _ in jf if len(s) >= 2).most_common(10)))
out.append("Numeral right before G740: " + str(sum(v for k, v in before.items() if k in VAL)) + f" of {n}; which: " + str({k: v for k, v in before.items() if k in VAL}))
print("\n".join(out)); (ROOT / "results/jar_sign_output.txt").write_text("\n".join(out) + "\n")
