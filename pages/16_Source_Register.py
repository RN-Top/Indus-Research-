"""Source register: every source we have logged, with its licence status and what it allows.

Read-only. Reads data/own_corpus/source_log.csv. A source counts as usable only when its
licence_status is checked and can_record_our_reading_now says yes.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

from indus_workbench import ui

st.set_page_config(page_title="Source Register", layout="wide")
st.title("Source register")
ui.init_settings()

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "data" / "own_corpus" / "source_log.csv"

st.markdown(
    "Every source we have logged, with what its licence allows. A source is usable for readings only "
    "when its licence is checked **and** the log says we can record our reading now. Anything else is "
    "blocked, and the next action says what would unblock it."
)

df = pd.read_csv(LOG, dtype=str).fillna("")
usable = df["can_record_our_reading_now"].str.strip().str.lower().str.startswith("yes")
c1, c2, c3 = st.columns(3)
c1.metric("Sources logged", len(df))
c2.metric("Usable now", int(usable.sum()))
c3.metric("Blocked or unclear", int((~usable).sum()))

show = st.radio("Show", ["All", "Usable now", "Blocked or unclear"], horizontal=True)
view = df if show == "All" else df[usable] if show == "Usable now" else df[~usable]
st.dataframe(
    view[["source", "licence_status", "can_record_our_reading_now", "status", "next_action"]],
    use_container_width=True,
    hide_index=True,
)

with st.expander("Full evidence for each source"):
    for _, row in view.iterrows():
        st.markdown(f"**{row['source']}**")
        st.markdown(f"- Locator: {row['locator']}")
        st.markdown(f"- Licence evidence: {row['licence_evidence']}")
        if row["notes"]:
            st.markdown(f"- Notes: {row['notes']}")
