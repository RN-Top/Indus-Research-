"""Descriptive statistics over sign sequences.

All functions take an iterable of texts, each a list of sign IDs in reading
order. Unreadable signs ("?") are dropped from counts, and an n-gram that
would span an unreadable sign is not counted.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Sequence

import numpy as np
import pandas as pd

from .schema import UNREADABLE

Texts = Iterable[Sequence[str]]


def readable_segments(signs: Sequence[str]) -> list[list[str]]:
    """Split a text at unreadable signs, so n-grams never bridge a gap."""
    segments, current = [], []
    for s in signs:
        if s == UNREADABLE:
            if current:
                segments.append(current)
            current = []
        else:
            current.append(s)
    if current:
        segments.append(current)
    return segments


def sign_frequencies(texts: Texts) -> pd.DataFrame:
    counts = Counter(s for t in texts for s in t if s != UNREADABLE)
    df = pd.DataFrame(counts.most_common(), columns=["sign", "count"])
    if df.empty:
        return df.assign(share=[], rank=[])
    df["share"] = df["count"] / df["count"].sum()
    df["rank"] = np.arange(1, len(df) + 1)
    return df


def zipf_fit(freq: pd.DataFrame) -> dict[str, float]:
    """Least-squares fit of log(count) = a + b * log(rank).

    Natural language word frequencies give b near -1. Sign systems with a
    large logographic component usually give a steeper head and a long tail of
    rare signs; the slope alone does not show whether a system is writing.
    """
    if len(freq) < 3:
        return {"slope": float("nan"), "intercept": float("nan"), "r2": float("nan")}
    x = np.log(freq["rank"].to_numpy(float))
    y = np.log(freq["count"].to_numpy(float))
    b, a = np.polyfit(x, y, 1)
    resid = y - (a + b * x)
    r2 = 1 - resid.var() / y.var() if y.var() > 0 else float("nan")
    return {"slope": float(b), "intercept": float(a), "r2": float(r2)}


def summary(texts: Texts) -> dict[str, float]:
    texts = [list(t) for t in texts]
    readable = [s for t in texts for s in t if s != UNREADABLE]
    counts = Counter(readable)
    lengths = [len(t) for t in texts]
    return {
        "texts": len(texts),
        "sign_tokens": len(readable),
        "sign_types": len(counts),
        "hapax_types": sum(1 for c in counts.values() if c == 1),
        "hapax_share_of_types": (sum(1 for c in counts.values() if c == 1) / len(counts)) if counts else 0.0,
        "mean_length": float(np.mean(lengths)) if lengths else 0.0,
        "median_length": float(np.median(lengths)) if lengths else 0.0,
        "max_length": max(lengths, default=0),
        "unreadable_tokens": sum(1 for t in texts for s in t if s == UNREADABLE),
    }


def length_distribution(texts: Texts) -> pd.DataFrame:
    c = Counter(len(t) for t in texts)
    return pd.DataFrame(sorted(c.items()), columns=["length", "texts"])


def positional_profile(texts: Texts, min_count: int = 1) -> pd.DataFrame:
    """Where each sign occurs: as the sole sign, first, last, or in between.

    Positions are taken from the full text in reading order, so a sign next to
    an unreadable sign keeps its true position.
    """
    rows: Counter[tuple[str, str]] = Counter()
    for t in texts:
        n = len(t)
        for i, s in enumerate(t):
            if s == UNREADABLE:
                continue
            pos = "solo" if n == 1 else "initial" if i == 0 else "final" if i == n - 1 else "medial"
            rows[(s, pos)] += 1
    if not rows:
        return pd.DataFrame(columns=[
            "sign", "solo", "initial", "medial", "final", "total",
            "initial_share", "medial_share", "final_share", "dominant",
        ])
    df = (
        pd.Series(rows).rename_axis(["sign", "position"]).unstack(fill_value=0)
        .reindex(columns=["solo", "initial", "medial", "final"], fill_value=0)
    )
    df["total"] = df.sum(axis=1)
    df = df[df["total"] >= min_count].sort_values("total", ascending=False)
    for col in ("initial", "medial", "final"):
        df[f"{col}_share"] = df[col] / df["total"]
    df["dominant"] = df[["solo", "initial", "medial", "final"]].idxmax(axis=1)
    return df.reset_index()


def ngrams(texts: Texts, n: int, min_count: int = 1) -> pd.DataFrame:
    """Counts of n-grams within texts (never across text boundaries)."""
    if n < 1:
        raise ValueError("n must be at least 1")
    counts: Counter[tuple[str, ...]] = Counter()
    for t in texts:
        for seg in readable_segments(t):
            for i in range(len(seg) - n + 1):
                counts[tuple(seg[i : i + n])] += 1
    df = pd.DataFrame(
        [(" ".join(k), v) for k, v in counts.items() if v >= min_count],
        columns=["ngram", "count"],
    )
    if df.empty:
        return df.assign(share=[])
    total = sum(counts.values())
    df["share"] = df["count"] / total
    return df.sort_values(["count", "ngram"], ascending=[False, True]).reset_index(drop=True)


def ngram_coverage(texts: Texts, n: int, top: int) -> float:
    """Share of all n-gram tokens accounted for by the `top` most frequent n-grams."""
    df = ngrams(texts, n)
    if df.empty:
        return 0.0
    return float(df["count"].head(top).sum() / df["count"].sum())
