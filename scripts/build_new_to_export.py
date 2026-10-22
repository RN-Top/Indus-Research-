"""Build the 'new to my export' set: objects in the fuller ICIT copy (paragorth's merged Wells/ICIT corpus,
data/icit_merged_paragorth/merged-corpus-canonical.json) whose text does not occur ANYWHERE in this project's
corpus (data/indus_website_real_corpus.csv, all splits, damaged included), in either direction.

These texts were never seen by any exploration or holdout analysis here. They are not independent of ICIT
(same transcription project), so a test on them is a 'held out from my export' test, not an out-of-corpus test.
Sequences use the merged file's seq_raw (no allograph merges), in reading order, as G-numbers.

    python scripts/build_new_to_export.py
"""
import csv, json, sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from indus_workbench import data  # noqa: E402

m = json.load(open(ROOT / "data/icit_merged_paragorth/merged-corpus-canonical.json"))
raw, _ = data.load_raw("indus_website")
a = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"),
                      drop_damaged=False, dedupe=False, drop_unidentified=False).df
mine = set()
for s in a.signs:
    t = tuple(s); mine.add(t); mine.add(t[::-1])
SITE = {"Chanhu-daro": "Chanhujo-daro"}
SITE_MINE = {}
# object identity: CISI number (this project's CSV has it in cisi_number; "unknown" when absent)
mine_rows = list(csv.DictReader(open(ROOT / "data/indus_website_real_corpus.csv")))
mine_cisi = {r["cisi_number"].strip() for r in mine_rows if r["cisi_number"].strip() not in ("", "-", "unknown")}
# objects without a CISI number in the export, by site, for a fallback near-match
nocisi = {}
for r in mine_rows:
    if r["cisi_number"].strip() in ("", "-", "unknown"):
        nocisi.setdefault(SITE_MINE.get(r["site"], r["site"]), []).append(tuple(r["sign_sequence"].split()))


def near(t, others):
    return any(len(o) == len(t) and sum(x != y for x, y in zip(o, t)) <= 1 for o in others)


rows = []
for k, o in enumerate(m):
    seq = ["G%d" % x for x in o.get("seq_raw") or []]
    if not seq or tuple(seq) in mine:
        continue
    c = (o.get("cisi") or "").strip()
    site = SITE.get(o["site"], o["site"])
    if c not in ("", "-"):
        status = "same object (CISI in export)" if c in mine_cisi else "new object (CISI not in export)"
    else:
        status = ("probable re-transcription (no CISI; same site, length, 1 sign different)"
                  if near(tuple(seq), nocisi.get(site, [])) else "probably new (no CISI)")
    rows.append(dict(new_id=f"N{k:05d}", status=status, cisi=o.get("cisi", ""), site=SITE.get(o["site"], o["site"]), type=o.get("type", ""),
                     symbol=o.get("symbol", ""), material=o.get("material", ""), complete=o.get("complete", ""),
                     period=o.get("period", ""), n_signs=len(seq), signs=" ".join(seq)))
out = ROOT / "data/icit_merged_paragorth/new_to_export.csv"
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
texts = Counter(r["signs"] for r in rows)
print(f"Merged objects: {len(m)}; this project's objects: {len(a)}")
print(f"New-to-export objects: {len(rows)}; distinct new texts: {len(texts)}; "
      f"complete (Y): {sum(r['complete'] == 'Y' for r in rows)}; 2+ signs: {sum(r['n_signs'] >= 2 for r in rows)}")
print("Status:", Counter(r["status"] for r in rows).most_common())
good = [r for r in rows if r["status"].startswith(("new object", "probably new"))]
print(f"Usable as new: {len(good)} objects, {len(set(r['signs'] for r in good))} distinct texts, "
      f"{sum(r['n_signs'] >= 2 for r in good)} with 2+ signs")
print("By site:", Counter(r["site"] for r in rows).most_common(10))
print("By type (first field):", Counter(r["type"].split(":")[0] for r in rows).most_common(10))
