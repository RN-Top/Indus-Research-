"""Is G55 (twelve strokes) commoner at sites on the sea than inland? Scouting, descriptive.
Sites are classed by their setting in Harappan times (c. 2600-1900 BCE), not today (data/ancient_waterways.json notes):
  sea   - coast, tidal estuary, the Rann of Kutch (then open water), Gulf islands and coasts, Ur (Gulf-head port)
  river - on a major river or the then-flowing Ghaggar-Hakra
  dry   - hills or oases away from big water
Classes fixed before counting. Texts: export (all splits) + held-out-from-export set, deduplicated by sign sequence
within each site. Already-seen material (the G55 test used the new set), so this is description, not a test."""
import sys
from collections import Counter
from pathlib import Path
import pandas as pd
from scipy.stats import fisher_exact
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from indus_workbench import data  # noqa: E402
SEA = {"Lothal", "Dholavira", "Surkotada", "Kanmer", "Khirsara", "Desalpur", "Shikarpur", "Bala-kot", "Allahdino",
       "Qala'at al-Bahrain", "Saar", "Hajar", "Karzakan", "Janabiyah", "Ra's al-Junayz", "Ur", "Failaka"}
RIVER = {"Mohenjo-daro", "Harappa", "Chanhujo-daro", "Lakhanjo-daro", "Ganweriwala", "Kalibangan", "Banawali", "Bhirrana",
         "Rakhigarhi", "Farmana", "Rupar", "Alamgirpur", "Kish", "Tell Umma", "Susa", "Jhukar", "Amri"}
DRY = {"Nausharo", "Miri Qalat", "Nindowari-damb", "Gonur Depe", "Altyn Depe", "Shortughai", "Salut", "Luristan"}
def cls(s): return "sea" if s in SEA else "river" if s in RIVER else "dry" if s in DRY else None
parts = []
for key in ("indus_website", "icit_new_to_export"):
    raw, _ = data.load_raw(key)
    parts.append(data.build_corpus(raw, key, drop_damaged=False, metadata=data.load_metadata(key)).df[["site", "signs"]])
df = pd.concat(parts, ignore_index=True); df["key"] = df.signs.map(tuple)
df = df.drop_duplicates(["site", "key"]); df["water"] = df.site.map(cls)
df["g55"] = df.signs.map(lambda s: "G55" in s)
out = []
t = df.dropna(subset=["water"]).groupby("water").agg(texts=("g55", "size"), with_g55=("g55", "sum"))
t["per_1000"] = (1000 * t.with_g55 / t.texts).round(1); out.append(t.to_string())
for a, b in (("sea", "river"),):
    x = t.loc[a]; y = t.loc[b]
    odds, p = fisher_exact([[x.with_g55, x.texts - x.with_g55], [y.with_g55, y.texts - y.with_g55]], alternative="greater")
    out.append(f"\nsea vs river: odds ratio {odds:.2f}, one-sided Fisher p {p:.4f}")
home_sea = df[df.water.eq("sea") & ~df.site.isin({"Qala'at al-Bahrain", "Saar", "Hajar", "Karzakan", "Janabiyah", "Ra's al-Junayz", "Ur", "Failaka"})]
x = home_sea.g55; y = df[df.water.eq("river")].g55
odds, p = fisher_exact([[x.sum(), len(x) - x.sum()], [y.sum(), len(y) - y.sum()]], alternative="greater")
out.append(f"Indian coast only (no Gulf) vs river: {x.sum()}/{len(x)} vs {y.sum()}/{len(y)}; odds ratio {odds:.2f}, p {p:.4f}")
out.append("\nPer site (texts with G55 / distinct texts):")
for s, g in df[df.g55].groupby("site"):
    out.append(f"  {s:20} {cls(s) or '-':5} {len(g)}/{(df.site == s).sum()}")
out.append("\nG55 texts at sea sites:")
for _, r in df[df.g55 & df.water.eq("sea")].iterrows(): out.append(f"  {r.site:20} {' '.join(r.signs)}")
print("\n".join(out)); (ROOT / "results/g55_water_scouting_output.txt").write_text("\n".join(out) + "\n")
# Added after seeing the output above: does a G55 text also contain a man sign? By region.
MAN = {"G90", "G91", "G125"}
GUJ = {"Lothal", "Dholavira", "Surkotada", "Kanmer", "Khirsara", "Desalpur", "Shikarpur"}
GULF = {"Qala'at al-Bahrain", "Saar", "Hajar", "Karzakan", "Janabiyah", "Ra's al-Junayz", "Failaka"}
def reg(s): return "Gujarat coast" if s in GUJ else "Gulf" if s in GULF else "Indus/Ghaggar rivers" if s in RIVER and s not in {"Kish", "Tell Umma", "Susa"} else None
df["region"] = df.site.map(reg); df["man"] = df.signs.map(lambda s: bool(MAN & set(s)))
o2 = ["\nG55 texts that also contain a man sign, by region (vs all texts in that region):"]
for r, g in df.dropna(subset=["region"]).groupby("region"):
    gg = g[g.g55]; o2.append(f"  {r:22} G55 texts with man: {gg.man.sum()}/{len(gg)}   all texts with man: {g.man.sum()}/{len(g)} ({g.man.mean():.1%})")
riv = df[df.region.eq("Indus/Ghaggar rivers") & df.g55]
o2.append("  River-city G55 texts with a man sign: " + "; ".join(f"{r.site}: {' '.join(r.signs)}" for _, r in riv[riv.man].iterrows()))
print("\n".join(o2)); open(ROOT / "results/g55_water_scouting_output.txt", "a").write("\n".join(o2) + "\n")
