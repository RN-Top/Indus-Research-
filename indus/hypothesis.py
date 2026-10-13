"""Decipherment hypotheses as testable objects.

A hypothesis is a sign-to-value key, a lexicon of target-language forms with
sources, and matching rules. Scoring asks one question: does applying the key
to the corpus produce lexicon words more often than keys made by shuffling the
same values among signs of similar frequency? A reading that does no better
than its shuffles is not evidence, however good individual readings look.

Locking records a SHA-256 of everything that affects the score, plus which
texts are held out, so a hypothesis cannot be quietly tuned after testing.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections.abc import Sequence
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field

from .schema import UNREADABLE


class MatchMode(str, Enum):
    exact = "exact"
    no_diacritics = "no_diacritics"
    consonants = "consonants"


class LexEntry(BaseModel):
    form: str
    gloss: str = ""
    source: str


class Hypothesis(BaseModel):
    name: str
    author: str = ""
    language: str = ""
    description: str = ""
    key: dict[str, str] = Field(default_factory=dict)
    lexicon: list[LexEntry] = Field(default_factory=list)
    match_mode: MatchMode = MatchMode.no_diacritics
    heldout_fraction: float = Field(0.2, ge=0, lt=1)
    heldout_seed: int = 0
    locked_at: str | None = None
    locked_hash: str | None = None

    # Locking -----------------------------------------------------------------

    def content_hash(self) -> str:
        payload = self.model_dump(mode="json", exclude={"locked_at", "locked_hash", "author", "description"})
        payload["key"] = {k: v for k, v in sorted(payload["key"].items()) if v}
        payload["lexicon"] = sorted(payload["lexicon"], key=lambda e: (e["form"], e["gloss"], e["source"]))
        return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

    def lock(self) -> "Hypothesis":
        return self.model_copy(
            update={
                "locked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "locked_hash": self.content_hash(),
            }
        )

    @property
    def status(self) -> str:
        if not self.locked_hash:
            return "exploratory"
        return "locked" if self.locked_hash == self.content_hash() else "changed after lock"

    def save(self, directory: str | Path) -> Path:
        path = Path(directory) / f"{slug(self.name)}.json"
        path.write_text(self.model_dump_json(indent=2))
        return path


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "hypothesis"


def load_hypotheses(directory: str | Path) -> dict[str, Hypothesis]:
    out = {}
    for path in sorted(Path(directory).glob("*.json")):
        h = Hypothesis.model_validate_json(path.read_text())
        out[h.name] = h
    return out


# Matching --------------------------------------------------------------------


def normalise(text: str, mode: MatchMode) -> str:
    text = text.lower().replace("-", "").replace(" ", "")
    if mode in (MatchMode.no_diacritics, MatchMode.consonants):
        text = "".join(c for c in unicodedata.normalize("NFD", text) if not unicodedata.combining(c))
    if mode == MatchMode.consonants:
        text = re.sub(r"[aeiouy]", "", text)
    return text


def segment(reading: str, words: set[str], max_len: int) -> list[str] | None:
    """Split `reading` entirely into lexicon words, preferring fewer words."""
    n = len(reading)
    best: list[list[str] | None] = [None] * (n + 1)
    best[0] = []
    for i in range(1, n + 1):
        for j in range(max(0, i - max_len), i):
            prev = best[j]
            if prev is not None and reading[j:i] in words:
                cand = prev + [reading[j:i]]
                if best[i] is None or len(cand) < len(best[i]):
                    best[i] = cand
    return best[n]


def covered_chars(reading: str, words: set[str], max_len: int) -> int:
    """Largest number of characters coverable by non-overlapping lexicon words."""
    n = len(reading)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i - 1]
        for j in range(max(0, i - max_len), i):
            if reading[j:i] in words:
                dp[i] = max(dp[i], dp[j] + i - j)
    return dp[n]


class Scorer:
    """Applies keys to a fixed set of texts and scores them against a lexicon."""

    def __init__(self, texts: Sequence[Sequence[str]], lexicon: Sequence[LexEntry], mode: MatchMode):
        self.texts = [list(t) for t in texts]
        self.mode = mode
        self.words = {normalise(e.form, mode) for e in lexicon if normalise(e.form, mode)}
        self.max_len = max((len(w) for w in self.words), default=0)

    def readings(self, key: dict[str, str]) -> list[str | None]:
        out = []
        for t in self.texts:
            if not t or any(s == UNREADABLE or not key.get(s) for s in t):
                out.append(None)
            else:
                out.append(normalise("".join(key[s] for s in t), self.mode))
        return out

    def score(self, key: dict[str, str]) -> dict[str, float]:
        readings = self.readings(key)
        read = [r for r in readings if r]
        full = sum(1 for r in read if segment(r, self.words, self.max_len) is not None)
        chars = sum(len(r) for r in read)
        cov = sum(covered_chars(r, self.words, self.max_len) for r in read)
        return {
            "texts": len(self.texts),
            "readable": len(read),
            "coverage": len(read) / len(self.texts) if self.texts else 0.0,
            "full_match": full,
            "full_match_rate": full / len(read) if read else 0.0,
            "char_coverage": cov / chars if chars else 0.0,
        }


# Null model ------------------------------------------------------------------


def frequency_bands(texts: Sequence[Sequence[str]], signs: Sequence[str], bands: int) -> dict[str, int]:
    counts = pd.Series([s for t in texts for s in t if s in set(signs)]).value_counts()
    ranked = [s for s in counts.index] + [s for s in signs if s not in counts.index]
    size = max(1, int(np.ceil(len(ranked) / bands)))
    return {s: i // size for i, s in enumerate(ranked)}


def shuffled_key(key: dict[str, str], band_of: dict[str, int], rng: np.random.Generator) -> dict[str, str]:
    """Permute values among assigned signs within the same frequency band."""
    out = {}
    by_band: dict[int, list[str]] = {}
    for s, v in key.items():
        if v:
            by_band.setdefault(band_of.get(s, -1), []).append(s)
    for members in by_band.values():
        values = [key[s] for s in members]
        rng.shuffle(values)
        out.update(zip(members, values))
    return out


def null_distribution(
    scorer: Scorer,
    key: dict[str, str],
    n: int = 1000,
    bands: int = 5,
    seed: int = 0,
    metric: str = "char_coverage",
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    band_of = frequency_bands(scorer.texts, [s for s, v in key.items() if v], bands)
    return np.array([scorer.score(shuffled_key(key, band_of, rng))[metric] for _ in range(n)])


def compare_to_null(real: float, null: np.ndarray) -> dict[str, float]:
    return {
        "percentile": float((null < real).mean()),
        "p_value": float((1 + (null >= real).sum()) / (1 + len(null))),
        "null_mean": float(null.mean()),
        "null_95": float(np.quantile(null, 0.95)),
    }


# Held-out split ----------------------------------------------------------------


def heldout_ids(text_ids: Sequence[str], fraction: float, seed: int) -> set[str]:
    """Deterministic split: a text is held out if its salted hash falls below `fraction`."""
    out = set()
    for tid in text_ids:
        h = hashlib.sha256(f"{seed}:{tid}".encode()).digest()
        if int.from_bytes(h[:8], "big") / 2**64 < fraction:
            out.add(tid)
    return out


def trivial_forms(h: Hypothesis) -> list[str]:
    """Lexicon forms equal to a single sign value.

    Shuffling keeps the same set of values, so such forms match under almost
    every shuffled key too. They inflate raw scores and weaken the test.
    """
    values = {normalise(v, h.match_mode) for v in h.key.values() if v}
    return sorted({e.form for e in h.lexicon if normalise(e.form, h.match_mode) in values})
