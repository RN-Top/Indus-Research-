import numpy as np
import pandas as pd
import streamlit as st

from indus_workbench import controls, data, stats, ui

st.set_page_config(page_title="Sign Statistics", layout="wide")
st.title("Sign Statistics")
st.caption("Computed on the exploration split only.")

ui.init_settings()
corpus = ui.load_corpus()
ui.sidebar_status(corpus)
if corpus is None:
    st.stop()
seqs = data.explore_only(corpus).sequences

freq = stats.sign_frequencies(seqs)
singletons = int((freq["tokens"] == 1).sum())
c = st.columns(3)
c[0].metric("Distinct signs", f"{len(freq):,}")
c[1].metric("Signs seen only once", f"{singletons:,}")
c[2].metric("Top 20 signs' share of all tokens", f"{freq['share'].head(20).sum():.0%}")
st.caption("Many rare signs is normal for small corpora, but it limits what can be tested: "
           "the Hypothesis Lab marks results resting on fewer than 5 occurrences as inconclusive.")

st.subheader("Most frequent signs")
if corpus.source_key == "indus_website":
    ui.sign_table([{"rank": i + 1, "sign": r.sign, "sign picture": ui.glyphs([r.sign]), "uses": r.tokens,
                    "texts": r.texts} for i, r in enumerate(freq.head(20).itertuples())],
                  ["rank", "sign", "sign picture", "uses", "texts"])
st.bar_chart(freq.head(40).set_index("sign")["tokens"], color=ui.CARNELIAN)
if corpus.source_key == "indus_website":
    freq["CISI P-number"] = freq["sign"].map(ui.crosswalk()).fillna("")
st.dataframe(freq, use_container_width=True, height=300, hide_index=True)

st.subheader("Text lengths")
st.bar_chart(stats.length_distribution(seqs), color=ui.CARNELIAN)

st.subheader("Where signs sit in a text")
st.markdown(
    "Share of each sign's tokens at the start, middle or end of texts with 2 or more signs, "
    "beside what a **within-text shuffle** gives (the negative control). A sign whose observed "
    "share is far above its shuffled share has a real positional preference. Test it formally "
    "in the Hypothesis Lab."
)
min_n = st.slider("Minimum occurrences", 5, 200, 20)
obs = stats.positional_profile(seqs)
r = controls.rng(0)
null_runs = [stats.positional_profile(controls.shuffle_within_texts(seqs, r)) for _ in range(20)]
null = sum(n[["start_share", "end_share"]].reindex(obs.index).fillna(0) for n in null_runs) / len(null_runs)
table = pd.DataFrame({
    "occurrences": obs["n"],
    "start (observed)": obs["start_share"], "start (shuffled)": null["start_share"],
    "end (observed)": obs["end_share"], "end (shuffled)": null["end_share"],
})
table = table[table["occurrences"] >= min_n]
table["end − shuffled"] = table["end (observed)"] - table["end (shuffled)"]
table["start − shuffled"] = table["start (observed)"] - table["start (shuffled)"]
st.dataframe(table.sort_values("end − shuffled", ascending=False).style.format(
    {c: "{:.2f}" for c in table.columns if c != "occurrences"}), use_container_width=True, height=400)
