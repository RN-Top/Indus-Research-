import math

import pytest

from indus import entropy, stats
from indus.comparison import load_comparison

TEXTS = [["A", "B", "JAR"], ["A", "C", "JAR"], ["B", "JAR"], ["A"], ["A", "?", "B", "JAR"]]


def test_frequencies_skip_unreadable():
    freq = stats.sign_frequencies(TEXTS).set_index("sign")["count"].to_dict()
    assert freq == {"A": 4, "JAR": 4, "B": 3, "C": 1}


def test_positional_profile():
    prof = stats.positional_profile(TEXTS).set_index("sign")
    assert prof.loc["JAR", "final"] == 4
    assert prof.loc["A", "solo"] == 1
    assert prof.loc["A", "initial"] == 3
    assert prof.loc["JAR", "dominant"] == "final"
    # B after '?' keeps its medial position in the full text
    assert prof.loc["B", "medial"] == 2


def test_ngrams_do_not_bridge_gaps_or_texts():
    grams = stats.ngrams(TEXTS, 2).set_index("ngram")["count"].to_dict()
    assert grams == {"B JAR": 3, "A B": 1, "A C": 1, "C JAR": 1}
    assert "JAR A" not in grams


def test_summary():
    s = stats.summary(TEXTS)
    assert s["texts"] == 5 and s["sign_types"] == 4 and s["unreadable_tokens"] == 1
    assert s["hapax_types"] == 1


def test_zipf_fit_on_exact_power_law():
    import pandas as pd

    freq = pd.DataFrame({"rank": [1, 2, 3, 4], "count": [120, 60, 40, 30]})
    fit = stats.zipf_fit(freq)
    assert fit["slope"] == pytest.approx(-1, abs=1e-9)
    assert fit["r2"] == pytest.approx(1)


def test_conditional_entropy_bounds():
    deterministic = [["A", "B"]] * 10 + [["C", "D"]] * 10
    assert entropy.conditional_entropy(deterministic) == 0
    uniform = [["A", "B"], ["A", "C"], ["A", "D"], ["A", "E"]]
    assert entropy.conditional_entropy(uniform) == pytest.approx(2.0)
    assert math.isnan(entropy.conditional_entropy([["A"]]))


def test_miller_madow_increases_estimate():
    uniform = [["A", "B"], ["A", "C"]]
    assert entropy.conditional_entropy(uniform, miller_madow=True) > entropy.conditional_entropy(uniform)


def test_controls_preserve_lengths_and_signs():
    for make in entropy.CONTROLS.values():
        out = make(TEXTS, seed=1)
        assert [len(t) for t in out] == [len(t) for t in TEXTS]
    shuffled = entropy.shuffled_within_texts(TEXTS, seed=3)
    assert [sorted(a) for a in shuffled] == [sorted(b) for b in TEXTS]


def test_rigid_control_is_more_predictable(tmp_path):
    from indus import load_corpus
    from pathlib import Path

    texts = load_corpus(Path(__file__).parent.parent / "data" / "sample").texts["signs"].tolist()
    rigid = entropy.conditional_entropy(entropy.rigid_order(texts))
    rand = entropy.conditional_entropy(entropy.unigram_random(texts, seed=0))
    assert rigid < rand


def test_load_comparison(tmp_path):
    (tmp_path / "toy_marks.csv").write_text("# source: test\n# kind: non-linguistic\ntext_id,signs\n1,X Y\n2,Y\n")
    [c] = load_comparison(tmp_path)
    assert c.name == "toy marks" and c.kind == "non-linguistic" and c.texts == [["X", "Y"], ["Y"]]
