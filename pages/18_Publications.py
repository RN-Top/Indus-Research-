"""Publications: Erin Rae Toppe's Zenodo preprints, read from the README.

Read-only. Parses the Zenodo entries in README.md so the list has one source of truth.
"""

import re
from pathlib import Path

import streamlit as st

from indus_workbench import ui

st.set_page_config(page_title="Publications", layout="wide")
st.title("Publications")
ui.init_settings()

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

st.markdown(
    "Preprints by Erin Rae Toppe on Zenodo. None is peer-reviewed. Each one reports its tests, "
    "including failures."
)

entry = re.compile(r"^(?:\*\*Preprints:\*\*\s*)?Toppe, E\. R\. \(2026\)\. \*(?P<title>.+?)\*")
doi = re.compile(r"doi:(10\.5281/zenodo\.\d+)")

items = []
for line in README.read_text(encoding="utf-8").splitlines():
    m = entry.match(line.strip())
    if not m:
        continue
    dois = doi.findall(line)
    note = "not peer-reviewed" in line
    exploratory = "exploratory" in line
    items.append(
        {
            "title": m.group("title"),
            "dois": dois,
            "latest_doi": dois[-1] if dois else "",
            "note": "exploratory" if exploratory else ("not peer-reviewed" if note else ""),
            "raw": line.strip(),
        }
    )

st.metric("Preprints", len(items))
for it in items:
    st.subheader(it["title"])
    if it["latest_doi"]:
        st.markdown(f"Latest version: [doi:{it['latest_doi']}](https://doi.org/{it['latest_doi']})")
    if len(it["dois"]) > 1:
        st.caption("All versions: " + ", ".join(it["dois"]))
    if it["note"]:
        st.caption(it["note"])
