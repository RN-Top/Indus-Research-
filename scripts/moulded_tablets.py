"""(3) Moulded tablets (ICIT code TAB:B = bas-relief/moulded, mass-produced): which texts are repeated in many copies,
which also appear on seals, and where twelve (G55) sits. Scouting, descriptive (all data seen)."""
import sys
from collections import Counter
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from indus_workbench import data  # noqa: E402
parts = []
for key in ("indus_website", "icit_new_to_export"):
    raw, _ = data.load_raw(key); md = data.load_metadata(key)
    parts.append(data.build_corpus(raw, key, drop_damaged=True, metadata=md).df.merge(md[["text_id", "object_codes"]], on="text_id", how="left"))
df = pd.concat(parts, ignore_index=True); df["key"] = df.signs.map(lambda s: " ".join(s)); df = df.drop_duplicates(["text_id", "source_ref", "key"])
tab = df[df.object_codes.astype(str).str.startswith("TAB")]
out = [f"Tablets by code: {tab.object_codes.value_counts().to_dict()}; sites: {tab.site.value_counts().head(5).to_dict()}"]
mb = tab[tab.object_codes.eq("TAB:B")]
copies = mb.groupby("key").size().sort_values(ascending=False)
seal_keys = set(df[df.object_type.eq("seal")].key)
out.append(f"\nMoulded tablets (TAB:B): {len(mb)} objects, {len(copies)} distinct texts; texts in 3+ copies: {(copies>=3).sum()}")
out.append("Most-copied moulded texts (copies; also on a seal?):")
for k, n in copies.head(20).items():
    out.append(f"  {n:3}  {k:35} {'SEAL TOO' if k in seal_keys else ''}")
g = mb[mb.signs.map(lambda s: 'G55' in s)]
out.append(f"\nMoulded tablets with G55: {len(g)}  -> " + "; ".join(f"{r.site} {r.source_ref} {r.key}" for _, r in g.iterrows()))
# share of moulded texts that also occur on seals vs chance-ish: share of distinct moulded texts found on seals
out.append(f"Distinct moulded texts also found on seals: {sum(k in seal_keys for k in copies.index)} of {len(copies)}")
sign_mb = Counter(x for s in mb.signs for x in s); sign_all = Counter(x for s in df.signs for x in s)
nm, na = sum(sign_mb.values()), sum(sign_all.values())
over = sorted(((sign_mb[x]/nm)/(sign_all[x]/na), x, sign_mb[x]) for x in sign_mb if sign_mb[x] >= 8)[::-1][:12]
out.append("Signs most over-represented on moulded tablets (ratio, count): " + ", ".join(f"{x} {r:.1f}x ({n})" for r, x, n in over))
print("\n".join(out)); (ROOT / "results/moulded_tablets_output.txt").write_text("\n".join(out) + "\n")
