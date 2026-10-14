"""Extract sign glyphs, sign variants and object details from the source database.

The full corpus (data/indus_website_real_corpus.csv) was converted from the
MySQL dump `population-script.sql` in github.com/yajnadevam/indus-website
(GPL-3.0). That dump holds more than the CSV kept. This script extracts:

  data/glyph_map.csv       G-number -> code point in the SK Indus Script font
  data/glyph_variants.csv  pairs of G-numbers the source marks as similar
  data/text_metadata.csv   per inscription: object type, material, size,
                           completeness, CISI number

The SQL file is not committed. To rebuild:
  git clone --depth 1 https://github.com/yajnadevam/indus-website /tmp/iw
  python scripts/extract_site_metadata.py /tmp/iw/population-script.sql
"""

import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

# Object codes from the source's FEATURE table, grouped as the source's own
# website groups them (src/data/usefulMaps.js), except TAB:C, which the
# website labels "Tag" but whose code says tablet; it is kept as a tablet.
OBJECT_GROUPS = {
    "SEAL": "seal", "SEAL:S": "seal", "SEAL:R": "seal", "SEAL:C": "seal", "SEAL:CY": "seal",
    "SEAL:L": "seal", "TAB:I": "tablet", "TAB:B": "tablet", "TAB:C": "tablet",
    "TAG": "tag", "TAG:P": "tag", "TAG:L": "tag", "TAG:O": "tag", "TAG:B": "tag", "TAG:W": "tag",
    "TAG:C": "tag", "TAG:R": "tag", "POT:T:g": "pottery", "POT:T:s": "pottery", "POT:T:p": "pottery",
    "ROD": "rod", "BNGL": "bangle", "IMPL": "impression", "MISC": "other", "Oth": "other",
}


def values(sql: str, table: str) -> str:
    m = re.search(r"INSERT INTO " + table + r"\b[^;]*?VALUES\s*(.*?);\s*\n", sql, re.S)
    return m.group(1) if m else ""


def main(path: str) -> None:
    sql = Path(path).read_text(encoding="utf-8", errors="replace")

    glyphs = []
    for gid, ent in re.findall(r'\((\d+),\s*"&#x([0-9A-Fa-f]+);"', values(sql, "GLYPH")):
        glyphs.append({"g_sign": f"G{int(gid)}", "codepoint": f"U+{ent.upper()}"})
    pd.DataFrame(glyphs).to_csv(ROOT / "data/glyph_map.csv", index=False)

    sim = re.findall(r"\((\d+),\s*(\d+)\)", values(sql, "GLYPHSIMILARITY"))
    pd.DataFrame([{"g_sign": f"G{a}", "similar_to": f"G{b}"} for a, b in sim]).to_csv(
        ROOT / "data/glyph_variants.csv", index=False)

    feature = dict(re.findall(r'\((\d+),\s*"([^"]+)"\)', values(sql, "FEATURE")))
    obj: dict[str, list[str]] = {}
    for sid, qid in re.findall(r"\((\d+),\s*(\d+)\)", values(sql, "ICONOGRAPHYFEATURES")):
        obj.setdefault(sid, []).append(feature.get(qid, "?"))

    complete = dict(re.findall(r'\((\d+),\s*"([YN])"', values(sql, "INSCRIPTION")))

    seals = re.findall(
        r'\((\d+),\s*"([^"]*)",\s*(NULL|"[^"]*"),\s*(NULL|"[^"]*"),\s*(NULL|"[^"]*"),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)\)',
        values(sql, "SEAL"))
    rows = []
    for sid, site, material, cisi, _museum, w, h, t in seals:
        codes = obj.get(sid, [])
        groups = sorted({OBJECT_GROUPS.get(c, "other") for c in codes})
        rows.append({
            "text_id": f"S{sid}",
            "object_codes": ";".join(codes),
            "object_type": groups[0] if len(groups) == 1 else ("mixed" if groups else "unknown"),
            "material": material.strip('"') if material != "NULL" else "",
            "complete": complete.get(sid, ""),
            "width_mm": float(w) or None, "height_mm": float(h) or None,
        })
    pd.DataFrame(rows).to_csv(ROOT / "data/text_metadata.csv", index=False)
    print(f"glyphs {len(glyphs)}, variant pairs {len(sim)}, inscriptions {len(rows)}")


if __name__ == "__main__":
    main(sys.argv[1])
