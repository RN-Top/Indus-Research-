"""Testing proposed sign readings (decipherment keys).

A reading hypothesis assigns a sound value to each sign and names a lexicon
of words in the proposed language, each with a published source. The test
asks one question: does applying the key to the corpus produce lexicon words
more often than keys made by shuffling the same values among signs of
similar frequency? A key that does no better than its shuffles is not
evidence, however convincing individual readings look.

Ported from the repository's first version of the app and changed in two
ways for rigour: the held-out texts are the same locked holdout used
everywhere else (no user-chosen split or seed), and records are plain JSON
with a SHA-256 fingerprint, like the other hypotheses.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections.abc import Sequence
from datetime import datetime, timezone

import numpy as np
import pandas as pd

MATCH_MODES = {
    "exact": "Exact spelling",
    "no_diacritics": "Ignore diacritics (ā = a)",
    "consonants": "Consonants only",
}

FINGERPRINT_FIELDS = ["key", "lexicon", "match_mode", "source_key", "metric", "n_null", "bands", "seed",
                      "read_mode", "data_settings"]


# Records ---------------------------------------------------------------------

def new_reading(name: str, key: dict[str, str], lexicon: list[dict], *, language: str = "",
                author: str = "", description: str = "", match_mode: str = "no_diacritics",
                source_key: str = "indus_website", metric: str = "char_coverage",
                n_null: int = 1000, bands: int = 5, seed: int = 0, read_mode: str = "full",
                data_settings: dict | None = None) -> dict:
    return {
        "type": "reading", "name": name, "language": language, "author": author,
        "description": description,
        "key": {k: v for k, v in sorted(key.items()) if str(v).strip()},
        "lexicon": sorted(({"form": e["form"], "gloss": e.get("gloss", ""), "source": e.get("source", "")}
                           for e in lexicon if str(e.get("form", "")).strip()),
                          key=lambda e: (e["form"], e["gloss"], e["source"])),
        "match_mode": match_mode, "source_key": source_key, "metric": metric,
        "n_null": n_null, "bands": bands, "seed": seed,
        # "full": a text is read only if every sign has a value.
        # "runs": every run of 2+ consecutive valued signs is read (for partial keys).
        "read_mode": read_mode,
        "data_settings": data_settings or {"drop_damaged": True, "dedupe": False, "drop_unidentified": True},
    }


def fingerprint(r: dict) -> str:
    core = {k: r.get(k) for k in FINGERPRINT_FIELDS}
    return hashlib.sha256(json.dumps(core, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def freeze(r: dict) -> dict:
    r = dict(r)
    r["frozen_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    r["sha256"] = fingerprint(r)
    r["id"] = f"R-{r['frozen_utc'][:10]}-{r['sha256'][:8]}"
    return r


def verify(r: dict) -> bool:
    return "sha256" in r and fingerprint(r) == r["sha256"]


# Matching --------------------------------------------------------------------

def normalise(text: str, mode: str) -> str:
    text = text.lower().replace("-", "").replace(" ", "")
    if mode in ("no_diacritics", "consonants"):
        text = "".join(c for c in unicodedata.normalize("NFD", text) if not unicodedata.combining(c))
    if mode == "consonants":
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

    def __init__(self, texts: Sequence[Sequence[str]], lexicon: Sequence[dict], mode: str,
                 read_mode: str = "full"):
        self.texts = [list(t) for t in texts]
        self.mode = mode
        self.read_mode = read_mode
        self.words = {w for w in (normalise(e["form"], mode) for e in lexicon) if w}
        self.max_len = max((len(w) for w in self.words), default=0)

    def readings(self, key: dict[str, str]) -> list[str | None]:
        if self.read_mode == "runs":
            return self._run_readings(key)
        out = []
        for t in self.texts:
            if not t or any(not key.get(s) for s in t):
                out.append(None)  # a text is readable only if every sign has a value
            else:
                out.append(normalise("".join(key[s] for s in t), self.mode))
        return out

    def _run_readings(self, key: dict[str, str]) -> list[str | None]:
        """Each run of 2+ consecutive signs that all have values becomes one reading."""
        out: list[str | None] = []
        for t in self.texts:
            run: list[str] = []
            for s in list(t) + [None]:
                if s is not None and key.get(s):
                    run.append(s)
                    continue
                if len(run) >= 2:
                    out.append(normalise("".join(key[x] for x in run), self.mode))
                run = []
        return out

    def score(self, key: dict[str, str]) -> dict[str, float]:
        read = [r for r in self.readings(key) if r]
        full = sum(1 for r in read if segment(r, self.words, self.max_len) is not None)
        chars = sum(len(r) for r in read)
        cov = sum(covered_chars(r, self.words, self.max_len) for r in read)
        return {
            "texts": len(self.texts), "readable": len(read),
            "coverage": len(read) / len(self.texts) if self.texts else 0.0,
            "full_match": full,
            "full_match_rate": full / len(read) if read else 0.0,
            "char_coverage": cov / chars if chars else 0.0,
        }


METRICS = {
    "char_coverage": "Share of reading covered by lexicon words",
    "full_match_rate": "Share of texts read entirely as lexicon words",
}


# Null model ------------------------------------------------------------------

def frequency_bands(texts, signs, bands: int) -> dict[str, int]:
    sset = set(signs)
    counts = pd.Series([s for t in texts for s in t if s in sset], dtype=object).value_counts()
    ranked = list(counts.index) + [s for s in signs if s not in counts.index]
    size = max(1, int(np.ceil(len(ranked) / bands)))
    return {s: i // size for i, s in enumerate(ranked)}


def shuffled_key(key: dict[str, str], band_of: dict[str, int], rng: np.random.Generator) -> dict[str, str]:
    """Permute values among assigned signs within the same frequency band."""
    out: dict[str, str] = {}
    by_band: dict[int, list[str]] = {}
    for s, v in key.items():
        if v:
            by_band.setdefault(band_of.get(s, -1), []).append(s)
    for members in by_band.values():
        values = [key[s] for s in members]
        rng.shuffle(values)
        out.update(zip(members, values))
    return out


def null_distribution(scorer: Scorer, key: dict[str, str], n: int = 1000, bands: int = 5,
                      seed: int = 0, metric: str = "char_coverage") -> np.ndarray:
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


def warnings(r: dict) -> list[str]:
    """Problems that weaken a test, shown before it is run."""
    out = []
    missing = [e["form"] for e in r["lexicon"] if not str(e.get("source", "")).strip()]
    if missing:
        out.append(f"{len(missing)} lexicon forms have no source: {', '.join(missing[:8])}")
    values = {normalise(v, r["match_mode"]) for v in r["key"].values() if v}
    trivial = sorted({e["form"] for e in r["lexicon"] if normalise(e["form"], r["match_mode"]) in values})
    if trivial:
        out.append(f"{len(trivial)} lexicon forms equal a single sign value ({', '.join(trivial[:8])}). "
                   "They match under most shuffled keys too, so they make the test weaker.")
    if len(set(r["key"].values())) < len(r["key"]) / 2:
        out.append("Many signs share the same value, which leaves the shuffle little to permute.")
    return out
