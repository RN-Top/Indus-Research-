"""(2) The same seal text in more than one place (scouting; descriptive). Identical sign sequences of 3+ signs found
at 2+ sites. Highlights pairs of a SEAL at one site and SEALINGS (tags) at another: the seal's holder, or an identical
seal of the same office, acting in two cities. Also (1) the Lothal sealings by seal text with what they closed
(Frenez & Tosi 2005, Table 1, via paragorth derived/lothal-sealings-frenez-tosi2005.json)."""
import json, sys
from collections import Counter, defaultdict
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from indus_workbench import data  # noqa: E402
parts = []
for key in ("indus_website", "icit_new_to_export"):
    raw, _ = data.load_raw(key); md = data.load_metadata(key)
    parts.append(data.build_corpus(raw, key, drop_damaged=True, metadata=md).df)
df = pd.concat(parts, ignore_index=True); df["key"] = df.signs.map(lambda s: " ".join(s))
df = df.drop_duplicates(["text_id", "source_ref", "key"])
out = ["(1) Lothal sealings by seal text (Frenez & Tosi 2005 Table 1: closure type, context W = warehouse)"]
FT = {r[0]: r for r in json.load(open(Path.home() / "ext2/pg/data/derived/lothal-sealings-frenez-tosi2005.json"))["rows"]}
lot = df[df.site.eq("Lothal") & df.object_type.eq("tag")]
for k, g in lot.groupby("key"):
    refs = sorted(set(map(str, g.source_ref)))
    if len(refs) >= 2:
        info = [f"{r}:{FT[r][2]}/{FT[r][3]}/{FT[r][1]} seals" for r in refs if r in FT]
        types = {FT[r][2] for r in refs if r in FT and FT[r][2] != "undiagnostic"}
        out.append(f"  {len(refs)}x  {k}  -> {len(types)} closure types: " + "; ".join(info))
out.append("\n(2) Identical texts (3+ signs) at 2+ sites:")
multi = df[df.signs.map(len) >= 3].groupby("key")
rows = []
for k, g in multi:
    if g.site.nunique() >= 2:
        objs = Counter(zip(g.site, g.object_type))
        sealing_sites = set(g[g.object_type.eq("tag")].site); seal_sites = set(g[g.object_type.eq("seal")].site)
        cross = bool(sealing_sites and (seal_sites - sealing_sites))
        rows.append((cross, len(g), k, dict(objs)))
rows.sort(key=lambda r: (-r[0], -r[1]))
for cross, n, k, objs in rows[:40]:
    out.append(f"  {'SEAL->SEALING ' if cross else '              '}{n:3}  {k:40} {objs}")
out.append(f"\nTexts (3+ signs) at 2+ sites: {len(rows)}; of these with a seal at one site and sealings at another: {sum(r[0] for r in rows)}")
print("\n".join(out)); (ROOT / "results/same_seal_sites_output.txt").write_text("\n".join(out) + "\n")
