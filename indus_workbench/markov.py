"""Sequence models and their baseline.

A bigram (first-order Markov) model is compared against a unigram model that
ignores order. If the bigram model does not predict unseen texts better than
the unigram baseline, the corpus shows no usable sequential structure at
that level. Evaluation is always on texts the model was not fitted on.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict

import numpy as np

BOS, EOS, UNK = "<s>", "</s>", "<unk>"


class Unigram:
    def __init__(self, k: float = 0.5):
        self.k = k

    def fit(self, seqs):
        self.counts = Counter(x for s in seqs for x in s + [EOS])
        self.vocab = set(self.counts) | {UNK}
        self.total = sum(self.counts.values())
        return self

    def prob(self, prev, x):
        x = x if x in self.vocab else UNK
        return (self.counts.get(x, 0) + self.k) / (self.total + self.k * len(self.vocab))


class Bigram:
    """Bigram with interpolation to the unigram (Jelinek-Mercer smoothing)."""

    def __init__(self, lam: float = 0.7, k: float = 0.5):
        self.lam, self.k = lam, k

    def fit(self, seqs):
        self.uni = Unigram(self.k).fit(seqs)
        self.big: dict[str, Counter] = defaultdict(Counter)
        for s in seqs:
            padded = [BOS] + s + [EOS]
            for a, b in zip(padded, padded[1:]):
                self.big[a][b] += 1
        return self

    def prob(self, prev, x):
        row = self.big.get(prev)
        p_uni = self.uni.prob(prev, x)
        if not row:
            return p_uni
        p_big = row.get(x, 0) / sum(row.values())
        return self.lam * p_big + (1 - self.lam) * p_uni

    def transitions(self, top: int = 50):
        rows = []
        for a, row in self.big.items():
            tot = sum(row.values())
            for b, c in row.items():
                rows.append((a, b, c, c / tot))
        rows.sort(key=lambda r: -r[2])
        return rows[:top]


def log_loss(model, seqs) -> float:
    """Average bits per sign (including the end-of-text symbol) on `seqs`."""
    bits, n = 0.0, 0
    for s in seqs:
        padded = [BOS] + s + [EOS]
        for a, b in zip(padded, padded[1:]):
            bits -= math.log2(model.prob(a, b))
            n += 1
    return bits / max(n, 1)


def cross_validate(seqs, k: int = 5, seed: int = 0, lam: float = 0.7) -> dict:
    """k-fold cross-validation by text. Returns bits/sign for both models per
    fold plus the paired difference. Uses only the data passed in, so the
    locked holdout is never touched here."""
    r = np.random.default_rng(seed)
    idx = r.permutation(len(seqs))
    folds = np.array_split(idx, k)
    uni, big = [], []
    for f in folds:
        fset = set(f.tolist())
        test = [seqs[i] for i in f]
        train = [seqs[i] for i in idx if i not in fset]
        uni.append(log_loss(Unigram().fit(train), test))
        big.append(log_loss(Bigram(lam).fit(train), test))
    diff = np.array(uni) - np.array(big)
    return {
        "unigram_bits": uni, "bigram_bits": big,
        "mean_gain_bits": float(diff.mean()),
        "folds_bigram_better": int((diff > 0).sum()), "k": k,
    }
