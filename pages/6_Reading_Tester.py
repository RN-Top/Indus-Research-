import json

import numpy as np
import pandas as pd
import streamlit as st

from indus_workbench import data, readings as rd, stats, ui

st.set_page_config(page_title="Reading Tester", layout="wide")
st.title("Reading Tester")
st.markdown(
    "Test a proposed **decipherment key**: a sound value for each sign plus a lexicon of words in the "
    "proposed language, each with a published source. The key is applied to every text, and the "
    "result is compared with keys made by **shuffling the same values among signs of similar "
    "frequency**. A key that doesn't beat its shuffles isn't evidence, however good individual "
    "readings look."
)

ui.init_settings()
corpus = ui.load_corpus()
ui.sidebar_status(corpus)
if corpus is None:
    st.stop()

explore = data.explore_only(corpus)

# --- Load an existing key ----------------------------------------------------
up = st.file_uploader("Start from a saved reading file (optional)", type=["json"])
base = json.loads(up.getvalue()) if up else {}
if base and base.get("source_key") != corpus.source_key:
    st.warning(f"This file was made for corpus `{base.get('source_key')}`; switch to it on the Home page.")

# --- Edit ---------------------------------------------------------------------
c1, c2, c3 = st.columns(3)
name = c1.text_input("Name", base.get("name", ""))
language = c2.text_input("Proposed language", base.get("language", ""),
                         placeholder="e.g. Proto-Dravidian")
author = c3.text_input("Author", base.get("author", ""))
description = st.text_area("Argument for this key", base.get("description", ""), height=80)

freq = stats.sign_frequencies(explore.sequences)
signs = freq[["sign", "tokens"]].copy()
signs["value"] = signs["sign"].map(base.get("key", {})).fillna("")
k1, k2 = st.columns(2)
with k1:
    st.markdown("**Key**: a value for each sign (leave blank if unassigned)")
    key_df = st.data_editor(signs, hide_index=True, disabled=["sign", "tokens"], height=380,
                            use_container_width=True, key="key_editor")
with k2:
    st.markdown("**Lexicon**: words in the proposed language, each with a source")
    lex0 = pd.DataFrame(base.get("lexicon", []), columns=["form", "gloss", "source"])
    lex_df = st.data_editor(lex0, num_rows="dynamic", hide_index=True, height=380,
                            use_container_width=True, key="lex_editor")

s1, s2, s3 = st.columns(3)
mode = s1.selectbox("Spelling match", list(rd.MATCH_MODES), format_func=rd.MATCH_MODES.get,
                    index=list(rd.MATCH_MODES).index(base.get("match_mode", "no_diacritics")))
metric = s2.selectbox("Score", list(rd.METRICS), format_func=rd.METRICS.get,
                      index=list(rd.METRICS).index(base.get("metric", "char_coverage")))
bands = s3.slider("Frequency bands for shuffling", 1, 10, int(base.get("bands", 5)),
                  help="Values are only swapped between signs of similar frequency. 1 = shuffle freely.")

key = {r["sign"]: str(r["value"]).strip() for r in key_df.to_dict("records") if str(r["value"]).strip()}
lexicon = [{k: str(r.get(k, "") or "").strip() for k in ("form", "gloss", "source")}
           for r in lex_df.fillna("").to_dict("records") if str(r.get("form", "")).strip()]
current = rd.new_reading(name or "Untitled key", key, lexicon, language=language, author=author,
                         description=description, match_mode=mode, source_key=corpus.source_key,
                         metric=metric, bands=bands)

for w in rd.warnings(current):
    st.warning(w)
if not key or not lexicon:
    st.info("Add values to the key and at least one lexicon word to run a test.")
    st.stop()


@st.cache_data(show_spinner="Scoring against shuffled keys…")
def run(rec_json: str, texts: tuple):
    r = json.loads(rec_json)
    sc = rd.Scorer([list(t) for t in texts], r["lexicon"], r["match_mode"])
    real = sc.score(r["key"])
    null = rd.null_distribution(sc, r["key"], n=r["n_null"], bands=r["bands"], seed=r["seed"],
                                metric=r["metric"])
    return real, null


def show(label, real, null):
    cmp = rd.compare_to_null(real[metric], null)
    st.subheader(label)
    m = st.columns(4)
    m[0].metric("Score", f"{real[metric]:.1%}")
    m[1].metric("Shuffled keys (mean)", f"{cmp['null_mean']:.1%}")
    m[2].metric("Beats shuffles", f"{cmp['percentile']:.1%}")
    m[3].metric("p-value", f"{cmp['p_value']:.3f}")
    st.caption(f"Readable texts (every sign has a value): {real['readable']} of {real['texts']} "
               f"({real['coverage']:.0%}). {len(null):,} shuffled keys.")
    hist = pd.Series(np.histogram(null, bins=30)[0],
                     index=np.round(np.histogram(null, bins=30)[1][:-1], 4), name="shuffled keys")
    st.bar_chart(hist, color=ui.OCHRE)
    st.caption(f"Distribution of shuffled-key scores. This key scores {real[metric]:.4f}.")
    return cmp


# --- Explore -----------------------------------------------------------------
st.header("1. Explore (exploration split)")
real, null = run(json.dumps(current), tuple(tuple(s) for s in explore.sequences))
show("Exploration texts", real, null)
st.info("Exploratory. Adjusting the key and re-running here, then reporting the best result, is "
        "overfitting. Freeze the key before testing it on the holdout.")

with st.expander("Readings of exploration texts"):
    sc = rd.Scorer(explore.sequences, current["lexicon"], mode)
    rows = []
    for tid, sg, r in zip(explore.df["text_id"], explore.sequences, sc.readings(current["key"])):
        seg = rd.segment(r, sc.words, sc.max_len) if r else None
        rows.append({"text_id": tid, "signs": " ".join(sg), "reading": r or "",
                     "as words": " · ".join(seg) if seg else ""})
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True, height=300)

# --- Freeze ------------------------------------------------------------------
st.header("2. Freeze")
if st.button("Freeze this key"):
    st.session_state["frozen_reading"] = rd.freeze(current)
fr = st.session_state.get("frozen_reading")
if fr:
    st.success(f"Frozen as **{fr['id']}**. Fingerprint `{fr['sha256'][:16]}…`")
    st.download_button("Download reading file", json.dumps(fr, indent=2, ensure_ascii=False),
                       file_name=f"{fr['id']}.json", mime="application/json")
    st.caption("Upload it to the repository's `hypotheses/` folder and commit, exactly as for "
               "other hypotheses. The commit date is the public record.")

# --- Confirm -----------------------------------------------------------------
st.header("3. Confirm on the locked holdout")
registered = [h for h in ui.load_registered() if h.get("type") == "reading"]
if not registered:
    st.write("No frozen reading files in `hypotheses/` yet.")
    st.stop()
pick = st.selectbox("Registered key", registered, format_func=lambda h: f"{h['id']} · {h['name']}")
if not rd.verify(pick):
    st.error("This file was edited after freezing. It can't be tested; freeze a new version.")
    st.stop()
if st.button("Run once on the holdout", type="primary"):
    c = ui.load_corpus(pick["source_key"])
    hold = data.holdout_only(c)
    real, null = run(json.dumps(pick), tuple(tuple(s) for s in hold.sequences))
    cmp = show("Holdout texts", real, null)
    result = {"id": pick["id"], "name": pick["name"], "metric": pick["metric"], "score": real[pick["metric"]],
              **cmp, "readable": real["readable"], "texts": real["texts"], "data_sha256": c.sha256,
              "settings": c.settings}
    st.download_button("Download result", json.dumps(result, indent=2, default=str),
                       file_name=f"{pick['id']}_result.json", mime="application/json")
    ui.log_result("reading_confirmatory", result)

st.caption("Passing this test is necessary, not sufficient. A real decipherment also needs consistency "
           "with archaeological context, correct predictions on newly found texts, and independent "
           "replication.")
