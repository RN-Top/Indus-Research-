"""Office seals vs single-use seals (scouting; all data seen; descriptive).
Frenez (2024): Indus clay sealings recorded who opened a container/room; a seal impressed on many sealings is an
official's seal in repeated use. For sealings/tags (object_type 'tag'), group identical sign sequences at the same
site = impressions of one seal (or of identical seals). Compare the signs on multi-impression seals (2+) with
single-impression ones. Also list multi-impression seals and where else (seals, other sites) the same text occurs."""
import sys
from collections import Counter, defaultdict
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from indus_workbench import data  # noqa: E402
parts = []
for key in ("indus_website", "icit_new_to_export"):
    raw, _ = data.load_raw(key); md = data.load_metadata(key)
    d = data.build_corpus(raw, key, drop_damaged=False, metadata=md).df.merge(md[["text_id", "object_codes"]], on="text_id", how="left")
    parts.append(d)
df = pd.concat(parts, ignore_index=True); df["key"] = df.signs.map(lambda s: " ".join(s))
df = df.drop_duplicates(["text_id", "source_ref", "key"])
tags = df[df.object_type.eq("tag")]
grp = tags.groupby(["site", "key"]).agg(n=("text_id", "size"), refs=("source_ref", lambda x: sorted(set(map(str, x)))),
                                        codes=("object_codes", lambda x: dict(Counter(map(str, x))))).reset_index()
multi = grp[grp.n >= 2].sort_values("n", ascending=False); single = grp[grp.n == 1]
out = [f"Sealings/tags: {len(tags)} objects, {len(grp)} distinct seal texts by site; used 2+ times: {len(multi)}; once: {len(single)}",
       f"Tag sites: {tags.site.value_counts().to_dict()}\n", "Multi-impression seals:"]
elsewhere = df[~df.object_type.eq("tag")]
for _, r in multi.iterrows():
    other = elsewhere[elsewhere.key.eq(r.key)]
    o = "; also on: " + ", ".join(f"{a} {b}" for a, b in Counter(zip(other.site, other.object_type)).items()) if len(other) else ""
    out.append(f"  {r.n:2}x {r.site:12} {r.key}   {r.codes}{o}")
def signs(g): return Counter(x for k in g.key for x in k.split())
cm, cs = signs(multi), signs(single); tm, ts = sum(cm.values()), sum(cs.values())
out.append(f"\nSign tokens: multi-use seals {tm}, single-use {ts}")
out.append("Signs on multi-use seals (share vs single-use share):")
for g, n in cm.most_common(25):
    out.append(f"  {g:5} {n:3}  {n/tm:.3f} vs {cs[g]/ts:.3f}")
print("\n".join(out)); (ROOT / "results/office_seals_scouting_output.txt").write_text("\n".join(out) + "\n")
