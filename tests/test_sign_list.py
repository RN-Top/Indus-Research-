"""Every sign in the bundled full corpus must be a sign in Fuls's list.

Fuls, Corpus of Indus Inscriptions (2022), Table 2.6, pp. 22-24: 713 signs,
numbered 001-958, plus 000 (illegible) and 999 (blank space), p. 21.
"""

import csv
import unittest
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


def fuls_signs() -> set[int]:
    with open(DATA / "fuls_sign_list.csv", newline="") as f:
        return {int(r["sign_id"]) for r in csv.DictReader(f)}


class TestFulsSignList(unittest.TestCase):
    def test_list_matches_book(self):
        signs = fuls_signs() - {0, 999}
        self.assertEqual(len(signs), 713)
        self.assertEqual((min(signs), max(signs)), (1, 958))

    def test_corpus_signs_are_in_list(self):
        valid = fuls_signs()
        bad = set()
        with open(DATA / "indus_website_real_corpus.csv", newline="") as f:
            for row in csv.DictReader(f):
                for s in row["sign_sequence"].split():
                    if not (s.startswith("G") and s[1:].isdigit() and int(s[1:]) in valid):
                        bad.add(s)
        self.assertFalse(bad, f"signs not in Fuls's list: {sorted(bad)}")


if __name__ == "__main__":
    unittest.main()
