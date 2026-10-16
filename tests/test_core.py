"""Tests for the analysis core.

These run on a small SYNTHETIC corpus built below, never on real data, so the
right answers are known. Run with:  python -m pytest   or   python -m unittest
"""

import unittest

import numpy as np
import pandas as pd

from indus_workbench import controls, data, entropy, hypotheses, markov, stats


def synthetic_csv(n=400, seed=0) -> bytes:
    """A corpus with planted structure: 'A' is always followed by 'B',
    'Z' always ends a text, and 'S' only occurs at site 'Alpha'."""
    r = np.random.default_rng(seed)
    filler = [f"F{i}" for i in range(30)]
    rows = []
    for i in range(n):
        L = int(r.integers(2, 7))
        seq = list(r.choice(filler, size=L))
        if i % 3 == 0:
            j = int(r.integers(0, L - 1))
            seq[j], seq[j + 1] = "A", "B"
        if i % 4 == 0:
            seq[-1] = "Z"
        site = "Alpha" if i % 2 == 0 else "Beta"
        if site == "Alpha" and i % 5 == 0:
            seq[0] = "S"
        direction = "L-R" if i % 7 == 0 else "R-L"
        stored = list(reversed(seq)) if direction == "L-R" else seq
        rows.append({
            "inscription_id": f"T{i}", "sign_sequence": " ".join(stored), "site": site,
            "object_type": "seal", "line_count": 1, "damaged": "True" if i % 50 == 1 else "False",
            "reading_direction": direction, "motif": "unknown", "cisi_number": f"C-{i}",
        })
    rows.append(dict(rows[0], inscription_id="DUP"))  # exact duplicate text
    return pd.DataFrame(rows).to_csv(index=False).encode()


RAW = synthetic_csv()


class DataTests(unittest.TestCase):
    def test_orientation_restores_reading_order(self):
        c = data.build_corpus(RAW, "test", drop_damaged=False)
        row = c.df[c.df.text_id == "T0"].iloc[0]  # i=0 is L-R, stored reversed
        self.assertEqual(row.signs[-1], "Z")

    def test_exclusions_are_logged(self):
        c = data.build_corpus(RAW, "test", drop_damaged=True, dedupe=True)
        reasons = {e.reason for e in c.exclusions}
        self.assertIn("marked damaged in source", reasons)
        self.assertTrue(any("duplicate" in r for r in reasons))
        self.assertEqual(c.n_texts + len(c.exclusions), 401)

    def test_holdout_is_deterministic_and_about_20_percent(self):
        a = [data.holdout_split(f"T{i}") for i in range(5000)]
        b = [data.holdout_split(f"T{i}") for i in range(5000)]
        self.assertEqual(a, b)
        self.assertAlmostEqual(a.count("holdout") / 5000, 0.2, delta=0.02)

    def test_fingerprint_changes_with_data(self):
        self.assertNotEqual(data.sha256_bytes(RAW), data.sha256_bytes(RAW + b"\n"))


class EntropyTests(unittest.TestCase):
    def test_bounds(self):
        seqs = [list("abcd") * 3 for _ in range(50)]
        h1 = entropy.block_entropy(seqs, 1)
        self.assertAlmostEqual(h1, 1.0, places=6)  # 4 equiprobable symbols, base 4
        rigid = [["a", "a", "a"] for _ in range(20)] + [["b"]]
        self.assertLess(entropy.block_entropy(rigid, 2), 0.01)

    def test_random_beats_structured(self):
        r = controls.rng(1)
        lang = controls.markov_language(800, [5], 20, r, concentration=0.02)
        noise = controls.uniform_random(lang, r)
        self.assertLess(entropy.block_entropy(lang, 2), entropy.block_entropy(noise, 2))


class ControlTests(unittest.TestCase):
    def test_shuffle_within_preserves_each_text(self):
        seqs = [["a", "b", "c"], ["d", "e"]]
        out = controls.shuffle_within_texts(seqs, controls.rng(0))
        self.assertEqual([sorted(s) for s in out], [sorted(s) for s in seqs])

    def test_shuffle_global_preserves_lengths_and_counts(self):
        seqs = [["a", "b", "c"], ["d", "e"], ["a"]]
        out = controls.shuffle_global(seqs, controls.rng(0))
        self.assertEqual([len(s) for s in out], [3, 2, 1])
        self.assertEqual(sorted(x for s in out for x in s), sorted(x for s in seqs for x in s))


class MarkovTests(unittest.TestCase):
    def test_bigram_beats_unigram_on_structured_data(self):
        lang = controls.markov_language(600, [6], 15, controls.rng(3), concentration=0.02)
        cv = markov.cross_validate(lang, k=5)
        self.assertGreater(cv["mean_gain_bits"], 0.3)

    def test_no_gain_on_shuffled_data(self):
        lang = controls.markov_language(600, [6], 15, controls.rng(3), concentration=0.02)
        shuf = controls.shuffle_global(lang, controls.rng(4))
        cv = markov.cross_validate(shuf, k=5)
        self.assertLess(cv["mean_gain_bits"], 0.1)


class HypothesisTests(unittest.TestCase):
    def setUp(self):
        self.c = data.build_corpus(RAW, "test")

    def _run(self, kind, params):
        h = hypotheses.new_hypothesis(kind, params, "test", n_perm=300)
        return hypotheses.run_test(h, self.c.df)

    def test_planted_patterns_are_found(self):
        self.assertLess(self._run("precedes", {"a": "A", "b": "B"}).p_value, 0.01)
        self.assertLess(self._run("position", {"a": "Z", "where": "end"}).p_value, 0.01)
        self.assertLess(self._run("association", {"a": "S", "field": "site", "value": "Alpha"}).p_value, 0.01)

    def test_absent_pattern_is_not_found(self):
        self.assertGreater(self._run("precedes", {"a": "B", "b": "A"}).p_value, 0.05)
        self.assertGreater(self._run("position", {"a": "F1", "where": "start"}).p_value, 0.01)

    def test_false_positive_rate_is_controlled(self):
        # Negative control: on pure noise, p < 0.05 should happen ~5% of the time.
        r = controls.rng(9)
        hits = 0
        trials = 60
        for t in range(trials):
            seqs = [list(r.choice([f"F{i}" for i in range(10)], size=4)) for _ in range(200)]
            h = hypotheses.new_hypothesis("precedes", {"a": "F1", "b": "F2"}, "x", n_perm=200, seed=t)
            hits += hypotheses.run_test(h, pd.DataFrame({"signs": seqs})).p_value < 0.05
        self.assertLess(hits / trials, 0.15)

    def test_class_cohesion_finds_shared_contexts(self):
        # P1..P3 are always followed by Q; R1..R3 by random fillers.
        r = controls.rng(5)
        seqs = []
        for i in range(400):
            seq = list(r.choice([f"F{k}" for k in range(25)], size=4))
            seq[1] = f"P{i % 3 + 1}" if i % 2 == 0 else f"R{i % 3 + 1}"
            if i % 2 == 0:
                seq[2] = "Q"
            seqs.append(seq)
        df = pd.DataFrame({"signs": seqs})
        h = hypotheses.new_hypothesis("class_cohesion", {"signs": ["P1", "P2", "P3"]}, "x", n_perm=200)
        self.assertLess(hypotheses.run_test(h, df).p_value, 0.05)

    def test_freeze_and_tamper_detection(self):
        h = hypotheses.freeze(hypotheses.new_hypothesis("precedes", {"a": "A", "b": "B"}, "x"))
        self.assertTrue(hypotheses.verify(h))
        h["params"]["b"] = "C"
        self.assertFalse(hypotheses.verify(h))

    def test_benjamini_hochberg(self):
        q = hypotheses.benjamini_hochberg([0.01, 0.04, 0.03, 0.5])
        self.assertAlmostEqual(q[0], 0.04)
        self.assertAlmostEqual(q[3], 0.5)
        self.assertTrue(all(a >= b for a, b in zip(q, [0.01, 0.04, 0.03, 0.5])))


class StatsTests(unittest.TestCase):
    def test_positional_profile(self):
        prof = stats.positional_profile([["a", "b", "c"], ["a", "c"]])
        self.assertEqual(prof.loc["a", "start"], 2)
        self.assertEqual(prof.loc["c", "end"], 2)


if __name__ == "__main__":
    unittest.main()


class ClassTests(unittest.TestCase):
    """New Phase 3 tests, on synthetic data with planted structure."""

    def _corpus(self, seed=0):
        r = np.random.default_rng(seed)
        seqs = []
        for i in range(600):
            seq = list(r.choice([f"F{k}" for k in range(30)], size=4))
            if i % 2 == 0:  # "short numerals" S1-S3 are followed by X
                seq[1], seq[2] = f"S{i % 3 + 1}", "X"
            else:  # "long numerals" L1-L3 are followed by Y
                seq[1], seq[2] = f"L{i % 3 + 1}", "Y"
            seqs.append(seq)
        obj = ["seal" if (i % 2 == 0 and i % 5) else "tablet" for i in range(600)]
        return pd.DataFrame({"signs": seqs, "object_type": obj})

    def test_class_contrast_finds_two_systems(self):
        df = self._corpus()
        h = hypotheses.new_hypothesis("class_contrast", {"signs": ["S1", "S2", "S3"], "other": ["L1", "L2", "L3"]},
                                      "x", n_perm=200)
        self.assertLess(hypotheses.run_test(h, df).p_value, 0.01)

    def test_class_contrast_null_when_identical(self):
        df = self._corpus()
        h = hypotheses.new_hypothesis("class_contrast", {"signs": ["F1", "F2"], "other": ["F3", "F4"]},
                                      "x", n_perm=200)
        self.assertGreater(hypotheses.run_test(h, df).p_value, 0.01)

    def test_class_association_and_position(self):
        df = self._corpus()
        h = hypotheses.new_hypothesis("class_association",
                                      {"signs": ["S1", "S2", "S3"], "field": "object_type", "value": "seal"},
                                      "x", n_perm=200)
        self.assertLess(hypotheses.run_test(h, df).p_value, 0.01)
        h = hypotheses.new_hypothesis("position", {"a": ["S1", "S2", "S3"], "where": "not_end"}, "x", n_perm=200)
        r = hypotheses.run_test(h, df)
        self.assertGreater(r.n_support, 0)
        self.assertLess(r.p_value, 0.01)

    def test_variant_check_ranks_true_partners_high(self):
        from indus_workbench import classes
        df = self._corpus()
        # S1 and S2 share contexts by construction; F-signs are noise.
        out = classes.variant_check(list(df["signs"]), [("S1", "S2")], min_count=5)
        self.assertLessEqual(int(out["rank"].iloc[0]), 3)

    def test_settings_are_part_of_the_fingerprint(self):
        h = hypotheses.freeze(hypotheses.new_hypothesis("precedes", {"a": "A", "b": "B"}, "x"))
        h["data_settings"] = dict(h["data_settings"], dedupe=True)
        self.assertFalse(hypotheses.verify(h))


class PairSpecificityTests(unittest.TestCase):
    def _texts(self, fixed: bool, seed=0):
        r = np.random.default_rng(seed)
        nums, items = ["N1", "N2", "N3", "N4"], ["I1", "I2", "I3", "I4"]
        seqs = []
        for _ in range(500):
            k = int(r.integers(4))
            n = nums[k] if fixed else nums[int(r.integers(4))]  # fixed: item k always takes numeral k
            seqs.append(["F0", n, items[k], "F1"])
        return pd.DataFrame({"signs": seqs})

    def test_finds_fixed_pairs(self):
        h = hypotheses.new_hypothesis("pair_specificity", {"signs": ["N1", "N2", "N3", "N4"]}, "x", n_perm=200)
        self.assertLess(hypotheses.run_test(h, self._texts(True)).p_value, 0.01)

    def test_free_counting_is_not_flagged(self):
        h = hypotheses.new_hypothesis("pair_specificity", {"signs": ["N1", "N2", "N3", "N4"]}, "x", n_perm=200)
        self.assertGreater(hypotheses.run_test(h, self._texts(False)).p_value, 0.01)


class PairShareTests(unittest.TestCase):
    def _texts(self, planted, seed=0):
        r = np.random.default_rng(seed)
        nums = ["N1", "N2", "N3", "N4", "N6", "N7"]
        seqs = []
        for _ in range(600):
            item = "T" if r.random() < 0.3 else f"I{int(r.integers(5))}"
            if planted and item == "T" and r.random() < 0.6:
                n = ["N6", "N7"][int(r.integers(2))]
            else:
                n = nums[int(r.integers(len(nums)))]
            seqs.append(["F0", n, item])
        return pd.DataFrame({"signs": seqs})

    def _h(self):
        return hypotheses.new_hypothesis(
            "pair_share", {"signs": ["N1", "N2", "N3", "N4", "N6", "N7"], "subset": ["N6", "N7"],
                           "targets": ["T"]}, "x", n_perm=300)

    def test_finds_planted_preference(self):
        self.assertLess(hypotheses.run_test(self._h(), self._texts(True)).p_value, 0.01)

    def test_no_preference_not_flagged(self):
        self.assertGreater(hypotheses.run_test(self._h(), self._texts(False)).p_value, 0.01)


class OrderTests(unittest.TestCase):
    def _texts(self, ordered, seed=0):
        r = np.random.default_rng(seed)
        seqs = []
        for _ in range(300):
            body = list(r.choice([f"F{k}" for k in range(10)], size=3))
            pair = ["E", "L"] if (ordered or r.random() < 0.5) else ["L", "E"]
            seqs.append(body[:1] + [pair[0]] + body[1:] + [pair[1]] if r.random() < 0.5 else [pair[0]] + body + [pair[1]])
        return pd.DataFrame({"signs": seqs})

    def test_finds_fixed_order(self):
        h = hypotheses.new_hypothesis("class_order", {"first": ["E"], "second": ["L"]}, "x", n_perm=200)
        self.assertLess(hypotheses.run_test(h, self._texts(True)).p_value, 0.01)

    def test_free_order_not_flagged(self):
        h = hypotheses.new_hypothesis("class_order", {"first": ["E"], "second": ["L"]}, "x", n_perm=200)
        self.assertGreater(hypotheses.run_test(h, self._texts(False)).p_value, 0.01)

    def test_pair_share_preceding_side(self):
        r = np.random.default_rng(3)
        seqs = []
        for _ in range(400):
            o = "O" if r.random() < 0.4 else "X"
            n = "N2" if (o == "O" and r.random() < 0.7) else ["N1", "N2", "N3"][int(r.integers(3))]
            seqs.append([o, n, "F"])
        h = hypotheses.new_hypothesis("pair_share", {"signs": ["N1", "N2", "N3"], "subset": ["N2"],
                                                     "targets": ["O"], "side": "preceding"}, "x", n_perm=200)
        self.assertLess(hypotheses.run_test(h, pd.DataFrame({"signs": seqs})).p_value, 0.01)


class MiddleFinalSlotTests(unittest.TestCase):
    """Positive and negative controls for the end-of-middle slot test (middle_final_slot)."""
    P = {"signs": ["T1", "T2"], "openers": ["O1"], "closers": ["C1"]}

    def _texts(self, planted, n=300, seed=0):
        r = np.random.default_rng(seed)
        seqs = []
        for _ in range(n):
            body = [f"M{int(r.integers(6))}" for _ in range(int(r.integers(1, 4)))]
            if r.random() < 0.4:
                t = f"T{int(r.integers(1, 3))}"
                body = body + [t] if planted else body[:0] + list(r.permutation(body + [t]))
            seqs.append((["O1", "G2"] if r.random() < 0.5 else []) + body + ["C1"])
        return pd.DataFrame({"signs": seqs})

    def _h(self, **extra):
        return hypotheses.new_hypothesis("middle_final_slot", dict(self.P, **extra), "x", n_perm=200)

    def test_finds_planted_end_slot(self):
        res = hypotheses.run_test(self._h(), self._texts(True))
        self.assertLess(res.p_value, 0.01)
        self.assertGreater(res.observed, 0.95)

    def test_random_position_not_flagged(self):
        self.assertGreater(hypotheses.run_test(self._h(), self._texts(False)).p_value, 0.01)

    def test_false_positive_rate_near_alpha(self):
        hits = sum(hypotheses.run_test(self._h(), self._texts(False, n=150, seed=k), n_perm=100).p_value < 0.05
                   for k in range(30))
        self.assertLessEqual(hits, 5)

    def test_middle_extraction(self):
        m = hypotheses._middle(["O1", "G2", "A", "B", "C1", "C1"], {"O1"}, {"C1"}, {"G2", "G60"})
        self.assertEqual(m, ["A", "B"])
        self.assertIsNone(hypotheses._middle(["O1", "A", "B"], {"O1"}, {"C1"}, {"G2"}))  # no closer
        self.assertIsNone(hypotheses._middle(["A", "B", "C1"], {"O1"}, {"C1"}, {"G2"}, require_heading=True))
        self.assertEqual(hypotheses._middle(["A", "G2", "B", "C1"], {"O1"}, {"C1"}, {"G2"}), ["A", "G2", "B"])


class TemplateOrderTests(unittest.TestCase):
    """Positive and negative controls for the slot-order (template_order) test."""
    P = {"openers": ["O1", "O2"], "middle": [f"M{k}" for k in range(8)], "closers": ["C1", "C2"]}

    def _texts(self, ordered, n=300, seed=0, site="A"):
        r = np.random.default_rng(seed)
        seqs = []
        for _ in range(n):
            body = [f"M{int(r.integers(8))}" for _ in range(int(r.integers(1, 4)))]
            s = ([f"O{int(r.integers(1, 3))}"] if r.random() < 0.6 else []) + body + \
                ([f"C{int(r.integers(1, 3))}"] if r.random() < 0.7 else [])
            s += [f"F{int(r.integers(5))}"] if r.random() < 0.3 else []  # unrelated sign, ignored
            if not ordered:
                s = list(r.permutation(s))
            seqs.append(s)
        return pd.DataFrame({"signs": seqs, "site": site})

    def _h(self, **extra):
        return hypotheses.new_hypothesis("template_order", dict(self.P, **extra), "x", n_perm=200)

    def test_finds_planted_order(self):
        res = hypotheses.run_test(self._h(), self._texts(True))
        self.assertLess(res.p_value, 0.01)
        self.assertGreater(res.observed, 0.95)

    def test_shuffled_texts_not_flagged(self):
        self.assertGreater(hypotheses.run_test(self._h(), self._texts(False)).p_value, 0.01)

    def test_false_positive_rate_near_alpha(self):
        hits = sum(hypotheses.run_test(self._h(), self._texts(False, n=150, seed=k), n_perm=100).p_value < 0.05
                   for k in range(30))
        self.assertLessEqual(hits, 5)  # about 1.5 expected at alpha 0.05

    def test_exclude_drops_texts(self):
        df = pd.concat([self._texts(True, site="A"), self._texts(False, seed=1, site="B")], ignore_index=True)
        h = self._h(exclude=[{"field": "site", "value": "A"}])
        self.assertGreater(hypotheses.run_test(h, df).p_value, 0.01)
        self.assertLess(hypotheses.run_test(self._h(exclude=[{"field": "site", "value": "B"}]), df).p_value, 0.01)

    def test_unscorable_texts_ignored(self):
        df = pd.DataFrame({"signs": [["M1", "M2"], ["F1", "F2"], ["O1"], ["C1", "C2"]]})
        res = hypotheses.run_test(self._h(), df)
        self.assertEqual(res.n_support, 0)


class UnitTests(unittest.TestCase):
    def _texts(self, seed=0):
        r = np.random.default_rng(seed)
        seqs = []
        for i in range(400):
            body = list(r.choice([f"F{k}" for k in range(25)], size=3))
            seqs.append((["O1", "O2"] if i % 2 == 0 else []) + body + (["C1", "C2"] if i % 3 == 0 else []))
        site = ["A" if i % 4 == 0 else "B" for i in range(400)]
        obj = ["seal" if i % 2 == 0 else "tablet" for i in range(400)]
        return pd.DataFrame({"signs": seqs, "site": site, "object_type": obj})

    def test_unit_position_open_and_close(self):
        df = self._texts()
        h = hypotheses.new_hypothesis("unit_position", {"units": [["O1", "O2"]], "where": "start"}, "x", n_perm=200)
        self.assertLess(hypotheses.run_test(h, df).p_value, 0.01)
        h = hypotheses.new_hypothesis("unit_position", {"units": [["C1", "C2"]], "where": "end"}, "x", n_perm=200)
        self.assertLess(hypotheses.run_test(h, df).p_value, 0.01)
        h = hypotheses.new_hypothesis("unit_position", {"units": [["O1", "O2"]], "where": "end"}, "x", n_perm=200)
        self.assertGreater(hypotheses.run_test(h, df).p_value, 0.05)

    def test_unit_recurrence(self):
        df = self._texts()
        h = hypotheses.new_hypothesis("unit_recurrence", {"units": [["O1", "O2"], ["C1", "C2"]]}, "x", n_perm=200)
        self.assertLess(hypotheses.run_test(h, df).p_value, 0.01)
        h = hypotheses.new_hypothesis("unit_recurrence", {"units": [["F1", "F2"], ["F3", "F4"]]}, "x", n_perm=200)
        self.assertGreater(hypotheses.run_test(h, df).p_value, 0.01)

    def test_merge_units(self):
        self.assertEqual(hypotheses.merge_units([["A", "B", "C", "A", "B"]], [["A", "B"]]), [["A+B", "C", "A+B"]])

    def test_association_within_subgroup(self):
        df = self._texts()
        # O1 occurs only on even texts, which are all seals: within seals it says nothing about object type
        h = hypotheses.new_hypothesis("class_association", {"signs": ["O1"], "field": "object_type", "value": "seal"},
                                      "x", n_perm=200)
        self.assertLess(hypotheses.run_test(h, df).p_value, 0.01)
        h = hypotheses.new_hypothesis("class_association", {"signs": ["O1"], "field": "site", "value": "A",
                                                            "within": {"field": "object_type", "value": "seal"}},
                                      "x", n_perm=200)
        self.assertGreater(hypotheses.run_test(h, df).p_value, 0.01)

    def test_motif_group(self):
        self.assertEqual(data.motif_group("Bull1:W"), "unicorn")
        self.assertEqual(data.motif_group("Elep"), "Elep")
        self.assertEqual(data.motif_group("unknown"), "none")


class GroupContrastTests(unittest.TestCase):
    def _df(self, differ: bool, seed=0):
        r = np.random.default_rng(seed)
        rows = []
        for i in range(400):
            g = "U" if i % 2 == 0 else "Z"
            pool = [f"F{k}" for k in range(20)] + (["U1", "U2"] * 5 if (differ and g == "U") else [])
            rows.append({"signs": list(r.choice(pool, size=5)), "motif_group": g, "site": "M", "object_type": "seal"})
        return pd.DataFrame(rows)

    def test_detects_different_sign_mix(self):
        h = hypotheses.new_hypothesis("group_contrast", {"field": "motif_group", "value": "U",
                                      "within": [{"field": "site", "value": "M"}, {"field": "object_type", "value": "seal"}]},
                                      "x", n_perm=200)
        self.assertLess(hypotheses.run_test(h, self._df(True)).p_value, 0.01)

    def test_no_difference_not_flagged(self):
        h = hypotheses.new_hypothesis("group_contrast", {"field": "motif_group", "value": "U"}, "x", n_perm=200)
        self.assertGreater(hypotheses.run_test(h, self._df(False)).p_value, 0.01)
