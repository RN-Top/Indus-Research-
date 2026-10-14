import streamlit as st

from indus_workbench import data, ui

st.set_page_config(page_title="Corpus Browser", layout="wide")
st.title("Corpus Browser")

ui.init_settings()
corpus = ui.load_corpus()
ui.sidebar_status(corpus)
if corpus is None:
    st.stop()

show_holdout = st.toggle(
    "Show holdout texts", value=False,
    help="Looking at holdout texts before a confirmatory test weakens that test, because "
         "what you see can shape your hypothesis. Leave this off unless you have finished testing.")
c = corpus if show_holdout else data.explore_only(corpus)
if show_holdout:
    st.warning("Holdout texts are visible. Note this in your methods if you test afterwards.")

df = c.df
f1, f2, f3 = st.columns(3)
sites = f1.multiselect("Site", sorted(df["site"].unique()))
objs = f2.multiselect("Object type", sorted(df["object_type"].unique()))
query = f3.text_input("Contains sign sequence (space-separated, in reading order)",
                      placeholder="e.g. G740 G235")

mask = df.index == df.index
if sites:
    mask &= df["site"].isin(sites)
if objs:
    mask &= df["object_type"].isin(objs)
if query.strip():
    q = query.split()
    mask &= df["signs"].map(lambda s: any(s[i:i + len(q)] == q for i in range(len(s) - len(q) + 1)))

view = df[mask].copy()
view["sequence"] = view["signs"].map(" ".join)
st.caption(f"{len(view):,} texts match.")
st.dataframe(
    view[["text_id", "sequence", "length", "site", "object_type", "motif", "source_ref", "split"]],
    use_container_width=True, height=520, hide_index=True,
)
st.caption("`source_ref` is the catalogue number (CISI) where the source gives one. "
           "Use it to check any text against the published photographs.")
