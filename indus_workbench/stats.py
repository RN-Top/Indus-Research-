"""Descriptive statistics: frequencies, positions, n-grams."""

from __future__ import annotations

from collections import Counter

import numpy as np
import pandas as pd


def sign_frequencies(seqs: list[list[str]]) -> pd.DataFrame:
    tok = Counter(s for seq in seqs for s in seq)
    txt = Counter(s for seq in seqs for s in set(seq))
    total = sum(tok.values()) or 1
    df = pd.DataFrame({
        "sign": list(tok),
        "tokens": [tok[s] for s in tok],
        "texts": [txt[s] for s in tok],
    })
    df["share"] = df["tokens"] / total
    return df.sort_values("tokens", ascending=False).reset_index(drop=True)


def ngram_counts(seqs: list[list[str]], n: int) -> Counter:
    c: Counter = Counter()
    for seq in seqs:
        for i in range(len(seq) - n + 1):
            c[tuple(seq[i:i + n])] += 1
    return c


def positional_profile(seqs: list[list[str]], bins: int = 3) -> pd.DataFrame:
    """Where each sign tends to sit, normalised for text length.

    Position p in a text of length L maps to (p + 0.5) / L in [0, 1], then is
    binned into start / middle / end (for bins=3). Single-sign texts are
    counted separately as 'solo' because they have no position.
    """
    rows: dict[str, np.ndarray] = {}
    solo: Counter = Counter()
    for seq in seqs:
        L = len(seq)
        if L == 1:
            solo[seq[0]] += 1
            continue
        for p, s in enumerate(seq):
            b = min(int((p + 0.5) / L * bins), bins - 1)
            rows.setdefault(s, np.zeros(bins))[b] += 1
    labels = ["start", "middle", "end"] if bins == 3 else [f"bin{i + 1}" for i in range(bins)]
    df = pd.DataFrame.from_dict(rows, orient="index", columns=labels)
    df["solo"] = pd.Series(solo)
    df = df.fillna(0)
    df["n"] = df[labels].sum(axis=1)
    for lab in labels:
        df[f"{lab}_share"] = np.where(df["n"] > 0, df[lab] / df["n"].where(df["n"] > 0, 1), 0)
    df.index.name = "sign"
    return df.sort_values("n", ascending=False)


def length_distribution(seqs: list[list[str]]) -> pd.Series:
    return pd.Series(Counter(len(s) for s in seqs)).sort_index()


def neighbour_sets(seqs: list[list[str]]) -> tuple[dict, dict]:
    """For each sign, the multiset of signs before and after it."""
    before: dict[str, Counter] = {}
    after: dict[str, Counter] = {}
    for seq in seqs:
        padded = ["<s>"] + seq + ["</s>"]
        for i in range(1, len(padded) - 1):
            s = padded[i]
            before.setdefault(s, Counter())[padded[i - 1]] += 1
            after.setdefault(s, Counter())[padded[i + 1]] += 1
    return before, after
