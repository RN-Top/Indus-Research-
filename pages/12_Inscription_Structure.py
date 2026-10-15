"""Inscription structure: opener -> content -> closer, across sites and transcriptions.

Shows the exploratory results saved in results/ (functional_skeleton.json,
cisi_skeleton_check.json). Nothing here is a confirmatory (holdout) result.
"""

import json

import pandas as pd
import streamlit as st

from indus_workbench import ui

st.set_page_config(page_title="Inscription Structure", layout="wide")
ui.init_settings()
st.title("Inscription Structure")
st.success(
    "**Confirmed on the locked holdout (15 October 2026).** Roles learned from Mohenjo-daro put **76.1%** of "
    "138 unseen texts from other sites in slot order, against 26.7% shuffled (p = 0.0005, BH q = 0.0006 across "
    "all 14 confirmatory tests). Registered before running as `H-2026-10-15-0c595386`; see "
    "`results/confirmatory_2026-10-14.md`, fifth batch. Preprint: [doi:10.5281/zenodo.23404360](https://doi.org/10.5281/zenodo.23404360). "
    "The tables below are the exploratory work that led to it.")

R = ui.ROOT / "results"
sk = json.loads((R / "functional_skeleton.json").read_text())
cisi = json.loads((R / "cisi_skeleton_check.json").read_text())

st.markdown(
    "Indus inscriptions follow a fixed layout: **opening sign(s) → content (often a number and the thing "
    "counted) → closing sign(s)**. A text *conforms* if its opener, middle and closer signs never appear "
    "out of that order. Shuffling each text's signs shows how often that would happen by chance.")

# --- 1. Roles ----------------------------------------------------------------
st.header("1. Which signs open and close")
rule = sk["rule"]
st.caption(
    f"Rule (frozen): a sign used at least {rule['min_tokens']} times is an **opener** if it starts at least "
    f"{rule['open_share']:.0%} of its texts and at least {rule['ratio']}× the shuffled rate; a **closer** if it "
    f"ends at least {rule['close_share']:.0%} and at least {rule['ratio']}×. Numerals are classed by shape. "
    "Learned from Mohenjo-daro texts only.")
roles = pd.DataFrame(sk["roles_Mohenjo-daro"])
if len(roles):
    roles["share"] = roles.apply(lambda r: r["starts"] if r["role"] == "opener" else r["ends"], axis=1)
    show = roles[["role", "sign", "tokens", "share", "shuffled"]].sort_values(["role", "tokens"],
                                                                             ascending=[True, False])
    if ui.glyph_map():
        t = show.copy()
        t.insert(2, "sign picture", t["sign"].map(lambda s: ui.glyphs([s])))
        t["share"] = t["share"].map("{:.0%}".format)
        t["shuffled"] = t["shuffled"].map("{:.0%}".format)
        t = t.rename(columns={"share": "starts/ends", "tokens": "uses"})
        ui.sign_table(t.to_dict("records"), list(t.columns))
    else:
        st.dataframe(show.style.format({"share": "{:.0%}", "shuffled": "{:.0%}"}), hide_index=True)

# --- 2. Across sites -----------------------------------------------------------
st.header("2. The same structure at every site")
src = st.radio("Roles learned from", ["Mohenjo-daro", "Harappa", "all other sites (leave one out)"],
               horizontal=True)
key = {"Mohenjo-daro": "Mohenjo-daro", "Harappa": "Harappa"}.get(src, "LOSO")
rows = sk["transfer"][key]["rows"]
tab = pd.DataFrame([
    {"site": s, "texts scored": r["n"], "in order": r["rate"], "shuffled": r["null"],
     "chance-corrected": r["kappa"],
     "note": "own site, split-half" if s == key else ""}
    for s, r in rows.items() if r.get("rate") is not None])
st.dataframe(tab.style.format({"in order": "{:.1%}", "shuffled": "{:.1%}", "chance-corrected": "{:.2f}"}),
             hide_index=True, use_container_width=True)
st.bar_chart(tab.set_index("site")[["in order", "shuffled"]])
pooled = sk["transfer"][key]["pooled"]
st.caption(f"Pooled over sites other than the source: {pooled['rate']:.1%} of {pooled['n']} texts in order, "
           f"against {pooled['null']:.1%} shuffled. Chance-corrected: 0 = chance, 1 = every text in order.")

with st.expander("Robustness: change the thresholds"):
    rob = pd.DataFrame([{**r["rule"], "openers": r["openers"], "closers": r["closers"],
                         "in order": r["rate"], "texts": r["n"], "shuffled": r["null"]}
                        for r in sk["robustness"]])
    st.dataframe(rob.style.format({"in order": "{:.1%}", "shuffled": "{:.1%}"}), hide_index=True,
                 use_container_width=True)
    d = sk["duplicates_kept"]
    st.caption(f"With duplicate inscriptions kept: {d['rate']:.1%} of {d['n']} in order, "
               f"against {d['null']:.1%} shuffled.")

# --- 3. Independent transcription --------------------------------------------
st.header("3. An independent transcription agrees (CISI)")
st.markdown(
    f"The same frozen roles, translated into the **CISI** transcription's own sign numbers, applied to "
    f"Mohenjo-daro seals transcribed independently: **{cisi['observed']:.1%} of {cisi['scorable']} seals in "
    f"order**, against {cisi['shuffled']:.1%} shuffled (p = {cisi['p']:.4f}). Seals in either corpus's "
    "holdout were excluded.")
st.caption("Limit: same city, and partly the same physical seals, as the roles came from. This checks the "
           "transcription, not other sites. "
           f"Role signs without a confident crosswalk match: {sum(len(v) for v in cisi['unmapped'].values())}.")

# --- 4. Credit and limits ----------------------------------------------------
st.header("4. Prior work and limits")
st.markdown(
    "- **The layout itself is not new.** Bryan Wells and Andreas Fuls described initial signs, an *initial "
    "cluster terminal marker* (sign 2) and *terminal markers* (740, 520, 400 and others) in the ICIT "
    "database and its documentation. This work adds statistical tests against shuffled texts, a frozen "
    "rule, transfer across sites and agreement across transcriptions.\n"
    "- **Not shown:** what any slot means, whether the script records a language, or whether sites used "
    "it at the same time (the corpus has no dates).\n"
    "- **Data:** one website transcription (G-numbers, which follow Wells's sign list) and the CISI file. "
    "Full details in `results/functional_by_site.md` and `results/cisi_skeleton_check.md`.")
