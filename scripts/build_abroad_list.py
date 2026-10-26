"""List 1: every Indus inscription found outside the Indus region, from all sources in the project, deduplicated.

Sources: export (all splits), held-out-from-export set, Laursen (2010) Fig. 11 blind transcription, extra_texts.csv.
Duplicates: a Laursen seal is treated as the same object as a corpus text from the same site when they share 2+ signs
(any order) - the rule found after the Laursen test. Keeps the corpus reading and notes the Laursen number.
Marks the position of the 'man' signs (G90 human figure, G91 twin men, and other G90-family compounds listed below).
"""
import csv, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from indus_workbench import data  # noqa: E402
ap = json.loads((ROOT / "predictions/abroad_pairs_2026-10-23.json").read_text()); AB = set(ap["abroad_sites"]) | {"Tell Jokha (Umma)", "Mesopotamia?", "Near East (unspecified)", "western Iranian plateau"}
MAN = {"G90": "man", "G91": "twin men", "G125": "man with bow", "G130": "man with rake", "G95": "man holding staff", "G117": "man + oval", "G127": "man between D shapes"}
rows = []
raw, _ = data.load_raw("indus_website")
c = data.build_corpus(raw, "indus_website", drop_damaged=False, dedupe=False, drop_unidentified=False, metadata=data.load_metadata("indus_website")).df
for r in c.itertuples():
    if r.site in AB:
        rows.append(dict(source=f"export ({r.split})", id=r.text_id, cisi=r.source_ref, site=r.site, object=r.object_type, complete=str(not r.damaged), motif=r.motif, signs=" ".join(r.signs)))
for r in csv.DictReader(open(ROOT / "data/icit_merged_paragorth/new_to_export_corpus.csv")):
    if r["site"] in AB:
        rows.append(dict(source="held-out-from-export set", id=r["inscription_id"], cisi=r["cisi_number"], site=r["site"], object=r["object_type"], complete=str(r["damaged"] == "False"), motif=r["motif"], signs=r["sign_sequence"]))
for r in csv.DictReader(open(ROOT / "data/extra_inscriptions/extra_texts.csv")):
    if r["region"] == "abroad":
        rows.append(dict(source="extra_texts", id=r["id"], cisi="", site=r["site"], object=r["object_type"], complete=r["complete"] == "Y" and "True" or "False", motif=r["motif"], signs=r["sign_sequence_reading_order"]))
BAD = ("PSEUDO", "DECORATION", "NON-INDUS")
for r in csv.DictReader(open(ROOT / "data/laursen2010/foreign_inscriptions_laursen2010.csv")):
    if r["region"] != "abroad" or any(b in r["flags"] for b in BAD):
        continue
    s = set(r["sign_sequence_reading_order"].split()) - {"NOMATCH"}
    dup = [x for x in rows if x["site"] == r["site"] and len(s & set(x["signs"].split())) >= 2]
    if dup:
        dup[0]["laursen_no"] = r["seal_no"]; continue
    rows.append(dict(source="Laursen 2010 Fig. 11", id=f"Laursen-{r['seal_no']}", cisi="", site=r["site"], object="seal (Gulf Type)",
                     complete=str("BROKEN" not in r["flags"]), motif="", signs=r["sign_sequence_reading_order"], laursen_no=r["seal_no"]))
for x in rows:
    s = x["signs"].split()
    m = [(i, g) for i, g in enumerate(s) if g in MAN]
    x["man_signs"] = " ".join(f"{g}@{i + 1}/{len(s)}" for i, g in m)
    x["after_man"] = " | ".join(" ".join(s[i + 1:]) for i, _ in m)
    x.setdefault("laursen_no", "")
keys = ["source", "id", "cisi", "laursen_no", "site", "object", "complete", "motif", "signs", "man_signs", "after_man"]
with open(ROOT / "data/abroad/abroad_inscriptions.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); [w.writerow({k: x.get(k, "") for k in keys}) for x in rows]
print(f"{len(rows)} abroad inscriptions; with a man sign: {sum(bool(x['man_signs']) for x in rows)}")
from collections import Counter
print(Counter(x["source"].split(" (")[0] for x in rows)); print(Counter(x["site"] for x in rows).most_common())
