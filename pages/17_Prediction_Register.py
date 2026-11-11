"""Prediction register: every pre-registered prediction, its SHA-256 hash, and whether a result exists.

Read-only. A prediction counts as run only when a results file in results/ names it.
The hash is computed from the file as it is in the repo now; if it changes, the hash changes,
so compare it with the hash recorded when the prediction was committed.
"""

import hashlib
from pathlib import Path

import pandas as pd
import streamlit as st

from indus_workbench import ui

st.set_page_config(page_title="Prediction Register", layout="wide")
st.title("Prediction register")
ui.init_settings()

ROOT = Path(__file__).resolve().parents[1]
PRED = ROOT / "predictions"
RESULTS = ROOT / "results"

st.markdown(
    "Every prediction written down before its test was run, with its hash. A prediction is "
    "**run** only when a file in `results/` names it. Predictions with no result are not yet tested, "
    "and that is shown as such."
)

result_texts = {p.name: p.read_text(encoding="utf-8", errors="ignore") for p in RESULTS.glob("*.md")}

rows = []
for p in sorted(PRED.iterdir()):
    if p.suffix not in {".json", ".md"} or not p.is_file():
        continue
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    stem = p.stem
    named_in = [name for name, text in result_texts.items() if stem in text]
    rows.append(
        {
            "prediction": p.name,
            "sha256 (first 12)": digest[:12],
            "status": "run (see results)" if named_in else "not run yet",
            "results that name it": ", ".join(named_in) if named_in else "",
        }
    )

df = pd.DataFrame(rows)
run = (df["status"] == "run (see results)").sum() if len(df) else 0
c1, c2, c3 = st.columns(3)
c1.metric("Predictions", len(df))
c2.metric("Run", int(run))
c3.metric("Not run yet", int(len(df) - run))

st.dataframe(df, use_container_width=True, hide_index=True)

with st.expander("Full SHA-256 hashes"):
    for p in sorted(PRED.iterdir()):
        if p.suffix in {".json", ".md"} and p.is_file():
            st.markdown(f"`{hashlib.sha256(p.read_bytes()).hexdigest()}`  {p.name}")
