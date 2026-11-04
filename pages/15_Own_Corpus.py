"""Own corpus: the texts we transcribe ourselves, under fixed rules.

Read-only view. Rows are added to data/own_corpus/corpus_template.csv by hand, one reading
at a time, so each row keeps its source locator and licence.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

from indus_workbench import ui

st.set_page_config(page_title="Own Corpus", layout="wide")
st.title("Own Corpus")

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "own_corpus" / "corpus_template.csv"
RULES = ROOT / "data" / "own_corpus" / "RULES.md"

ui.init_settings()

st.markdown(
    "Texts we read ourselves from published sources, under rules written before any text was "
    "chosen. Every row has a source locator, a licence, our reading, and the published reading "
    "kept separate. Held-out rows are for scoring predictions only."
)

if CORPUS.exists():
    df = pd.read_csv(CORPUS, dtype=str).fillna("")
else:
    df = pd.DataFrame()

n = len(df)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", n)
c2.metric("Dev rows", int((df.get("split", pd.Series(dtype=str)) == "dev").sum()) if n else 0)
c3.metric("Held rows", int((df.get("split", pd.Series(dtype=str)) == "held").sum()) if n else 0)
c4.metric("With our reading", int((df.get("reading_G_numbers", pd.Series(dtype=str)) != "").sum()) if n else 0)

if n == 0:
    st.info(
        "No texts yet. The corpus is waiting on sources that meet the licence rule. "
        "Once rows are added to data/own_corpus/corpus_template.csv, they appear here."
    )
else:
    st.subheader("Rows")
    st.dataframe(df, use_container_width=True, hide_index=True)

    if "object_family" in df and (df["object_family"] != "").any():
        st.subheader("By object family")
        st.bar_chart(df["object_family"].value_counts())

    if "reader" in df:
        readers = df["reader"].replace("", "unrecorded").value_counts()
        st.caption(
            f"Readers: {', '.join(f'{k} ({v})' for k, v in readers.items())}. "
            "A corpus read by one person is single-reader and cannot be called confirmed."
        )


st.subheader("How a text gets into the corpus")
st.graphviz_chart('''
digraph G {
  rankdir=LR;
  node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=11, color="#555555"];
  edge [color="#888888", fontname="Helvetica", fontsize=9];
  src   [label="1. Source\nopen-access report,\ncatalogue or paper", fillcolor="#eef3fb"];
  lic   [label="2. Licence check\nreuse allowed?", shape=diamond, fillcolor="#fff6e0"];
  excl  [label="exclusions.csv\n(logged, not used)", fillcolor="#fbeaea"];
  loc   [label="3. Locator recorded\npage, figure, museum no.", fillcolor="#eef3fb"];
  read  [label="4. Our reading\nG-numbers, ? for unclear\nno copying published reading", fillcolor="#eef3fb"];
  split [label="5. Fixed-seed split\ndev or held", shape=diamond, fillcolor="#fff6e0"];
  dev   [label="dev rows\nexploratory only", fillcolor="#f2f2f2"];
  pre   [label="6. Prediction hashed\nbefore held rows are read", fillcolor="#eef3fb"];
  held  [label="held rows\nscored once", fillcolor="#e6f4ea"];
  ctrl  [label="7. Controls\nobject family and site", fillcolor="#eef3fb"];
  src -> lic -> loc [label="yes"];
  lic -> excl [label="no"];
  loc -> read -> split;
  split -> dev [label="dev"];
  split -> pre [label="held"];
  pre -> held -> ctrl;
}
''', use_container_width=True)

st.subheader("Rules")
if RULES.exists():
    st.markdown(RULES.read_text())
else:
    st.warning("RULES.md not found in data/own_corpus/.")
