"""Sign classes from context (Phase 3).

Signs that play the same role in a writing system (numerals, variants of one
sign, words of one kind) tend to appear between the same neighbours. Each sign
is described by the signs immediately before and after it; profiles are
weighted by positive pointwise mutual information (PPMI) so that very common
neighbours do not dominate; similarity is the cosine between profiles.

A similarity is only meaningful against a baseline, so `neighbours` reports
each candidate's similarity as a percentile among all sign pairs, and
`variant_check` measures how well the method recovers sign pairs that an
independent transcription says are the same sign (a positive control).
"""

from __future__ import annotations

from collections import Counter, defaultdict

import numpy as np
import pandas as pd


def context_profiles(seqs, min_count: int = 15) -> tuple[list[str], np.ndarray]:
    freq = Counter(s for q in seqs for s in q)
    vec: dict[str, Counter] = defaultdict(Counter)
    for q in seqs:
        padded = ["<s>"] + list(q) + ["</s>"]
        for i in range(1, len(padded) - 1):
            vec[padded[i]]["L:" + padded[i - 1]] += 1
            vec[padded[i]]["R:" + padded[i + 1]] += 1
    signs = sorted((s for s, n in freq.items() if n >= min_count), key=lambda s: -freq[s])
    feats = sorted({f for s in signs for f in vec[s]})
    col = {f: j for j, f in enumerate(feats)}
    m = np.zeros((len(signs), len(feats)))
    for i, s in enumerate(signs):
        for f, n in vec[s].items():
            m[i, col[f]] = n
    return signs, m


def similarity(m: np.ndarray) -> np.ndarray:
    total = m.sum()
    if total == 0:
        return np.zeros((len(m), len(m)))
    pr = m.sum(1, keepdims=True) / total
    pc = m.sum(0, keepdims=True) / total
    with np.errstate(divide="ignore", invalid="ignore"):
        ppmi = np.maximum(np.log((m / total) / (pr * pc)), 0)
    ppmi = np.nan_to_num(ppmi)
    norms = np.linalg.norm(ppmi, axis=1, keepdims=True)
    ppmi = np.divide(ppmi, norms, out=np.zeros_like(ppmi), where=norms > 0)
    return ppmi @ ppmi.T


def neighbours(seqs, sign: str, k: int = 15, min_count: int = 15) -> pd.DataFrame:
    signs, m = context_profiles(seqs, min_count)
    if sign not in signs:
        return pd.DataFrame(columns=["sign", "similarity", "percentile"])
    s = similarity(m)
    i = signs.index(sign)
    all_pairs = s[np.triu_indices(len(signs), 1)]
    row = [(signs[j], s[i, j]) for j in range(len(signs)) if j != i]
    row.sort(key=lambda r: -r[1])
    out = pd.DataFrame(row[:k], columns=["sign", "similarity"])
    out["percentile"] = [float((all_pairs < v).mean()) for v in out["similarity"]]
    return out


def variant_check(seqs, pairs: list[tuple[str, str]], min_count: int = 15) -> pd.DataFrame:
    """Positive control. For each pair known (independently) to be one sign,
    the rank of the partner among all of the first sign's neighbours.
    Chance expectation is about half the number of signs."""
    signs, m = context_profiles(seqs, min_count)
    s = similarity(m)
    idx = {x: i for i, x in enumerate(signs)}
    rows = []
    for a, b in pairs:
        if a not in idx or b not in idx:
            continue
        sims = s[idx[a]].copy()
        sims[idx[a]] = -np.inf
        rank = int((sims > s[idx[a], idx[b]]).sum()) + 1
        rows.append({"sign": a, "partner": b, "similarity": float(s[idx[a], idx[b]]),
                     "rank": rank, "of": len(signs) - 1, "chance_rank": (len(signs)) / 2})
    return pd.DataFrame(rows)
