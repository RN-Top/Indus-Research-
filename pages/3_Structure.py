import altair as alt
import pandas as pd
import streamlit as st

from app_common import ROOT, sidebar, synthetic_banner
from indus import entropy, stats
from indus.comparison import load_comparison
from indus.query import search

st.set_page_config(page_title="Structure", layout="wide")
corpus = sidebar()
st.title("Structure")
synthetic_banner(corpus)

table = corpus.text_table()
with st.expander("Subset", expanded=False):
    c1, c2, c3 = st.columns(3)
    sites = c1.multiselect("Site", sorted(table["site"].dropna().unique()), key="s_sites")
    types = c2.multiselect("Object type", sorted(table["object_type"].dropna().unique()), key="s_types")
    include_synth = c3.toggle("Include synthetic texts", value=True, key="s_synth")
subset = search(table, sites=sites, object_types=types)
if not include_synth:
    subset = subset[~subset["synthetic"]]
texts = subset["signs"].tolist()
if not texts:
    st.warning("No texts in this subset.")
    st.stop()

s = stats.summary(texts)
m = st.columns(6)
m[0].metric("Texts", s["texts"])
m[1].metric("Sign tokens", s["sign_tokens"])
m[2].metric("Sign types", s["sign_types"])
m[3].metric("Seen once", f"{s['hapax_share_of_types']:.0%}", help="Share of sign types that occur only once")
m[4].metric("Median length", f"{s['median_length']:g}")
m[5].metric("Longest text", s["max_length"])
if s["sign_tokens"] == 0:
    st.warning("Every sign in this subset is unreadable, so there is nothing to measure yet.")
    st.stop()
if s["unreadable_tokens"]:
    st.caption(f"{s['unreadable_tokens']} unreadable sign positions are excluded from counts.")

tab_freq, tab_pos, tab_ngram, tab_ent = st.tabs(["Frequency", "Position", "Sequences", "Entropy"])

with tab_freq:
    freq = stats.sign_frequencies(texts)
    fit = stats.zipf_fit(freq)
    st.markdown(
        f"Zipf fit: slope **{fit['slope']:.2f}**, R² {fit['r2']:.2f}. "
        "Word frequencies in natural language give a slope near −1. The slope alone cannot show "
        "whether a sign system is writing."
    )
    c1, c2 = st.columns([3, 2])
    chart = (
        alt.Chart(freq)
        .mark_circle(size=40)
        .encode(
            x=alt.X("rank:Q", scale=alt.Scale(type="log"), title="Rank"),
            y=alt.Y("count:Q", scale=alt.Scale(type="log"), title="Occurrences"),
            tooltip=["sign", "count", alt.Tooltip("share:Q", format=".1%")],
        )
    )
    c1.altair_chart(chart, width="stretch")
    c2.dataframe(freq, hide_index=True, height=360,
                 column_config={"share": st.column_config.NumberColumn(format="percent")})
    lengths = stats.length_distribution(texts)
    st.altair_chart(
        alt.Chart(lengths).mark_bar().encode(x=alt.X("length:O", title="Signs per text"), y=alt.Y("texts:Q", title="Texts")),
        width="stretch",
    )

with tab_pos:
    st.write(
        "Where each sign falls in its text, in reading order. Strong positional preferences, such as "
        "the jar sign at text ends, are among the best-established facts about the script."
    )
    min_count = st.slider("Minimum occurrences", 1, 50, 5, key="pos_min")
    prof = stats.positional_profile(texts, min_count=min_count)
    long = prof.melt(id_vars="sign", value_vars=["solo", "initial", "medial", "final"], var_name="position", value_name="count")
    order = prof["sign"].tolist()
    st.altair_chart(
        alt.Chart(long)
        .mark_bar()
        .encode(
            y=alt.Y("sign:N", sort=order, title=None, axis=alt.Axis(labelOverlap=False)),
            x=alt.X("count:Q", stack="normalize", title="Share of occurrences", axis=alt.Axis(format="%")),
            color=alt.Color("position:N", sort=["initial", "medial", "final", "solo"]),
            order=alt.Order("position:N"),
            tooltip=["sign", "position", "count"],
        )
        .properties(height=alt.Step(20)),
        width="stretch",
    )
    st.dataframe(
        prof[["sign", "total", "initial", "medial", "final", "solo", "dominant"]],
        hide_index=True,
        width="stretch",
    )

with tab_ngram:
    c1, c2 = st.columns(2)
    n = c1.radio("Sequence length", [2, 3, 4], horizontal=True, key="ng_n", format_func=lambda k: f"{k} signs")
    min_c = c2.number_input("Minimum count", 1, 100, 2, key="ng_min")
    grams = stats.ngrams(texts, n, min_count=min_c)
    cov = stats.ngram_coverage(texts, n, top=20)
    st.markdown(f"The 20 most common {n}-sign sequences account for **{cov:.0%}** of all {n}-sign sequences.")
    st.dataframe(grams, hide_index=True, width="stretch",
                 column_config={"share": st.column_config.NumberColumn(format="percent")})

with tab_ent:
    st.write(
        "Conditional entropy measures how predictable the next sign is from the current one, in bits. "
        "Rao et al. (2009) found Indus values within the range of languages; Sproat (2010, 2014) showed "
        "that some non-linguistic symbol systems fall in the same range. Read the corpus curve against "
        "real comparison corpora, not only the artificial controls."
    )
    c1, c2 = st.columns(2)
    mm = c1.toggle("Miller–Madow small-sample correction", value=True, key="ent_mm")
    seed = c2.number_input("Control random seed", 0, 10_000, 0, key="ent_seed")
    max_k = min(s["sign_types"], 400)
    ks = sorted({k for k in [5, 10, 20, 40, 60, 80, 100, 150, 200, 300, 400, max_k] if 2 <= k <= max_k})

    series = {"This corpus": texts}
    for name, make in entropy.CONTROLS.items():
        series[f"Control: {name}"] = make(texts, seed=seed)
    comparisons = load_comparison(ROOT / "data" / "comparison")
    for comp in comparisons:
        series[f"{comp.name} ({comp.kind})"] = comp.texts

    curves = pd.concat(
        [entropy.conditional_entropy_curve(t, ks, mm).assign(series=name) for name, t in series.items()]
    )
    curves["type"] = curves["series"].map(lambda n: "artificial control" if n.startswith("Control") else "corpus")
    st.altair_chart(
        alt.Chart(curves)
        .mark_line(point=True)
        .encode(
            x=alt.X("k:Q", title="Most frequent signs included (k)"),
            y=alt.Y("conditional_entropy:Q", title="Conditional entropy (bits)"),
            color=alt.Color("series:N", title=None),
            strokeDash=alt.StrokeDash("type:N", title=None, sort=["corpus", "artificial control"]),
            tooltip=["series", "k", alt.Tooltip("conditional_entropy:Q", format=".3f")],
        ),
        width="stretch",
    )
    if not comparisons:
        st.info(
            "No comparison corpora loaded yet. Add CSVs to data/comparison/ (see its README) for "
            "linguistic and non-linguistic systems; until then only the artificial controls are shown."
        )

    block = pd.DataFrame(
        [
            {"series": name, "n": n_, "H_n / n": entropy.block_entropy(t, n_, mm) / n_}
            for name, t in series.items()
            for n_ in (1, 2, 3)
        ]
    ).pivot(index="series", columns="n", values="H_n / n")
    block.columns = [f"n = {c}" for c in block.columns]
    st.markdown(
        "**Block entropy per sign** (bits). Values falling with n mean that context makes signs more "
        "predictable. In a small corpus they also fall for random controls, because most longer blocks "
        "are seen only once, so compare each row with the controls rather than reading it alone."
    )
    st.dataframe(block.style.format("{:.3f}"), width="stretch")
    st.caption("Sources: Rao et al. 2009; Sproat 2010, 2014; Yadav et al. 2010. See References.")
