"""Indus Script Workbench: home page, data choice and data audit."""

import pandas as pd
import streamlit as st

from indus_workbench import data, ui

st.set_page_config(page_title="Indus Script Workbench", page_icon="🔍", layout="wide")

st.title("Indus Script Workbench")
st.info(ui.DISCLAIMER)

st.markdown(
    "Every result in this app is checked three ways:\n"
    "- **Negative controls**: the same measurement on shuffled or random sign sequences. "
    "A pattern that also appears there is not evidence.\n"
    "- **Positive controls**: the same measurement on data with known structure. "
    "A method that misses known structure can't be trusted.\n"
    "- **A locked holdout**: 20% of texts are set aside. Hypotheses are explored on the "
    "other 80%, registered publicly, then tested once on the holdout."
)

ui.init_settings()
st.header("1. Choose the data")
st.radio("Corpus", list(data.SOURCES), key="source_key",
         format_func=lambda k: data.SOURCES[k]["label"])
c1, c2 = st.columns(2)
c1.checkbox("Exclude texts marked damaged", key="drop_damaged",
            help="Damaged texts may be missing signs, which distorts sequence statistics.")
c2.checkbox("Remove exact duplicate texts", key="dedupe",
            help="Identical texts (for example sets of matching tablets) can inflate counts. "
                 "Run important results both ways; the Robustness page does this for you.")

corpus = ui.load_corpus()
ui.sidebar_status(corpus)
if corpus is None:
    st.stop()

src = data.SOURCES[corpus.source_key]
st.header("2. Data audit")
m = st.columns(4)
m[0].metric("Texts used", f"{corpus.n_texts:,}")
m[1].metric("Sign tokens", f"{corpus.n_tokens:,}")
m[2].metric("Distinct signs", f"{len(corpus.sign_inventory):,}")
m[3].metric("Texts excluded", f"{len(corpus.exclusions):,}")

st.markdown(
    f"- **Origin:** {src['origin']}\n"
    f"- **Licence:** {src['licence']}\n"
    f"- **Sign numbering:** {src['sign_scheme']}\n"
    f"- **Pinned version:** dataset commit `{data.HF_REVISION[:12]}`\n"
    f"- **File fingerprint (SHA-256):** `{corpus.sha256}`"
)
st.caption(
    "If the fingerprint ever changes, the data changed, and results are no longer comparable "
    "with earlier ones. Quote the fingerprint whenever you report a result."
)

split = corpus.df["split"].value_counts()
st.markdown(
    f"**Split:** {split.get('explore', 0):,} texts for exploration, "
    f"{split.get('holdout', 0):,} locked in the holdout. The split depends only on each text's ID "
    "and a fixed salt, so nobody can choose a favourable split."
)

with st.expander(f"Excluded texts and reasons ({len(corpus.exclusions):,})"):
    if corpus.exclusions:
        ex = pd.DataFrame([e.__dict__ for e in corpus.exclusions])
        st.dataframe(ex["reason"].value_counts().rename("texts"))
        st.dataframe(ex, use_container_width=True, height=300)
    else:
        st.write("None.")

with st.expander("Caveats a reviewer will raise about this data"):
    st.markdown(
        "- The full corpus comes from a website transcription. Its sign list is not named "
        "on the dataset card, so G-numbers can't yet be matched to Mahadevan or Parpola "
        "numbers. Treat results from it as provisional until they are repeated on a scholarly "
        "corpus such as ICIT.\n"
        "- The CISI files cover only 179 seals from one site. They are small, but come in three "
        "versions that split sign variants differently. That makes them the right place to "
        "test whether a result depends on how signs were identified.\n"
        "- Reading direction is a storage convention in this dataset: right-to-left rows are "
        "used as stored and left-to-right rows are reversed."
    )

ui.log_result("data", {
    "source_key": corpus.source_key, "url": src["url"], "sha256": corpus.sha256,
    "revision": data.HF_REVISION, "settings": corpus.settings,
    "n_texts": corpus.n_texts, "n_tokens": corpus.n_tokens,
    "n_signs": len(corpus.sign_inventory), "n_excluded": len(corpus.exclusions),
    "explore": int(split.get("explore", 0)), "holdout": int(split.get("holdout", 0)),
})
