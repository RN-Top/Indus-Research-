import json

import pandas as pd
import streamlit as st

from indus_workbench import data, hypotheses as hy, ui

st.set_page_config(page_title="Hypothesis Lab", layout="wide")
st.title("Hypothesis Lab")
st.markdown(
    "**1. Explore** a claim on the exploration split as often as you like. "
    "**2. Register** it: freeze the exact claim and commit the file to the repository's "
    "`hypotheses/` folder, which timestamps it publicly. "
    "**3. Confirm**: the app tests every registered hypothesis once on the locked holdout and "
    "corrects for the number of tests. Only step 3 counts as evidence."
)

ui.init_settings()
corpus = ui.load_corpus()
ui.sidebar_status(corpus)
if corpus is None:
    st.stop()

explore_tab, register_tab, confirm_tab = st.tabs(["1. Explore", "2. Register", "3. Confirm on holdout"])


def hypothesis_form(prefix: str) -> dict | None:
    kind = st.selectbox("Type of claim", list(hy.KINDS), key=f"{prefix}kind",
                        format_func=lambda k: f"{k}: {hy.KINDS[k]}")
    p: dict = {}
    if kind == "precedes":
        a, b = st.columns(2)
        p["a"] = a.text_input("Sign A", key=f"{prefix}a").strip()
        p["b"] = b.text_input("Sign B (follows A)", key=f"{prefix}b").strip()
    elif kind == "position":
        a, b = st.columns(2)
        p["a"] = a.text_input("Sign A", key=f"{prefix}a").strip()
        p["where"] = b.selectbox("Position", ["start", "end"], key=f"{prefix}where")
    elif kind == "association":
        a, b, c = st.columns(3)
        p["a"] = a.text_input("Sign A", key=f"{prefix}a").strip()
        p["field"] = b.selectbox("Field", ["site", "object_type", "motif"], key=f"{prefix}field")
        p["value"] = c.selectbox("Value", sorted(corpus.df[p["field"]].unique()), key=f"{prefix}value")
    elif kind == "class_cohesion":
        p["signs"] = st.text_input("Signs in the proposed class (space-separated)",
                                   key=f"{prefix}signs").split()
    statement = st.text_area(
        "Claim in plain words, including what it would mean if true",
        key=f"{prefix}stmt",
        placeholder="e.g. Sign G740 marks the start of a text, consistent with a title or owner prefix.")
    alpha = st.number_input("Significance level (α)", 0.001, 0.1, 0.05, 0.005, key=f"{prefix}alpha")
    if not all(p.values()) or not statement.strip():
        st.caption("Fill in every field to continue.")
        return None
    return hy.new_hypothesis(kind, p, statement, source_key=corpus.source_key, alpha=alpha,
                             author=st.session_state.get("author", ""))


def show_result(res: hy.TestResult, alpha: float):
    c = st.columns(4)
    c[0].metric("Observed", f"{res.observed:.3g}")
    c[1].metric("Null average", f"{res.null_mean:.3g}")
    c[2].metric("Effect ratio", f"{res.effect_ratio:.2f}×" if res.null_mean else "—")
    c[3].metric("p-value", f"{res.p_value:.4f}" if res.p_value == res.p_value else "—")
    st.caption(f"{res.note} {res.n_perm:,} permutations. Rests on {res.n_support} occurrence(s).")
    if res.n_support < hy.MIN_SUPPORT:
        st.warning(f"Fewer than {hy.MIN_SUPPORT} occurrences: too little data to say anything.")


# ---------------------------------------------------------------- explore
with explore_tab:
    st.info("Exploration results are leads, not evidence. Any pattern found by trying many "
            "claims will sometimes look significant by chance.")
    h = hypothesis_form("x_")
    if h and st.button("Test on exploration split", type="primary"):
        ex = data.explore_only(corpus)
        with st.spinner("Running permutation test…"):
            res = hy.run_test(h, ex.df)
        show_result(res, h["alpha"])
        if h["kind"] == "precedes":
            with st.spinner("Positive control: can this test detect a planted pattern?"):
                power = hy.sensitivity_check(h, ex.df)
            st.caption(f"Positive control: when A→B is planted in 5% of shuffled texts, the test "
                       f"detects it {power:.0%} of the time. If this is low, a negative result "
                       "means little.")
        st.session_state["draft"] = h

# ---------------------------------------------------------------- register
with register_tab:
    st.text_input("Your name (recorded in the file)", key="author")
    draft = st.session_state.get("draft")
    if not draft:
        st.write("Explore a hypothesis first; the last one you tested appears here.")
    else:
        st.json({k: draft[k] for k in ["kind", "params", "statement", "alpha", "source_key"]})
        if st.button("Freeze this hypothesis"):
            draft["author"] = st.session_state.get("author", "")
            frozen = hy.freeze(draft)
            st.session_state["frozen"] = frozen
        frozen = st.session_state.get("frozen")
        if frozen:
            st.success(f"Frozen as **{frozen['id']}**. Fingerprint `{frozen['sha256'][:16]}…`")
            st.download_button("Download hypothesis file", json.dumps(frozen, indent=2),
                               file_name=f"{frozen['id']}.json", mime="application/json")
            st.markdown(
                "Now add this file to the `hypotheses/` folder of your GitHub repository and "
                "commit it. On a phone: open the repo on github.com → `hypotheses` → **Add file** → "
                "**Upload files**. The commit date is your public proof that the claim was made "
                "before the confirmatory test. Any later edit to the file breaks its fingerprint, "
                "and the app will refuse to test it.")

# ---------------------------------------------------------------- confirm
with confirm_tab:
    registered = ui.load_registered()
    st.write(f"{len(registered)} hypothesis file(s) found in `hypotheses/`.")
    if not registered:
        st.stop()
    rows = []
    for h in registered:
        rows.append({"file": h["_file"], "id": h.get("id", "?"), "kind": h.get("kind"),
                     "intact": hy.verify(h), "corpus": h.get("source_key")})
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
    bad = [r["file"] for r in rows if not r["intact"]]
    if bad:
        st.error(f"These files were edited after freezing and will be skipped: {', '.join(bad)}")
    st.warning("Running this spends the holdout for these hypotheses. Run it once, record the "
               "output, and commit the results file to `results/`.")
    if st.button("Run confirmatory tests on the holdout", type="primary"):
        results = []
        for h in registered:
            if not hy.verify(h):
                continue
            c = ui.load_corpus(h["source_key"])
            if c is None:
                continue
            res = hy.run_test(h, data.holdout_only(c).df)
            results.append({"id": h["id"], "kind": h["kind"], "params": h["params"],
                            "statement": h["statement"], "alpha": h["alpha"],
                            "observed": res.observed, "null_mean": res.null_mean,
                            "effect_ratio": res.effect_ratio, "p": res.p_value,
                            "support": res.n_support, "n_perm": res.n_perm,
                            "data_sha256": c.sha256, "settings": c.settings})
        valid = [r for r in results if r["p"] == r["p"]]
        qs = hy.benjamini_hochberg([r["p"] for r in valid])
        for r, q in zip(valid, qs):
            r["q_BH"] = q
        for r in results:
            r.setdefault("q_BH", float("nan"))
            r["verdict"] = hy.verdict(r["q_BH"], r["alpha"], r["support"])
        out = pd.DataFrame(results)
        st.dataframe(out[["id", "kind", "observed", "null_mean", "effect_ratio", "p", "q_BH",
                          "support", "verdict"]], hide_index=True, use_container_width=True)
        st.caption("q_BH is the p-value adjusted for testing several hypotheses (Benjamini-Hochberg). "
                   "A claim is supported only if q_BH < α and it rests on at least "
                   f"{hy.MIN_SUPPORT} occurrences.")
        payload = json.dumps(results, indent=2, default=str)
        st.download_button("Download results file", payload, file_name="confirmatory_results.json",
                           mime="application/json")
        ui.log_result("confirmatory", {"results": results})
