import numpy as np
import pytest

from indus.hypothesis import (
    Hypothesis, LexEntry, MatchMode, Scorer, compare_to_null, covered_chars, heldout_ids,
    load_hypotheses, normalise, null_distribution, segment, trivial_forms,
)

LEX = [LexEntry(form="kaṭu", source="t"), LexEntry(form="mīn", source="t"), LexEntry(form="an", source="t")]


def make(**kw):
    base = dict(name="H", key={"A": "ka", "B": "ṭu", "C": "mīn", "D": "an"}, lexicon=LEX)
    base.update(kw)
    return Hypothesis(**base)


def test_normalise_modes():
    assert normalise("Mīn-ā", MatchMode.exact) == "mīnā"
    assert normalise("Mīn-ā", MatchMode.no_diacritics) == "mina"
    assert normalise("Mīn-ā", MatchMode.consonants) == "mn"


def test_segment_and_coverage():
    words = {"katu", "min", "an"}
    assert segment("katumin", words, 4) == ["katu", "min"]
    assert segment("katux", words, 4) is None
    assert covered_chars("katuxmin", words, 4) == 7


def test_score():
    sc = Scorer([["A", "B", "C"], ["D", "?"], ["A", "C"], ["E"]], LEX, MatchMode.no_diacritics)
    r = sc.score(make().key)
    assert r["readable"] == 2  # '?' and unassigned E are not readable
    assert r["full_match"] == 1  # katumin yes, kamin no
    assert r["char_coverage"] == pytest.approx((7 + 3) / (7 + 5))


def test_lock_detects_changes(tmp_path):
    h = make().lock()
    assert h.status == "locked"
    edited = h.model_copy(update={"key": {**h.key, "A": "ki"}})
    assert edited.status == "changed after lock"
    # description and author do not affect the fingerprint
    assert h.model_copy(update={"description": "x"}).status == "locked"
    h.save(tmp_path)
    assert load_hypotheses(tmp_path)["H"].status == "locked"


def test_heldout_split_is_deterministic():
    ids = [f"T{i}" for i in range(1000)]
    a, b = heldout_ids(ids, 0.2, 1), heldout_ids(ids, 0.2, 1)
    assert a == b and 150 < len(a) < 250
    assert heldout_ids(ids, 0.2, 2) != a


def test_null_preserves_value_set_and_detects_planted_signal():
    rng = np.random.default_rng(0)
    signs = [f"S{i}" for i in range(20)]
    key = {s: v for s, v in zip(signs, ["ka", "ki", "ku", "ta", "ti", "tu", "pa", "pi", "pu", "ma",
                                        "mi", "mu", "na", "ni", "nu", "ra", "ri", "ru", "la", "li"])}
    texts = [list(rng.choice(signs, size=4)) for _ in range(200)]
    planted = {"".join(key[s] for s in t[:2]) for t in texts[:60]}
    lex = [LexEntry(form=f, source="t") for f in planted]
    sc = Scorer(texts, lex, MatchMode.exact)
    real = sc.score(key)["char_coverage"]
    null = null_distribution(sc, key, n=200, bands=1, seed=0)
    assert compare_to_null(real, null)["percentile"] > 0.95


def test_trivial_forms():
    h = make(lexicon=LEX + [LexEntry(form="ka", source="t")])
    assert trivial_forms(h) == ["an", "ka", "mīn"]
