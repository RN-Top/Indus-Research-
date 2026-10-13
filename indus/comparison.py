"""Comparison corpora for the structure statistics.

Each corpus is one CSV in data/comparison/ with columns:
    text_id, signs (space-separated tokens in reading order), and a
    `# source:` comment on the first line naming where the data came from.
A second comment line `# kind: linguistic` or `# kind: non-linguistic`
says which group the corpus belongs to.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class ComparisonCorpus:
    name: str
    kind: str
    source: str
    texts: list[list[str]]


def load_comparison(directory: str | Path) -> list[ComparisonCorpus]:
    out = []
    for path in sorted(Path(directory).glob("*.csv")):
        meta = {}
        with open(path) as f:
            for line in f:
                if not line.startswith("#"):
                    break
                key, _, value = line[1:].partition(":")
                meta[key.strip()] = value.strip()
        df = pd.read_csv(path, comment="#", dtype=str, keep_default_na=False)
        texts = [s.split() for s in df["signs"] if s.strip()]
        out.append(
            ComparisonCorpus(
                name=path.stem.replace("_", " "),
                kind=meta.get("kind", "unknown"),
                source=meta.get("source", "no source given"),
                texts=texts,
            )
        )
    return out
