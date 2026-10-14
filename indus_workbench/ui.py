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


@st.cache_data(show_spinner="Loading corpus…", ttl=None)
def _raw(source_key: str) -> tuple[bytes, str]:
    return data.load_raw(source_key)


# Indus palette, shared by the CSS below and by charts.
CARNELIAN = "#A4442A"
LAPIS = "#2F4A7A"
OCHRE = "#C08A3E"
UMBER = "#2E2118"
CLAY = "#EDE0CC"

_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&display=swap');
h1, h2, h3 {{ font-family: 'Cormorant Garamond', Georgia, serif !important; color: {UMBER};
              letter-spacing: 0.01em; }}
h1 {{ font-weight: 700 !important; }}
/* A row of incised lozenges under each page title, like the border of a seal. */
h1::after {{ content: ""; display: block; height: 10px; margin-top: 6px;
  background: repeating-linear-gradient(135deg, {CARNELIAN} 0 2px, transparent 2px 9px),
              repeating-linear-gradient(45deg, {CARNELIAN} 0 2px, transparent 2px 9px);
  opacity: 0.35; max-width: 240px; }}
[data-testid="stSidebar"] {{ border-right: 3px double {OCHRE}; }}
[data-testid="stMetric"] {{ background: {CLAY}; border-left: 4px solid {CARNELIAN};
  border-radius: 6px; padding: 10px 14px; }}
a, a:visited {{ color: {LAPIS}; }}
.indus-hero {{ background: linear-gradient(135deg, #8E3A23 0%, {CARNELIAN} 55%, {OCHRE} 100%);
  color: #FBF5EA; border-radius: 10px; padding: 22px 24px; margin-bottom: 18px; }}
.indus-hero h2 {{ color: #FBF5EA !important; margin: 0 0 4px 0; font-size: 2rem; }}
.indus-hero p {{ margin: 0; opacity: 0.92; }}
</style>
"""


def apply_theme() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def hero(title: str, subtitle: str) -> None:
    st.markdown(f'<div class="indus-hero"><h2>{title}</h2><p>{subtitle}</p></div>',
                unsafe_allow_html=True)


DEFAULTS = {"source_key": "indus_website", "drop_damaged": True, "dedupe": False,
            "drop_unidentified": True}


def init_settings() -> None:
    """Call at the top of every page, before any widget.

    Re-assigning the keys stops Streamlit from discarding the Home page's
    widget values when the user moves to another page."""
    apply_theme()
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
        raw, origin = _raw(key)
    except Exception as e:  # network error or failed integrity check
        st.error(f"Could not load the corpus ({key}): {e}")
        return None
    c = data.build_corpus(raw, key, drop_damaged=s["drop_damaged"], dedupe=s["dedupe"],
                          drop_unidentified=s["drop_unidentified"],
                          collapse_variants=data.SOURCES[key].get("collapse_variants", False))
    c.settings["loaded_from"] = origin
    return c


def sidebar_status(corpus: data.Corpus | None) -> None:
    with st.sidebar:
        st.caption(f"Workbench v{__version__}")
        if corpus is None:
            return
        st.caption(
            f"**Data:** {corpus.source_key}  \n"
            f"{corpus.n_texts:,} texts · {corpus.n_tokens:,} signs  \n"
            f"Damaged texts {'excluded' if corpus.settings['drop_damaged'] else 'included'} · "
            f"duplicates {'removed' if corpus.settings['dedupe'] else 'kept'} · "
            f"unidentified signs {'excluded' if corpus.settings['drop_unidentified'] else 'kept'}  \n"
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
