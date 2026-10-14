"""Controls. Every measurement in the app is compared against these.

Negative controls (null models) destroy one kind of structure while keeping
everything else fixed. If a pattern survives in a null model, the pattern is
explained by whatever the null model kept, not by the order of the signs.

    shuffle_within_texts   keeps each text's signs and length, destroys order
    shuffle_global         keeps sign frequencies and text lengths, destroys
                           which signs share a text and their order
    uniform_random         keeps text lengths and the alphabet, destroys
                           everything else (the maximum-entropy reference)

Positive controls check that a method can find structure that is known to be
there. `plant_bigram` hides a known pattern in shuffled data, and
`markov_language` generates a synthetic sequence corpus whose grammar is
known exactly. A method that fails a positive control cannot be trusted on
the real corpus.
"""

from __future__ import annotations

from collections import Counter

import numpy as np

Seqs = list[list[str]]


def rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def shuffle_within_texts(seqs: Seqs, r: np.random.Generator) -> Seqs:
    out = []
    for s in seqs:
        idx = r.permutation(len(s))
        out.append([s[i] for i in idx])
    return out


def shuffle_global(seqs: Seqs, r: np.random.Generator) -> Seqs:
    pool = [x for s in seqs for x in s]
    pool = [pool[i] for i in r.permutation(len(pool))]
    out, k = [], 0
    for s in seqs:
        out.append(pool[k:k + len(s)])
        k += len(s)
    return out


def uniform_random(seqs: Seqs, r: np.random.Generator) -> Seqs:
    alphabet = sorted({x for s in seqs for x in s})
    return [list(r.choice(alphabet, size=len(s))) for s in seqs]


NULL_MODELS = {
    "Shuffle within texts": shuffle_within_texts,
    "Shuffle across corpus": shuffle_global,
    "Uniform random signs": uniform_random,
}


def plant_bigram(seqs: Seqs, a: str, b: str, rate: float, r: np.random.Generator) -> Seqs:
    """Positive control: in a fraction `rate` of texts with 2+ signs, overwrite
    one random adjacent pair with (a, b). Used to check that a test detects a
    pattern of a given strength."""
    out = []
    for s in seqs:
        s = list(s)
        if len(s) >= 2 and r.random() < rate:
            i = int(r.integers(0, len(s) - 1))
            s[i], s[i + 1] = a, b
        out.append(s)
    return out


def markov_language(n_texts: int, lengths: list[int], alphabet_size: int,
                    r: np.random.Generator, concentration: float = 0.05) -> Seqs:
    """Positive control: sequences from a random first-order Markov chain with
    sparse (Dirichlet) transitions and Zipf-like sign use. Its sequential
    structure is real and known, so methods should detect it."""
    alphabet = [f"X{i}" for i in range(alphabet_size)]
    zipf = 1 / np.arange(1, alphabet_size + 1)
    start = zipf / zipf.sum()
    trans = np.vstack([r.dirichlet(np.full(alphabet_size, concentration) + start)
                       for _ in range(alphabet_size)])
    out = []
    for k in range(n_texts):
        L = lengths[k % len(lengths)]
        cur = int(r.choice(alphabet_size, p=start))
        seq = [alphabet[cur]]
        for _ in range(L - 1):
            cur = int(r.choice(alphabet_size, p=trans[cur]))
            seq.append(alphabet[cur])
        out.append(seq)
    return out


def tokenize_text(text: str, unit: str = "char") -> Seqs:
    """Turn an uploaded comparison text into sequences, one per line.

    unit='char' compares signs to characters; unit='word' to words. Lines play
    the role of inscriptions, so blocks never cross line ends."""
    seqs = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        seq = list(line.replace(" ", "")) if unit == "char" else line.split()
        if seq:
            seqs.append(seq)
    return seqs


def match_lengths(seqs: Seqs, target_lengths: list[int], r: np.random.Generator) -> Seqs:
    """Cut a comparison corpus into pieces with the same length distribution as
    the Indus corpus, so differences are not just about text length."""
    stream = [x for s in seqs for x in s]
    out, k = [], 0
    for L in target_lengths:
        if k + L > len(stream):
            k = 0
        if L > len(stream):
            break
        out.append(stream[k:k + L])
        k += L
    return out


def frequency_matched_signs(seqs: Seqs, sign: str, k: int, r: np.random.Generator,
                            exclude: set[str] | None = None, tolerance: float = 0.5) -> list[str]:
    """Pick k random signs whose frequency is within ±tolerance (relative) of
    `sign`'s frequency. Used to build fair comparison sets."""
    freq = Counter(x for s in seqs for x in s)
    f = freq.get(sign, 0)
    exclude = (exclude or set()) | {sign}
    lo, hi = f * (1 - tolerance), f * (1 + tolerance)
    pool = [x for x, c in freq.items() if lo <= c <= hi and x not in exclude]
    if len(pool) < k:
        pool = sorted((x for x in freq if x not in exclude), key=lambda x: abs(freq[x] - f))[:max(k * 3, k)]
    if not pool:
        return []
    return list(r.choice(pool, size=min(k, len(pool)), replace=False))
