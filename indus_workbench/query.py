"""Search texts by sign sequence (from the repository's first version).

Pattern syntax, written in reading order with signs separated by spaces:

    G740 G235       the two signs adjacent, anywhere in the text
    ^ G740          text begins with G740
    G740 $          text ends with G740
    G17 * G740      G17, any one sign, then G740
    G17 ... G740    G17, then G740 later in the same text
"""

from __future__ import annotations

import re

_TOKEN = re.compile(r"^[A-Za-z0-9_?-]+$")


class PatternError(ValueError):
    pass


def compile_pattern(pattern: str) -> re.Pattern[str]:
    tokens = pattern.split()
    start = bool(tokens) and tokens[0] == "^"
    end = bool(tokens) and tokens[-1] == "$"
    body = tokens[int(start): len(tokens) - int(end)]
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
