import pandas as pd
import streamlit as st

from indus_workbench import controls, data, markov, ui

st.set_page_config(page_title="Sequence Model", layout="wide")
st.title("Sequence Model")
st.markdown(
    "Does knowing one sign help predict the next? A **bigram model** (uses the previous sign) is "
    "compared with a **unigram baseline** (ignores order), scored on texts each model has not "
    "seen (5-fold cross-validation within the exploration split). Lower bits per sign is better. "
    "The same comparison on shuffled texts is the negative control: there, the bigram model "
    "should gain nothing."
)

ui.init_settings()
corpus = ui.load_corpus()
ui.sidebar_status(corpus)
if corpus is None:
    st.stop()
seqs = data.explore_only(corpus).sequences
lam = st.slider("Weight on the previous sign (λ)", 0.1, 0.95, 0.7, 0.05,
                help="Fix this before looking at results. Tuning it to maximise the gain is a "
                     "form of overfitting.")


@st.cache_data(show_spinner="Cross-validating…")
def run(seqs_t, lam):
    seqs = [list(s) for s in seqs_t]
    real = markov.cross_validate(seqs, 5, 0, lam)
    shuf = markov.cross_validate(controls.shuffle_within_texts(seqs, controls.rng(1)), 5, 0, lam)
    return real, shuf


real, shuf = run(tuple(map(tuple, seqs)), lam)
table = pd.DataFrame({
    "Unigram baseline (bits/sign)": [sum(real["unigram_bits"]) / 5, sum(shuf["unigram_bits"]) / 5],
    "Bigram model (bits/sign)": [sum(real["bigram_bits"]) / 5, sum(shuf["bigram_bits"]) / 5],
    "Gain from order (bits/sign)": [real["mean_gain_bits"], shuf["mean_gain_bits"]],
    "Folds where bigram wins": [f"{real['folds_bigram_better']}/5", f"{shuf['folds_bigram_better']}/5"],
}, index=["Indus (transcribed)", "Negative control: shuffled within texts"])
st.dataframe(table.style.format({c: "{:.3f}" for c in table.columns if "bits" in c}),
             use_container_width=True)

if real["mean_gain_bits"] > shuf["mean_gain_bits"] and real["folds_bigram_better"] == 5:
    st.success("Sign order predicts unseen texts better than the order-free baseline, and better "
               "than the shuffled control. The sequences have learnable structure.")
else:
    st.warning("The bigram model does not clearly beat the baseline beyond the shuffled control.")

st.subheader("Most frequent transitions (exploration split)")
model = markov.Bigram(lam).fit(seqs)
tr = pd.DataFrame(model.transitions(60), columns=["from", "to", "count", "P(to | from)"])
st.dataframe(tr, use_container_width=True, hide_index=True, height=400)
st.caption("`<s>` marks the start of a text and `</s>` the end. A strong transition here is a "
           "lead, not a finding: register it as a 'precedes' hypothesis to test it properly.")

ui.log_result("sequence_model", {"lambda": lam, "real": real, "shuffled_control": shuf})
