"""Write two demonstration hypotheses for the synthetic sample into hypotheses/.

Neither is a reading of the Indus script. They show how the test behaves:

* "Demo: planted key" builds its lexicon from frequent sign sequences read
  with its own key, the situation a correct decipherment would be in. It
  should beat almost every shuffled key.
* "Demo: unrelated lexicon" uses the same key with a lexicon of random
  syllable strings. It should score no better than its shuffles.

Run:  python scripts/make_demo_hypotheses.py
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from indus import load_corpus  # noqa: E402
from indus.hypothesis import Hypothesis, LexEntry  # noqa: E402
from indus.stats import ngrams  # noqa: E402

SYLLABLES = [c + v for c in "kgcjtdnpbmyrlvs" for v in "aiu"]


def main() -> None:
    rng = random.Random(42)
    corpus = load_corpus(ROOT / "data" / "sample")
    signs = corpus.signs["sign_id"].tolist()
    values = rng.sample(SYLLABLES, len(signs))
    key = dict(zip(signs, values))
    texts = corpus.texts["signs"].tolist()

    planted = []
    for n in (2, 3):
        for gram in ngrams(texts, n)["ngram"].head(25):
            form = "".join(key[s] for s in gram.split())
            planted.append(LexEntry(form=form, gloss=f"reading of {gram}", source="Demo: built from the key itself"))

    unrelated = [
        LexEntry(form="".join(rng.choice(SYLLABLES) for _ in range(rng.choice([1, 2, 2, 3]))),
                 gloss="random string", source="Demo: random syllables")
        for _ in range(len(planted))
    ]

    common = dict(author="Indus Script Research demo", language="none (demonstration)", key=key,
                  heldout_fraction=0.2, heldout_seed=7)
    demos = [
        Hypothesis(name="Demo: planted key", lexicon=planted, description=(
            "Lexicon built from frequent sequences read with this key. Shows what a passing result "
            "looks like. Not a reading of the Indus script."), **common),
        Hypothesis(name="Demo: unrelated lexicon", lexicon=unrelated, description=(
            "Same key, lexicon of random syllable strings. Shows what chance looks like. "
            "Not a reading of the Indus script."), **common),
    ]
    for h in demos:
        print("wrote", h.lock().save(ROOT / "hypotheses"))


if __name__ == "__main__":
    main()
