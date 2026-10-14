"""Shared Streamlit helpers: data loading, settings, the report log."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from . import __version__, data

ROOT = Path(__file__).resolve().parent.parent
HYPOTHESIS_DIR = ROOT / "hypotheses"

DISCLAIMER = (
    "The Indus script is **undeciphered**. This app does not decipher it. It measures "
    "patterns in transcribed sign sequences and tests each one against controls. "
    "Results describe the transcriptions, which carry their editors' choices about how to "
    "identify and split signs."
)


@st.cache_data(show_spinner="Downloading corpus…", ttl=None)
def _raw(url: str) -> bytes:
    return data.fetch(url)


DEFAULTS = {"source_key": "indus_website", "drop_damaged": True, "dedupe": False}


def init_settings() -> None:
    """Call at the top of every page, before any widget.

    Re-assigning the keys stops Streamlit from discarding the Home page's
    widget values when the user moves to another page."""
    ss = st.session_state
    for k, v in DEFAULTS.items():
        ss[k] = ss.get(k, v)


def settings() -> dict:
    ss = st.session_state
    return {k: ss.get(k, v) for k, v in DEFAULTS.items()}


def load_corpus(source_key: str | None = None, **overrides) -> data.Corpus | None:
    s = settings()
    s.update(overrides)
    key = source_key or s["source_key"]
    try:
        raw = _raw(data.SOURCES[key]["url"])
    except Exception as e:  # network or HTTP error
        st.error(f"Could not download the corpus ({key}): {e}")
        return None
    return data.build_corpus(raw, key, drop_damaged=s["drop_damaged"], dedupe=s["dedupe"])


def sidebar_status(corpus: data.Corpus | None) -> None:
    with st.sidebar:
        st.caption(f"Workbench v{__version__}")
        if corpus is None:
            return
        st.caption(
            f"**Data:** {corpus.source_key}  \n"
            f"{corpus.n_texts:,} texts · {corpus.n_tokens:,} signs  \n"
            f"Damaged texts {'excluded' if corpus.settings['drop_damaged'] else 'included'} · "
            f"duplicates {'removed' if corpus.settings['dedupe'] else 'kept'}  \n"
            f"SHA-256 `{corpus.sha256[:12]}…`"
        )
        st.caption("Change these on the Home page.")


def log_result(section: str, payload: dict) -> None:
    """Record a result for the methods report."""
    payload = dict(payload)
    payload["recorded_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    st.session_state.setdefault("report", {})[section] = payload


def load_registered() -> list[dict]:
    out = []
    if HYPOTHESIS_DIR.exists():
        for p in sorted(HYPOTHESIS_DIR.glob("*.json")):
            try:
                h = json.loads(p.read_text())
                h["_file"] = p.name
                out.append(h)
            except json.JSONDecodeError:
                st.warning(f"Could not read {p.name}")
    return out
