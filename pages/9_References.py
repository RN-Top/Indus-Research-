import re
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="References", layout="wide")
st.title("References")

bib = (Path(__file__).resolve().parent.parent / "references.bib").read_text()
entries = re.findall(r"@\w+\{([^,]+),(.*?)\n\}", bib, flags=re.S)


def field(body: str, name: str) -> str:
    m = re.search(rf"{name}\s*=\s*\{{(.*?)\}},?\n", body, flags=re.S)
    return re.sub(r"[{}]", "", m.group(1)).strip() if m else ""


for key, body in sorted(entries, key=lambda e: (field(e[1], "author"), field(e[1], "year"))):
    venue = field(body, "journal") or field(body, "publisher") or field(body, "series") or field(body, "howpublished")
    line = f"{field(body, 'author')} ({field(body, 'year')}). *{field(body, 'title')}*. {venue}."
    doi = field(body, "doi")
    if doi:
        line += f" [doi:{doi}](https://doi.org/{doi})"
    st.markdown(f"- {line}  `{key}`")

st.download_button("Download BibTeX", bib, file_name="indus-references.bib", mime="text/plain")
