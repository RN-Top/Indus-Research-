"""Search texts by sign sequence.

Pattern syntax, written in reading order with signs separated by spaces:

    FISH JAR        the two signs adjacent, anywhere in the text
    ^ FISH          text begins with FISH
    JAR $           text ends with JAR
    FISH * JAR      FISH, any one sign, then JAR
    FISH ... JAR    FISH, then JAR later in the same text
"""

from __future__ import annotations

import re

import pandas as pd

_TOKEN = re.compile(r"^[A-Za-z0-9_?-]+$")


class PatternError(ValueError):
    pass


def compile_pattern(pattern: str) -> re.Pattern[str]:
    """Compile a sign pattern to a regex over a space-padded sequence string."""
    tokens = pattern.split()
    start = bool(tokens) and tokens[0] == "^"
    end = bool(tokens) and tokens[-1] == "$"
    body = tokens[int(start) : len(tokens) - int(end)]
    if not [t for t in body if t != "..."]:
        raise PatternError("Enter at least one sign.")
    regex = "^" if start else ""
    for tok in body:
        if tok == "*":
            regex += r" \S+"
        elif tok == "...":
            regex += r"(?: \S+)*?"
        elif _TOKEN.match(tok):
            regex += " " + re.escape(tok)
        else:
            raise PatternError(f"'{tok}' is not a valid sign ID.")
    regex += " $" if end else "(?= )"
    return re.compile(regex)


def matches(rx: re.Pattern[str], signs: list[str]) -> bool:
    return bool(rx.search(" " + " ".join(signs) + " "))


def search(
    table: pd.DataFrame,
    pattern: str = "",
    sites: list[str] | None = None,
    object_types: list[str] | None = None,
    iconography: str = "",
) -> pd.DataFrame:
    """Filter a text table (from Corpus.text_table) by sequence and metadata."""
    mask = pd.Series(True, index=table.index)
    if pattern.strip():
        rx = compile_pattern(pattern)
        mask &= table["signs"].map(lambda s: matches(rx, s))
    if sites:
        mask &= table["site"].isin(sites)
    if object_types:
        mask &= table["object_type"].isin(object_types)
    if iconography.strip():
        mask &= table["iconography"].str.contains(iconography.strip(), case=False, regex=False)
    return table[mask]
