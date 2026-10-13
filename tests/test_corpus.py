from pathlib import Path

import pandas as pd
import pytest

from indus import load_corpus
from indus.query import PatternError, compile_pattern, matches, search

SAMPLE = Path(__file__).resolve().parent.parent / "data" / "sample"


@pytest.fixture(scope="module")
def corpus():
    return load_corpus(SAMPLE)


def test_sample_loads_without_errors(corpus):
    assert corpus.errors == []
    assert len(corpus.texts) > 0


def test_every_row_has_a_source(corpus):
    for frame in (corpus.sites, corpus.objects, corpus.texts, corpus.signs):
        assert (frame["source"].str.len() > 0).all()


def test_worked_example_is_real_and_unverified(corpus):
    text = corpus.texts.set_index("text_id").loc["MD-TIGER-1-a"]
    assert not text["synthetic"]
    assert text["confidence"] == "unverified"


def test_bad_rows_are_reported(tmp_path):
    for name in ("sites", "objects", "signs", "crosswalk"):
        (tmp_path / f"{name}.csv").write_text((SAMPLE / f"{name}.csv").read_text())
    (tmp_path / "texts.csv").write_text(
        "text_id,object_id,signs,sign_list,source\n"
        "T1,NOPE,JAR,PROVISIONAL,test\n"
        "T2,SYN-0001,NOT_A_SIGN,PROVISIONAL,test\n"
        "T3,SYN-0001,JAR,PROVISIONAL,\n"
    )
    errors = load_corpus(tmp_path).errors
    assert any("unknown object NOPE" in e for e in errors)
    assert any("unknown signs NOT_A_SIGN" in e for e in errors)
    assert any("line 4: source" in e for e in errors)


@pytest.mark.parametrize(
    "pattern, signs, expected",
    [
        ("FISH JAR", ["MAN", "FISH", "JAR"], True),
        ("FISH JAR", ["FISH", "MAN", "JAR"], False),
        ("^ FISH", ["FISH", "JAR"], True),
        ("^ FISH", ["MAN", "FISH"], False),
        ("JAR $", ["FISH", "JAR"], True),
        ("JAR $", ["JAR", "FISH"], False),
        ("FISH * JAR", ["FISH", "MAN", "JAR"], True),
        ("FISH * JAR", ["FISH", "JAR"], False),
        ("FISH ... JAR", ["FISH", "JAR"], True),
        ("FISH ... JAR", ["FISH", "MAN", "COMB", "JAR"], True),
        ("FISH ... JAR", ["JAR", "FISH"], False),
        ("FISH", ["FISH_HAT"], False),
        ("^ JAR $", ["JAR"], True),
    ],
)
def test_pattern(pattern, signs, expected):
    assert matches(compile_pattern(pattern), signs) is expected


@pytest.mark.parametrize("pattern", ["", "^ $", "...", "FISH (JAR"])
def test_invalid_patterns(pattern):
    with pytest.raises(PatternError):
        compile_pattern(pattern)


def test_search_combines_filters(corpus):
    table = corpus.text_table()
    hits = search(table, "JAR $", sites=["Harappa"])
    assert len(hits) > 0
    assert (hits["site"] == "Harappa").all()
    assert hits["signs"].map(lambda s: s[-1] == "JAR").all()
    tiger = search(table, iconography="tiger")
    assert "MD-TIGER-1-a" in set(tiger["text_id"])
    assert isinstance(tiger, pd.DataFrame)
