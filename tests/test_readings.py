"""Tests for the reading tester (decipherment keys). Synthetic data only."""

import unittest

import numpy as np

from indus_workbench import readings as rd

LEX = [{"form": "kaṭu", "source": "t"}, {"form": "mīn", "source": "t"}, {"form": "an", "source": "t"}]
KEY = {"A": "ka", "B": "ṭu", "C": "mīn", "D": "an"}


class ReadingTests(unittest.TestCase):
    def test_normalise_modes(self):
        self.assertEqual(rd.normalise("Mīn-ā", "exact"), "mīnā")
        self.assertEqual(rd.normalise("Mīn-ā", "no_diacritics"), "mina")
        self.assertEqual(rd.normalise("Mīn-ā", "consonants"), "mn")

    def test_segment_and_coverage(self):
        words = {"katu", "min", "an"}
        self.assertEqual(rd.segment("katumin", words, 4), ["katu", "min"])
        self.assertIsNone(rd.segment("katux", words, 4))
        self.assertEqual(rd.covered_chars("katuxmin", words, 4), 7)

    def test_score(self):
        sc = rd.Scorer([["A", "B", "C"], ["D", "E"], ["A", "C"], ["E"]], LEX, "no_diacritics")
        r = sc.score(KEY)
        self.assertEqual(r["readable"], 2)  # texts with unassigned E are unreadable
        self.assertEqual(r["full_match"], 1)  # katumin yes, kamin no
        self.assertAlmostEqual(r["char_coverage"], (7 + 3) / (7 + 5))

    def test_freeze_detects_changes(self):
        r = rd.freeze(rd.new_reading("H", KEY, LEX))
        self.assertTrue(rd.verify(r))
        r2 = dict(r, description="new text")  # description is not part of the claim
        self.assertTrue(rd.verify(r2))
        r3 = dict(r, key={**r["key"], "A": "ki"})
        self.assertFalse(rd.verify(r3))

    def test_planted_key_beats_shuffles(self):
        # Positive control: a lexicon built from the true key's readings.
        rng = np.random.default_rng(0)
        signs = [f"S{i}" for i in range(20)]
        vals = ["ka", "ki", "ku", "ta", "ti", "tu", "pa", "pi", "pu", "ma",
                "mi", "mu", "na", "ni", "nu", "ra", "ri", "ru", "la", "li"]
        key = dict(zip(signs, vals))
        texts = [list(rng.choice(signs, size=4)) for _ in range(200)]
        lex = [{"form": "".join(key[s] for s in t[:2]), "source": "t"} for t in texts[:60]]
        sc = rd.Scorer(texts, lex, "exact")
        null = rd.null_distribution(sc, key, n=200, bands=1, seed=0)
        self.assertGreater(rd.compare_to_null(sc.score(key)["char_coverage"], null)["percentile"], 0.95)

    def test_unrelated_lexicon_does_not_beat_shuffles(self):
        # Negative control: a lexicon with no link to the texts.
        rng = np.random.default_rng(1)
        signs = [f"S{i}" for i in range(20)]
        vals = ["ka", "ki", "ku", "ta", "ti", "tu", "pa", "pi", "pu", "ma",
                "mi", "mu", "na", "ni", "nu", "ra", "ri", "ru", "la", "li"]
        key = dict(zip(signs, vals))
        texts = [list(rng.choice(signs, size=4)) for _ in range(200)]
        lex = [{"form": "".join(rng.choice(vals, size=2)), "source": "t"} for _ in range(60)]
        sc = rd.Scorer(texts, lex, "exact")
        null = rd.null_distribution(sc, key, n=200, bands=1, seed=0)
        self.assertGreater(rd.compare_to_null(sc.score(key)["char_coverage"], null)["p_value"], 0.05)

    def test_warnings_flag_trivial_forms_and_missing_sources(self):
        r = rd.new_reading("H", KEY, LEX + [{"form": "ka", "source": ""}])
        w = " ".join(rd.warnings(r))
        self.assertIn("no source", w)
        self.assertIn("single sign value", w)


class QueryTests(unittest.TestCase):
    def test_patterns(self):
        from indus_workbench import query as q
        seq = ["G17", "G5", "G740"]
        self.assertTrue(q.matches(q.compile_pattern("G17 ... G740 $"), seq))
        self.assertTrue(q.matches(q.compile_pattern("^ G17 * G740"), seq))
        self.assertFalse(q.matches(q.compile_pattern("^ G740"), seq))
        with self.assertRaises(q.PatternError):
            q.compile_pattern("^ $")


if __name__ == "__main__":
    unittest.main()
