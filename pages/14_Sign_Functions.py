"""Sign functions: what the opening and closing signs seem to do, with the sign pictures.

Summarises results/heading_types.md, results/closer_category_test.md,
results/closer_categories_ext.md and results/copper_closer_test.md. Each row says
whether the finding is confirmed on the locked holdout or exploratory only.
"""

import streamlit as st

from indus_workbench import ui

st.set_page_config(page_title="Sign Functions", layout="wide")
ui.init_settings()
st.title("Sign Functions")
st.markdown(
    "What particular signs seem to *do* in an inscription, judged only from where they sit and what objects "
    "they appear on. This says nothing about how the signs were pronounced or what they meant. "
    "**Confirmed** means a test registered in advance and run once on the locked holdout; "
    "**exploratory** means a pattern in the exploration texts that has not been tested that way.")
if not ui.glyph_map():
    st.info("Sign pictures need `data/glyph_map.csv`; codes are shown alone.")

st.header("1. The opening: two heading families")
st.caption("An opener is followed by one of two cluster-closing signs, and which one is nearly fixed. "
           "Source: `results/heading_types.md` (exploratory).")
heads = [
    ("G817", "G2", "78 texts; next sign G2 in 67", "Family A"),
    ("G861", "G2", "83 texts; next sign G2 in 73", "Family A"),
    ("G820", "G2", "92 texts; G2 in 56, G60 in 15", "Family A (mostly)"),
    ("G920", "G60", "50 texts; next sign G60 in 37", "Family B"),
    ("G692", "G60", "25 texts; next sign G60 in 19", "Family B"),
]
ui.sign_table([{"family": f, "opener": o, "sign picture": ui.glyphs([o, n]), "pair": f"{o} + {n}", "evidence": e,
                "status": "exploratory"} for o, n, e, f in heads],
              ["family", "opener", "pair", "sign picture", "evidence", "status"])

st.header("2. The ending: generic and specific closers")
st.caption("Sources: `results/closer_category_test.md`, `results/closer_categories_ext.md`, `results/copper_closer_test.md`.")
closers = [
    ("G740", "Generic ending (the 'jar'). About a third of all texts; no site, object or animal of its own.", "exploratory"),
    ("G400", "Tablets, and Harappa. Holds within sites and within object types.", "exploratory"),
    ("G407", "Copper tablets of Mohenjo-daro (with G617). Also on ordinary steatite seals.", "confirmed (3 of 20 holdout texts copper, q = 0.0055)"),
    ("G617", "Copper tablets of Mohenjo-daro (with G407).", "confirmed, jointly with G407"),
    ("G527", "Leans to Lothal on a few texts; does not survive the confound check.", "weak lead"),
]
ui.sign_table([{"sign": s, "sign picture": ui.glyphs([s]), "what it goes with": w, "status": t} for s, w, t in closers],
              ["sign", "sign picture", "what it goes with", "status"])
st.caption("A '·' means the sign font has no picture for that code (G617 is one).")

st.header("3. The layout these fill")
st.markdown(
    "**[opener + G2 or G60]** → **[content, mostly unique]** → **[closer, usually G740, sometimes a specific mark]**. "
    "This matches the shape of Mesopotamian seal legends (*seal of / king* → *owner, title, father* → *your servant / god*), "
    "which is an analogy, not a translation (`results/seal_function_comparison.md`).")
st.caption("Pictures use the SK Indus Script font (Shabir Kumbhar; loaded from its public source, not stored here). "
           "Indus texts usually read right to left; pictures follow the transcription's order.")
