import pandas as pd
import streamlit as st

from indus_workbench import data, hypotheses as hy, ui

st.set_page_config(page_title="Robustness", layout="wide")
st.title("Robustness")
st.markdown(
    "A finding that only appears under one set of choices is fragile. This page re-runs your "
    "latest explored hypothesis (exploration split only) under every combination of:\n"
    "- damaged texts excluded or included\n"
    "- duplicate texts kept or removed\n"
    "- for the CISI seals, three ways of splitting sign variants\n\n"
    "A result worth registering should point the same way in every row."
)

ui.init_settings()
draft = st.session_state.get("draft")
corpus = ui.load_corpus()
ui.sidebar_status(corpus)
if not draft:
    st.info("Explore a hypothesis in the Hypothesis Lab first.")
    st.stop()

st.json({k: draft[k] for k in ["kind", "params", "source_key"]})
n_perm = st.select_slider("Permutations per run", [200, 500, 1000, 2000], value=500)

sources = [draft["source_key"]]
if draft["source_key"].startswith("cisi"):
    sources = ["cisi_primary", "cisi_hierarchical", "cisi_allograph"]
    st.caption("Sign IDs may differ between the three CISI versions (split variants get new IDs). "
               "A sign missing from a version shows as untestable there, which is itself informative.")

if st.button("Run robustness grid", type="primary"):
    rows = []
    prog = st.progress(0.0)
    combos = [(s, dd, de) for s in sources for dd in (True, False) for de in (False, True)]
    for i, (src, drop_damaged, dedupe) in enumerate(combos):
        c = ui.load_corpus(src, drop_damaged=drop_damaged, dedupe=dedupe)
        if c is None:
            continue
        res = hy.run_test(draft, data.explore_only(c).df, n_perm=n_perm)
        rows.append({"corpus": src, "damaged excluded": drop_damaged, "duplicates removed": dedupe,
                     "texts": data.explore_only(c).n_texts, "observed": res.observed,
                     "null mean": res.null_mean, "effect ratio": res.effect_ratio,
                     "p": res.p_value, "support": res.n_support})
        prog.progress((i + 1) / len(combos))
    df = pd.DataFrame(rows)
    st.dataframe(df, hide_index=True, use_container_width=True)
    ok = df["p"].dropna()
    if len(ok) == len(df) and (ok < draft["alpha"]).all():
        st.success("Same direction and below α in every configuration.")
    elif (ok < draft["alpha"]).any():
        st.warning("The result depends on data choices. Report this, and think about why.")
    else:
        st.info("Not significant in any configuration.")
    ui.log_result("robustness", {"hypothesis": {k: draft[k] for k in ["kind", "params"]},
                                 "rows": rows})
