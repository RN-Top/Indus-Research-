import numpy as np
import pandas as pd
import streamlit as st

from indus_workbench import controls, data, entropy, ui

st.set_page_config(page_title="Entropy Replication", layout="wide")
st.title("Entropy Replication")
st.markdown(
    "This page repeats the block-entropy comparison of **Rao (2010)** and **Rao et al. (2009, "
    "*Science*)**: how predictable are sign sequences, compared with sequences we understand? "
    "Rao found the Indus curve sits between fully random and fully rigid sequences, close to "
    "natural-language scripts.\n\n"
    "**What a match means:** the transcriptions have language-like *flexibility*. It does not "
    "prove the signs encode language; critics (Sproat 2010, 2014) showed some non-linguistic "
    "systems also fall in this range. Treat it as a necessary check, not proof."
)

ui.init_settings()
corpus = ui.load_corpus()
ui.sidebar_status(corpus)
if corpus is None:
    st.stop()

c1, c2, c3 = st.columns(3)
use_all = c1.toggle("Use all texts (not just exploration split)", value=True,
                    help="Entropy is a descriptive replication, not a hypothesis test, so using all "
                         "texts here does not spend the holdout.")
max_n = c2.slider("Largest block size", 2, 6, 4)
mm = c3.toggle("Miller-Madow bias correction", value=False)
n_seeds = st.slider("Random seeds per control (more = steadier)", 3, 30, 10)

seqs = corpus.sequences if use_all else data.explore_only(corpus).sequences
L = len({s for q in seqs for s in q})
lengths = [len(s) for s in seqs]


@st.cache_data(show_spinner="Computing curves…")
def curves(seqs_t, max_n, mm, n_seeds, comparison_t):
    seqs = [list(s) for s in seqs_t]
    L = len({s for q in seqs for s in q})
    out = {"Indus (transcribed)": entropy.block_entropy_curve(seqs, max_n, L, mm)}
    for name, fn in controls.NULL_MODELS.items():
        runs = [entropy.block_entropy_curve(fn(seqs, controls.rng(k)), max_n, L, mm) for k in range(n_seeds)]
        out[f"Negative control: {name.lower()}"] = list(np.mean(runs, axis=0))
    lens = [len(s) for s in seqs]
    runs = [entropy.block_entropy_curve(
        controls.markov_language(len(seqs), lens, L, controls.rng(100 + k)), max_n, L, mm) for k in range(n_seeds)]
    out["Positive control: synthetic grammar (known structure)"] = list(np.mean(runs, axis=0))
    if comparison_t:
        comp = [list(s) for s in comparison_t]
        Lc = len({s for q in comp for s in q})
        out["Comparison text (uploaded)"] = entropy.block_entropy_curve(comp, max_n, Lc, mm)
    return out


st.subheader("Optional: add a known writing system")
st.markdown(
    "Upload a plain-text file (one line per text) in a known script, for example Sumerian "
    "transliterations or Old Tamil, as a real-language positive control. It is cut into pieces "
    "with the same length distribution as the Indus texts so the comparison is fair."
)
up = st.file_uploader("Comparison text (.txt)", type=["txt"])
unit = st.radio("Units", ["char", "word"], horizontal=True,
                format_func=lambda u: "Characters/signs" if u == "char" else "Words")
comparison = None
if up:
    comp = controls.tokenize_text(up.read().decode("utf-8", errors="ignore"), unit)
    comparison = controls.match_lengths(comp, lengths, controls.rng(0))
    st.caption(f"{len(comparison):,} length-matched pieces from the uploaded text.")

res = curves(tuple(map(tuple, seqs)), max_n,
             mm, n_seeds, tuple(map(tuple, comparison)) if comparison else None)

st.subheader("Normalised block entropy")
chart = pd.DataFrame(res, index=pd.Index(range(1, max_n + 1), name="block size"))
chart["Maximum (fully random)"] = list(range(1, max_n + 1))
chart["Minimum (fully rigid)"] = 0.0
st.line_chart(chart)
st.dataframe(chart.style.format("{:.3f}"), use_container_width=True)

st.subheader("How much data each point rests on")
rows = []
for n in range(1, max_n + 1):
    tok, typ = entropy.blocks_available(seqs, n)
    rows.append({"block size": n, "blocks counted": tok, "distinct blocks": typ,
                 "blocks per type": tok / typ if typ else 0})
avail = pd.DataFrame(rows).set_index("block size")
st.dataframe(avail.style.format({"blocks per type": "{:.2f}"}), use_container_width=True)
st.caption("When blocks per type falls near 1, most blocks were seen once and the entropy "
           "estimate is unreliable (biased low). The controls share the same bias, so compare "
           "curves with each other rather than reading absolute values.")

indus = chart["Indus (transcribed)"]
ws = chart["Negative control: shuffle within texts"]
verdict = ("lower than" if indus.iloc[1] < ws.iloc[1] else "not lower than")
st.success(
    f"At block size 2, the Indus curve ({indus.iloc[1]:.3f}) is **{verdict}** the within-text "
    f"shuffle ({ws.iloc[1]:.3f}). Lower means sign order carries information beyond which signs "
    "occur together.")

ui.log_result("entropy", {
    "texts": len(seqs), "alphabet": L, "max_n": max_n, "miller_madow": mm, "seeds": n_seeds,
    "curves": {k: [round(v, 4) for v in vals] for k, vals in res.items()},
    "comparison_uploaded": bool(up),
})
