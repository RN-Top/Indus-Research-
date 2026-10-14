"""Entropy measures used to replicate Rao et al. (2009a) and Rao (2010).

Block entropy of order N is the Shannon entropy of the distribution of
N-sign blocks taken from inside texts (blocks never cross text boundaries).
Following Rao (2010), the logarithm is taken to base L, the alphabet size, so
that sequences over different alphabets can be compared: the normalised
block entropy then runs from 0 (fully rigid) to N (fully random).

Plug-in entropy estimates are biased downward when blocks are rare, which
matters a lot for a corpus this small at N >= 3. The Miller-Madow correction
is offered as one standard adjustment, and every number is reported next to
controls processed in exactly the same way, so the bias affects both sides
of each comparison.
"""

from __future__ import annotations

import math
from collections import Counter

import numpy as np


def _entropy_from_counts(counts: Counter, base: float, miller_madow: bool) -> float:
    n = sum(counts.values())
    if n == 0:
        return float("nan")
    p = np.array(list(counts.values()), dtype=float) / n
    h = -float(np.sum(p * np.log(p)))
    if miller_madow:
        h += (len(counts) - 1) / (2 * n)
    return h / math.log(base)


def block_counts(seqs: list[list[str]], n: int) -> Counter:
    c: Counter = Counter()
    for seq in seqs:
        for i in range(len(seq) - n + 1):
            c[tuple(seq[i:i + n])] += 1
    return c


def block_entropy(seqs: list[list[str]], n: int, alphabet_size: int | None = None,
                  miller_madow: bool = False) -> float:
    L = alphabet_size or len({s for q in seqs for s in q})
    if L < 2:
        return float("nan")
    return _entropy_from_counts(block_counts(seqs, n), L, miller_madow)


def block_entropy_curve(seqs: list[list[str]], max_n: int = 6, alphabet_size: int | None = None,
                        miller_madow: bool = False) -> list[float]:
    return [block_entropy(seqs, n, alphabet_size, miller_madow) for n in range(1, max_n + 1)]


def conditional_entropy(seqs: list[list[str]], alphabet_size: int | None = None,
                        miller_madow: bool = False) -> float:
    """H(X_t | X_{t-1}) within texts, as in Rao et al. (2009a). Base L."""
    L = alphabet_size or len({s for q in seqs for s in q})
    return (block_entropy(seqs, 2, L, miller_madow)
            - _entropy_from_counts(Counter(s for q in seqs for s in q[:-1]), L, miller_madow))


def blocks_available(seqs: list[list[str]], n: int) -> tuple[int, int]:
    """Number of block tokens and distinct block types at order n.

    Shown beside every entropy value so a reader can judge how far to trust it.
    """
    c = block_counts(seqs, n)
    return sum(c.values()), len(c)
