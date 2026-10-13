"""Streamlit helpers shared by every page: corpus selection, caching, banners."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from indus import Corpus, load_corpus

ROOT = Path(__file__).resolve().parent
CORPORA = {
    "Open sample": ROOT / "data" / "sample",
    "Private corpus (data/private, local only)": ROOT / "data" / "private",
}


@st.cache_data(show_spinner="Loading corpus…")
def _load(path: str, name: str) -> Corpus:
    return load_corpus(path, name=name)


def available_corpora() -> dict[str, Path]:
    return {k: v for k, v in CORPORA.items() if (v / "texts.csv").exists()}


def sidebar() -> Corpus:
    """Render the corpus picker in the sidebar and return the chosen corpus."""
    options = available_corpora()
    choice = st.sidebar.selectbox("Corpus", list(options), key="corpus_choice")
    corpus = _load(str(options[choice]), choice)
    st.sidebar.caption(f"{len(corpus.texts)} texts · {len(corpus.objects)} objects · {len(corpus.signs)} signs")
    if corpus.errors:
        st.sidebar.warning(f"{len(corpus.errors)} data problems found. See Home for details.")
    return corpus


def synthetic_banner(corpus: Corpus) -> None:
    n_synth = int(corpus.texts["synthetic"].sum())
    if n_synth:
        st.info(
            f"{n_synth} of the {len(corpus.texts)} texts in this corpus are synthetic placeholders generated to exercise "
            "the app. They are not Indus inscriptions, and results computed on them say nothing "
            "about the script."
        )
