import streamlit as st

from app_common import sidebar, synthetic_banner
from indus.query import PatternError, search

st.set_page_config(page_title="Corpus Browser", layout="wide")
corpus = sidebar()
st.title("Corpus Browser")
synthetic_banner(corpus)

table = corpus.text_table()

with st.form("search"):
    pattern = st.text_input(
        "Sign sequence",
        key="pattern",
        placeholder="e.g.  FISH JAR   ·   ^ STROKE2 FISH   ·   FISH ... JAR $",
        help="Signs in reading order, separated by spaces. ^ = start of text, $ = end, "
        "* = any one sign, ... = any number of signs.",
    )
    f1, f2, f3 = st.columns(3)
    sites = f1.multiselect("Site", sorted(table["site"].dropna().unique()), key="sites")
    types = f2.multiselect("Object type", sorted(table["object_type"].dropna().unique()), key="types")
    icon = f3.text_input("Iconography contains", key="icon", placeholder="e.g. unicorn, tiger")
    st.form_submit_button("Search")

try:
    results = search(table, pattern, sites, types, icon)
except PatternError as e:
    st.error(f"{e} Use sign IDs from the Sign Lists page.")
    st.stop()

st.write(f"**{len(results)}** of {len(table)} texts match.")
st.dataframe(
    results[["text_id", "site", "object_type", "iconography", "sequence", "length", "confidence", "synthetic"]],
    hide_index=True,
    width="stretch",
    column_config={"sequence": st.column_config.TextColumn("Signs (reading order)", width="large")},
)

st.subheader("Text detail")
if len(results):
    text_id = st.selectbox("Text", results["text_id"], key="detail_text")
    row = results.set_index("text_id").loc[text_id]
    d1, d2 = st.columns(2)
    with d1:
        st.markdown(f"**Signs:** `{row['sequence']}`")
        st.markdown(f"**Direction:** {row['direction']} · **Confidence:** {row['confidence']}")
        st.markdown(f"**Object:** {row['object_id']} ({row['object_type']}, {row['material'] or 'material unknown'})")
        st.markdown(f"**Site:** {row['site']} · **Iconography:** {row['iconography'] or 'none recorded'}")
    with d2:
        ids = {"CISI": row["cisi_id"], "Mahadevan": row["mahadevan_id"], "ICIT": row["icit_id"]}
        st.markdown("**Catalogue numbers:** " + (", ".join(f"{k} {v}" for k, v in ids.items() if v) or "not yet recorded"))
        st.markdown(f"**Source:** {row['source']}")
        if row["image_licence"]:
            st.markdown(f"**Image:** {row['image_licence']}")
        if row["notes"]:
            st.markdown(f"**Notes:** {row['notes']}")
