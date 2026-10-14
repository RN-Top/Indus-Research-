"""Corpus loading, normalisation, provenance and the locked holdout split.

Every analysis in the app starts from `Corpus`, so the rules that a reviewer
will check first (where the data came from, which version, what was excluded
and why, how texts were oriented, which texts are held out) all live here.
"""

from __future__ import annotations

import hashlib
import io
from dataclasses import dataclass, field

import pandas as pd

# ---------------------------------------------------------------------------
# Sources. URLs are pinned to a specific commit of the dataset repository so
# that results can be reproduced exactly. Change the revision deliberately,
# never silently, and record the change in CHANGELOG.md.
# ---------------------------------------------------------------------------

HF_REPO = "joyboseroy/indus_decipher"
HF_REVISION = "47e8616dff4d1ff62343bd74f3eeefc4afbfd4d8"


def _hf_url(filename: str) -> str:
    return f"https://huggingface.co/datasets/{HF_REPO}/resolve/{HF_REVISION}/{filename}"


SOURCES: dict[str, dict] = {
    "indus_website": {
        "label": "Full corpus: 2,543 inscriptions, 52 sites (G-numbered signs)",
        "url": _hf_url("indus_website_real_corpus.csv"),
        "sign_scheme": "G-numbers (sign list not named by the dataset card)",
        "origin": "MySQL dump from yajnadevam/indus-website on GitHub, converted to CSV by joyboseroy",
        "licence": "Derived CSV: MIT. Underlying transcription: the source repository's terms apply.",
    },
    "cisi_primary": {
        "label": "CISI: 179 Mohenjo-daro unicorn seals, primary signs",
        "url": _hf_url("cisi_real_corpus.csv"),
        "sign_scheme": "P-numbers, allographs merged",
        "origin": "Hand transcription of Parpola's CISI (mayig/indus-valley-script-corpus)",
        "licence": "MIT",
    },
    "cisi_hierarchical": {
        "label": "CISI: same seals, allographs split when attested 3+ times",
        "url": _hf_url("cisi_real_corpus_hierarchical.csv"),
        "sign_scheme": "P-numbers, partial allograph split",
        "origin": "Hand transcription of Parpola's CISI (mayig/indus-valley-script-corpus)",
        "licence": "MIT",
    },
    "cisi_allograph": {
        "label": "CISI: same seals, every allograph a separate sign",
        "url": _hf_url("cisi_real_corpus_allograph.csv"),
        "sign_scheme": "P-numbers, every allograph distinct",
        "origin": "Hand transcription of Parpola's CISI (mayig/indus-valley-script-corpus)",
        "licence": "MIT",
    },
}

# Column names the rest of the code relies on.
STANDARD_COLUMNS = [
    "text_id", "signs", "site", "object_type", "motif",
    "reading_direction", "damaged", "source_ref",
]

HOLDOUT_FRACTION = 0.20
# The salt is part of the pre-registered protocol. Changing it changes which
# texts are held out, which would let someone pick a favourable split.
HOLDOUT_SALT = "indus-workbench-holdout-v1"


@dataclass
class Exclusion:
    text_id: str
    reason: str


@dataclass
class Corpus:
    """A cleaned corpus plus everything needed to audit how it was made."""

    df: pd.DataFrame
    source_key: str
    sha256: str
    exclusions: list[Exclusion] = field(default_factory=list)
    settings: dict = field(default_factory=dict)

    @property
    def sequences(self) -> list[list[str]]:
        return list(self.df["signs"])

    @property
    def n_texts(self) -> int:
        return len(self.df)

    @property
    def n_tokens(self) -> int:
        return int(self.df["signs"].map(len).sum())

    @property
    def sign_inventory(self) -> list[str]:
        return sorted({s for seq in self.sequences for s in seq})

    def subset(self, mask: pd.Series, note: str) -> "Corpus":
        settings = dict(self.settings)
        settings.setdefault("subsets", []).append(note)
        return Corpus(self.df[mask].reset_index(drop=True), self.source_key,
                      self.sha256, list(self.exclusions), settings)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def parse_csv(raw: bytes) -> pd.DataFrame:
    """Read the raw CSV and map it to the standard columns."""
    df = pd.read_csv(io.BytesIO(raw), dtype=str, keep_default_na=False)
    cols = {c.lower().strip(): c for c in df.columns}

    def pick(*names, default=""):
        for n in names:
            if n in cols:
                return df[cols[n]]
        return pd.Series([default] * len(df), index=df.index)

    out = pd.DataFrame({
        "text_id": pick("inscription_id", "text_id", "id"),
        "raw_sequence": pick("sign_sequence", "signs", "sequence"),
        "site": pick("site", default="unknown"),
        "object_type": pick("object_type", "type", default="unknown"),
        "motif": pick("motif", default="unknown"),
        "reading_direction": pick("reading_direction", default="R-L"),
        "damaged": pick("damaged", default="False"),
        "source_ref": pick("cisi_number", "inscription_id", default=""),
    })
    for c in ["site", "object_type", "motif", "source_ref"]:
        out[c] = out[c].replace("", "unknown")
    out["damaged"] = out["damaged"].str.strip().str.lower().isin(["true", "1", "yes"])
    out["reading_direction"] = out["reading_direction"].str.strip().str.upper()
    return out


def orient(tokens: list[str], direction: str) -> list[str]:
    """Return signs in reading order.

    The dataset card defines the convention: R-L rows are used as stored and
    L-R rows are reversed. This is a storage convention, not a claim about
    how the script was read.
    """
    return list(reversed(tokens)) if direction == "L-R" else list(tokens)


def build_corpus(raw: bytes, source_key: str, *, drop_damaged: bool = True,
                 dedupe: bool = False, min_length: int = 1) -> Corpus:
    """Clean a raw CSV into a Corpus, logging every excluded text and why."""
    df = parse_csv(raw)
    exclusions: list[Exclusion] = []

    df["signs"] = [orient(str(s).split(), d)
                   for s, d in zip(df["raw_sequence"], df["reading_direction"])]

    keep = []
    seen: set[tuple] = set()
    for row in df.itertuples():
        if len(row.signs) < min_length:
            exclusions.append(Exclusion(row.text_id, f"shorter than {min_length} sign(s)"))
            keep.append(False)
            continue
        if drop_damaged and row.damaged:
            exclusions.append(Exclusion(row.text_id, "marked damaged in source"))
            keep.append(False)
            continue
        key = tuple(row.signs)
        if dedupe and key in seen:
            exclusions.append(Exclusion(row.text_id, "duplicate of an earlier identical text"))
            keep.append(False)
            continue
        seen.add(key)
        keep.append(True)

    df = df[keep].reset_index(drop=True)
    df["length"] = df["signs"].map(len)
    df["split"] = [holdout_split(t) for t in df["text_id"]]
    settings = {"drop_damaged": drop_damaged, "dedupe": dedupe, "min_length": min_length}
    return Corpus(df, source_key, sha256_bytes(raw), exclusions, settings)


def holdout_split(text_id: str) -> str:
    """Deterministically assign a text to 'explore' or 'holdout'.

    The split depends only on the text ID and a fixed salt, so it is the same
    for everyone, cannot be tuned, and does not change when other texts are
    added or removed.
    """
    h = hashlib.sha256(f"{HOLDOUT_SALT}:{text_id}".encode()).digest()
    frac = int.from_bytes(h[:8], "big") / 2**64
    return "holdout" if frac < HOLDOUT_FRACTION else "explore"


def explore_only(corpus: Corpus) -> Corpus:
    return corpus.subset(corpus.df["split"] == "explore", "exploration split only")


def holdout_only(corpus: Corpus) -> Corpus:
    return corpus.subset(corpus.df["split"] == "holdout", "HOLDOUT split")


def fetch(url: str, timeout: int = 60) -> bytes:
    """Download a source file. Kept separate so the app can cache it."""
    import urllib.request
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read()
