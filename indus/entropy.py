"""Entropy measures and control sequences.

The conditional entropy H(next sign | current sign) is the measure used by
Rao et al. (2009). Sproat (2010, 2014) showed that non-linguistic symbol
systems can fall in the same range as languages, so these values must be read
against real comparison corpora, not only against the artificial controls
generated here. Small corpora bias plug-in entropy downward; the Miller-Madow
correction is offered as a first-order fix.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from collections.abc import Sequence

import numpy as np
import pandas as pd

from .stats import Texts, readable_segments

LOG = math.log2


def _entropy(counts: Sequence[int], miller_madow: bool = False) -> float:
    total = sum(counts)
    if total == 0:
        return 0.0
    h = -sum((c / total) * LOG(c / total) for c in counts if c)
    if miller_madow:
        nonzero = sum(1 for c in counts if c)
        h += (nonzero - 1) / (2 * total * math.log(2))
    return h


def unigram_entropy(texts: Texts, miller_madow: bool = False) -> float:
    counts = Counter(s for t in texts for seg in readable_segments(t) for s in seg)
    return _entropy(list(counts.values()), miller_madow)


def _bigrams(texts: Texts, keep: set[str] | None = None) -> list[tuple[str, str]]:
    out = []
    for t in texts:
        for seg in readable_segments(t):
            for a, b in zip(seg, seg[1:]):
                if keep is None or (a in keep and b in keep):
                    out.append((a, b))
    return out


def conditional_entropy(texts: Texts, top_k: int | None = None, miller_madow: bool = False) -> float:
    """H(Y | X) in bits over within-text bigrams.

    If `top_k` is given, only bigrams whose two signs are both among the k most
    frequent signs are used, as in Rao et al. (2009), where the measure is
    plotted against k.
    """
    texts = [list(t) for t in texts]
    keep = None
    if top_k is not None:
        freq = Counter(s for t in texts for seg in readable_segments(t) for s in seg)
        keep = {s for s, _ in freq.most_common(top_k)}
    pairs = _bigrams(texts, keep)
    if not pairs:
        return float("nan")
    by_prev: dict[str, Counter[str]] = defaultdict(Counter)
    for a, b in pairs:
        by_prev[a][b] += 1
    total = len(pairs)
    return sum(
        (sum(nxt.values()) / total) * _entropy(list(nxt.values()), miller_madow)
        for nxt in by_prev.values()
    )


def conditional_entropy_curve(texts: Texts, ks: Sequence[int], miller_madow: bool = False) -> pd.DataFrame:
    texts = [list(t) for t in texts]
    return pd.DataFrame(
        {"k": list(ks), "conditional_entropy": [conditional_entropy(texts, k, miller_madow) for k in ks]}
    )


def block_entropy(texts: Texts, n: int, miller_madow: bool = False) -> float:
    """Entropy of n-sign blocks, H_n, in bits. H_n / n approaches the entropy rate."""
    counts: Counter[tuple[str, ...]] = Counter()
    for t in texts:
        for seg in readable_segments(t):
            for i in range(len(seg) - n + 1):
                counts[tuple(seg[i : i + n])] += 1
    return _entropy(list(counts.values()), miller_madow) if counts else float("nan")


# Controls -------------------------------------------------------------------


def shuffled_within_texts(texts: Texts, seed: int = 0) -> list[list[str]]:
    """Same texts and lengths with sign order randomised inside each text.

    Keeps sign frequencies and text lengths; destroys order. If the corpus's
    conditional entropy is close to this control, order carries little
    information.
    """
    rng = np.random.default_rng(seed)
    out = []
    for t in texts:
        t = list(t)
        rng.shuffle(t)
        out.append(t)
    return out


def unigram_random(texts: Texts, seed: int = 0) -> list[list[str]]:
    """Texts of the same lengths drawn independently from the sign frequencies."""
    texts = [list(t) for t in texts]
    rng = np.random.default_rng(seed)
    counts = Counter(s for t in texts for s in t)
    signs = list(counts)
    p = np.array([counts[s] for s in signs], float)
    p /= p.sum()
    return [list(rng.choice(signs, size=len(t), p=p)) for t in texts]


def rigid_order(texts: Texts) -> list[list[str]]:
    """Maximally predictable control: each text's signs sorted by frequency rank.

    This mirrors the "rigid" control in Rao et al. (2009). Like the random
    controls it is an artificial bound, not a real non-linguistic system.
    """
    texts = [list(t) for t in texts]
    rank = {s: i for i, (s, _) in enumerate(Counter(s for t in texts for s in t).most_common())}
    return [sorted(t, key=rank.__getitem__) for t in texts]


CONTROLS = {
    "Shuffled within texts": shuffled_within_texts,
    "Random from sign frequencies": unigram_random,
    "Rigid order": lambda texts, seed=0: rigid_order(texts),
}
