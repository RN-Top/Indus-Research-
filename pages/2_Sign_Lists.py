import streamlit as st

from app_common import sidebar

st.set_page_config(page_title="Sign Lists", layout="wide")
corpus = sidebar()
st.title("Sign Lists")
st.write(
    "Published inventories range from under 400 to about 700 signs because scholars split variants "
    "differently. Each text records which list it was transcribed under, and this table maps the "
    "working IDs to Mahadevan (1977), Parpola (1994) and Wells (2015) numbers where they have been checked."
)

signs = corpus.signs.merge(corpus.crosswalk.drop(columns="source"), on="sign_id", how="left")
counts = corpus.texts["signs"].explode().value_counts()
signs["occurrences"] = signs["sign_id"].map(counts).fillna(0).astype(int)

classes = st.multiselect("Graphic class", sorted(signs["graphic_class"].unique()), key="classes")
view = signs[signs["graphic_class"].isin(classes)] if classes else signs
st.dataframe(
    view[["sign_id", "label", "graphic_class", "mahadevan", "parpola", "wells", "occurrences", "sign_list", "source"]],
    hide_index=True,
    width="stretch",
)
missing = (signs[["mahadevan", "parpola", "wells"]] == "").all(axis=1).sum()
st.caption(f"{missing} of {len(signs)} signs have no checked cross-reference yet.")
