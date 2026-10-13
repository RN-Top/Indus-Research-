import streamlit as st

from app_common import sidebar, synthetic_banner

st.set_page_config(page_title="Indus Script Research", layout="wide")
corpus = sidebar()

st.title("Indus Script Research")
st.write(
    "A workbench for studying the Indus (Harappan) script. The script is undeciphered: "
    "this app does not read it. It makes the inscriptions searchable, measures their structure "
    "reproducibly, and tests proposed readings against a null model."
)
synthetic_banner(corpus)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Texts", len(corpus.texts))
c2.metric("Objects", len(corpus.objects))
c3.metric("Sites", len(corpus.sites))
c4.metric("Signs in list", len(corpus.signs))

st.subheader("Pages")
st.markdown(
    """
- **Corpus Browser**: search texts by sign sequence, site, object type and iconography.
- **Sign Lists**: the working sign list and its cross-references to Mahadevan, Parpola and Wells.
- **Structure**: sign frequency, positional profiles, n-grams and entropy against controls.
- **Hypothesis Workbench**: lock a proposed reading and score it against shuffled keys and held-out texts.
- **References**: sources for every dataset and method.
"""
)

st.subheader("Data checks")
if corpus.errors:
    st.warning(f"{len(corpus.errors)} problems found while loading this corpus.")
    st.code("\n".join(corpus.errors[:200]))
else:
    st.success("All files loaded and every text points to a known object and known signs.")

st.caption(
    "Copyrighted corpora (CISI photographs, Mahadevan 1977, ICIT) are never stored in this repository. "
    "Put licensed data in data/private/ to use it locally."
)
