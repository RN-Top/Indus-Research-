import altair as alt
import pandas as pd
import streamlit as st
from pydantic import ValidationError

from app_common import ROOT, sidebar, synthetic_banner
from indus.hypothesis import (
    Hypothesis,
    LexEntry,
    MatchMode,
    Scorer,
    compare_to_null,
    heldout_ids,
    load_hypotheses,
    null_distribution,
    segment,
    trivial_forms,
)

HYP_DIR = ROOT / "hypotheses"
METRICS = {
    "char_coverage": "Share of reading covered by lexicon words",
    "full_match_rate": "Share of texts read entirely as lexicon words",
}
MODES = {
    MatchMode.exact: "Exact spelling",
    MatchMode.no_diacritics: "Ignore diacritics (ā = a)",
    MatchMode.consonants: "Consonants only",
}

st.set_page_config(page_title="Hypothesis Workbench", layout="wide")
corpus = sidebar()
st.title("Hypothesis Workbench")
synthetic_banner(corpus)
st.write(
    "A hypothesis assigns a value to each sign and names a lexicon of words in the proposed language, "
    "each with its source. The test applies the key to every text and asks whether the readings contain "
    "lexicon words more often than keys made by shuffling the same values among signs of similar "
    "frequency. Lock a hypothesis before testing it on held-out texts."
)

# Choose ----------------------------------------------------------------------

saved = load_hypotheses(HYP_DIR)
if "pending_choice" in st.session_state:
    st.session_state["hyp_choice"] = st.session_state.pop("pending_choice")
c1, c2 = st.columns([2, 1])
choice = c1.selectbox("Hypothesis", ["New hypothesis", *saved], key="hyp_choice")
upload = c2.file_uploader("Or upload a hypothesis JSON", type="json", key="hyp_upload")

if upload is not None:
    try:
        base = Hypothesis.model_validate_json(upload.getvalue())
    except ValidationError as e:
        st.error(f"That file is not a valid hypothesis: {e.errors()[0]['msg']}")
        st.stop()
elif choice == "New hypothesis":
    base = Hypothesis(name="Untitled hypothesis")
else:
    base = saved[choice]

status_style = {"locked": "green", "exploratory": "orange", "changed after lock": "red"}
st.markdown(
    f"Status: :{status_style[base.status]}[**{base.status}**]"
    + (f" · locked {base.locked_at} · `{base.locked_hash[:12]}`" if base.locked_hash else "")
)
if base.description:
    st.caption(base.description)

# Edit ------------------------------------------------------------------------

locked = base.status == "locked"
form_key = f"edit::{base.name}::{base.locked_hash}"
with st.expander("Key, lexicon and settings", expanded=not locked):
    if locked:
        st.info("This hypothesis is locked, so it stays exactly as tested. Make an editable copy to change it.")
        if st.button("Make an editable copy", key="copy"):
            copy = base.model_copy(update={"name": f"{base.name} (revised)", "locked_at": None, "locked_hash": None})
            copy.save(HYP_DIR)
            st.session_state["pending_choice"] = copy.name
            st.rerun()
    m1, m2, m3 = st.columns(3)
    name = m1.text_input("Name", base.name, disabled=locked, key=f"{form_key}::name")
    language = m2.text_input("Proposed language", base.language, disabled=locked, key=f"{form_key}::lang")
    author = m3.text_input("Author", base.author, disabled=locked, key=f"{form_key}::author")
    description = st.text_area("Description and argument", base.description, disabled=locked, key=f"{form_key}::desc", height=80)

    signs = corpus.signs[["sign_id", "label"]].copy()
    signs["value"] = signs["sign_id"].map(base.key).fillna("")
    k1, k2 = st.columns(2)
    with k1:
        st.markdown("**Key**: value for each sign (leave blank if unassigned)")
        key_df = st.data_editor(
            signs, hide_index=True, disabled=True if locked else ["sign_id", "label"], key=f"{form_key}::key", height=360, width="stretch"
        )
    with k2:
        st.markdown("**Lexicon**: target-language forms, each with a source")
        lex = pd.DataFrame([e.model_dump() for e in base.lexicon], columns=["form", "gloss", "source"])
        lex_df = st.data_editor(lex, num_rows="fixed" if locked else "dynamic", disabled=locked, hide_index=True, key=f"{form_key}::lex", height=360, width="stretch")
    s1, s2, s3 = st.columns(3)
    mode = s1.selectbox(
        "Spelling match", list(MODES), index=list(MODES).index(base.match_mode),
        format_func=MODES.get, disabled=locked, key=f"{form_key}::mode",
    )
    frac = s2.slider("Held-out share of texts", 0.0, 0.5, base.heldout_fraction, 0.05, disabled=locked, key=f"{form_key}::frac")
    hseed = s3.number_input("Held-out split seed", 0, 10_000, base.heldout_seed, disabled=locked, key=f"{form_key}::hseed")

lex_rows = [r for r in lex_df.fillna("").to_dict("records") if str(r["form"]).strip()]
missing_source = [r["form"] for r in lex_rows if not str(r["source"]).strip()]
current = Hypothesis(
    name=name.strip() or "Untitled hypothesis",
    author=author,
    language=language,
    description=description,
    key={r["sign_id"]: str(r["value"]).strip() for r in key_df.to_dict("records") if str(r["value"]).strip()},
    lexicon=[LexEntry(form=str(r["form"]).strip(), gloss=str(r["gloss"]), source=str(r["source"]).strip() or "MISSING")
             for r in lex_rows],
    match_mode=mode,
    heldout_fraction=frac,
    heldout_seed=int(hseed),
    locked_at=base.locked_at,
    locked_hash=base.locked_hash,
)
if locked:
    current = base

problems = []
if missing_source:
    problems.append(f"{len(missing_source)} lexicon forms have no source: {', '.join(missing_source[:8])}")
trivial = trivial_forms(current)
if trivial:
    problems.append(
        f"{len(trivial)} lexicon forms equal a single sign value ({', '.join(trivial[:8])}). "
        "They match under most shuffled keys too, so they make the test weaker."
    )
for p in problems:
    st.warning(p)

b1, b2, b3 = st.columns(3)
if b1.button("Save", disabled=locked, key="save"):
    current.save(HYP_DIR)
    st.session_state["pending_choice"] = current.name
    st.toast("Saved. On a hosted app saved files are temporary: download the JSON and commit it.")
    st.rerun()
if b2.button("Lock and save", disabled=locked or bool(missing_source) or not current.key or not current.lexicon, key="lock",
             help="Records a fingerprint of the key, lexicon and settings. Needs a key, a lexicon and a source on every form."):
    current = current.lock()
    current.save(HYP_DIR)
    st.session_state["pending_choice"] = current.name
    st.toast(f"Locked as {current.locked_hash[:12]}. Held-out texts are now scored.")
    st.rerun()
b3.download_button("Download JSON", current.model_dump_json(indent=2), file_name=f"{current.name}.json",
                   mime="application/json", key="download")

# Test ------------------------------------------------------------------------

st.header("Test")
table = corpus.text_table()
held = heldout_ids(table["text_id"], current.heldout_fraction, current.heldout_seed)
train = table[~table["text_id"].isin(held)]
test = table[table["text_id"].isin(held)]

t1, t2, t3, t4 = st.columns(4)
metric = t1.selectbox("Score", list(METRICS), format_func=METRICS.get, key="metric")
n_null = t2.select_slider("Shuffled keys", [200, 500, 1000, 2000, 5000], 1000, key="n_null")
bands = t3.slider("Frequency bands for shuffling", 1, 10, 5, key="bands",
                  help="Values are only swapped between signs in the same frequency band. 1 = shuffle freely.")
nseed = t4.number_input("Shuffle seed", 0, 10_000, 0, key="nseed")

if not current.key or not current.lexicon:
    st.info("Add values to the key and at least one lexicon form to run a test.")
    st.stop()


@st.cache_data(show_spinner="Scoring against shuffled keys…")
def run(hyp_json: str, texts: tuple, metric: str, n: int, bands: int, seed: int):
    h = Hypothesis.model_validate_json(hyp_json)
    scorer = Scorer([list(t) for t in texts], h.lexicon, h.match_mode)
    real = scorer.score(h.key)
    null = null_distribution(scorer, h.key, n=n, bands=bands, seed=seed, metric=metric)
    return real, null


def as_tuple(df):
    return tuple(tuple(s) for s in df["signs"])


sets = {"Development texts": train}
if current.status == "locked" and len(test):
    sets["Held-out texts"] = test
results = {}
for label, df in sets.items():
    real, null = run(current.model_dump_json(), as_tuple(df), metric, n_null, bands, int(nseed))
    results[label] = (real, null, compare_to_null(real[metric], null))

cols = st.columns(len(results))
for col, (label, (real, null, cmp)) in zip(cols, results.items()):
    with col:
        st.subheader(label)
        st.metric("Score", f"{real[metric]:.1%}", f"{real[metric] - cmp['null_mean']:+.1%} vs shuffled mean")
        st.markdown(
            f"Beats **{cmp['percentile']:.1%}** of {len(null)} shuffled keys · p = {cmp['p_value']:.3f}  \n"
            f"Readable texts: {real['readable']} of {real['texts']} ({real['coverage']:.0%})"
        )
        hist = pd.DataFrame({"score": null})
        chart = alt.Chart(hist).mark_bar(opacity=0.7).encode(
            x=alt.X("score:Q", bin=alt.Bin(maxbins=40), title=METRICS[metric], axis=alt.Axis(format="%")),
            y=alt.Y("count()", title="Shuffled keys"),
        ) + alt.Chart(pd.DataFrame({"score": [real[metric]]})).mark_rule(strokeWidth=3, color="#c0392b").encode(x="score:Q")
        st.altair_chart(chart, width="stretch")

if current.status != "locked":
    st.info(
        f"Held-out texts ({len(test)}) are hidden until the hypothesis is locked, so the key cannot be tuned on them. "
        "Results above are exploratory."
    )
else:
    st.caption(f"{len(test)} texts are held out by a split fixed at lock time (seed {current.heldout_seed}).")

with st.expander("Readings of development texts"):
    scorer = Scorer(train["signs"].tolist(), current.lexicon, current.match_mode)
    rows = []
    for tid, signs, r in zip(train["text_id"], train["signs"], scorer.readings(current.key)):
        seg = segment(r, scorer.words, scorer.max_len) if r else None
        rows.append({"text_id": tid, "signs": " ".join(signs), "reading": r or "", "segmented": " · ".join(seg) if seg else ""})
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")

st.caption(
    "Passing this test is necessary, not sufficient. A real decipherment also needs consistency with "
    "context, predictions on newly found texts, and independent replication. See the research brief, section 5."
)
