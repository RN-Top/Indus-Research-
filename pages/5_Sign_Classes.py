import pandas as pd
import streamlit as st

from indus_workbench import classes, data, ui

st.set_page_config(page_title="Sign Classes", layout="wide")
st.title("Sign Classes")
st.markdown(
    "Signs that do the same job (numbers, variants of one sign, words of one kind) tend to sit "
    "between the same neighbours. Pick a sign to see which signs share its surroundings. This is "
    "how Alice Kober worked out Linear B's structure before anyone knew its sounds."
)

ui.init_settings()
corpus = ui.load_corpus()
ui.sidebar_status(corpus)
if corpus is None:
    st.stop()
seqs = data.explore_only(corpus).sequences
show_glyphs = corpus.source_key == "indus_website"

# --- Positive control --------------------------------------------------------
if show_glyphs:
    x = pd.read_csv(ui.ROOT / "data" / "crosswalk_G_to_P.csv")
    x = x[x["confident"]]
    pairs = [(a, b) for a in x["g_sign"] for b in x["g_sign"]
             if a < b and x.set_index("g_sign").loc[a, "p_sign"] == x.set_index("g_sign").loc[b, "p_sign"]]
    check = classes.variant_check(seqs, pairs)
    if len(check):
        st.subheader("Does the method work? A check against independent evidence")
        st.markdown(
            "The separate CISI transcription treats these pairs as one sign written two ways. If "
            "context really reveals what signs are, each partner should rank near the top of the "
            "other's list. By chance it would rank about halfway down.")
        st.dataframe(check.style.format({"similarity": "{:.3f}", "chance_rank": "{:.0f}"}),
                     hide_index=True, use_container_width=True)

# --- Explore a sign ----------------------------------------------------------
st.subheader("Signs that share a sign's surroundings")
min_count = st.slider("Only signs used at least this many times", 5, 50, 15,
                      help="Rare signs have too few neighbours to compare reliably.")
signs, _ = classes.context_profiles(seqs, min_count)
if not signs:
    st.info("No signs reach that count.")
    st.stop()
pick = st.selectbox("Sign", signs, format_func=lambda s: f"{s}  {ui.glyphs([s])}" if show_glyphs else s)
nb = classes.neighbours(seqs, pick, k=15, min_count=min_count)
if show_glyphs:
    ui.sign_table([{"sign": pick, "sign picture": ui.glyphs([pick]), "similarity": "(chosen sign)",
                    "more similar than": ""}] +
                  [{"sign": r.sign, "sign picture": ui.glyphs([r.sign]), "similarity": f"{r.similarity:.3f}",
                    "more similar than": f"{r.percentile:.0%} of sign pairs"} for r in nb.itertuples()],
                  ["sign", "sign picture", "similarity", "more similar than"])
else:
    st.dataframe(nb, hide_index=True, use_container_width=True)
st.caption("Computed on the exploration split. A list like this is a lead: to test that a group "
           "of signs forms a class, register a 'class_cohesion' hypothesis in the Hypothesis Lab.")
