"""Falsifiable hypotheses: definition, registration, testing, correction.

Workflow (see METHODS.md for the full protocol):

1. Explore freely on the exploration split (80% of texts).
2. Write a hypothesis as a precise, machine-testable claim with a predicted
   direction. `freeze()` adds a timestamp and a SHA-256 fingerprint of the
   claim.
3. Commit the JSON file to `hypotheses/` in the public repository. The git
   commit (and GitHub's record of it) is the public proof that the claim
   existed before the confirmatory test.
4. Run the confirmatory test on the locked holdout (20% of texts), once.
   All registered hypotheses are corrected together for multiple testing
   (Benjamini-Hochberg).

Every test is a permutation test against an explicit null model, and every
result reports the observed statistic, the null distribution's mean, the
effect ratio, the p-value and the number of permutations.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from . import controls

KINDS = {
    "precedes": "Sign A is immediately followed by sign B more often than chance.",
    "position": "Sign A appears at a given position (start or end of a text) more often than chance.",
    "association": "Texts containing sign A have a given value of a context field (site, object type, motif) more often than chance.",
    "class_cohesion": "A set of signs shares following-sign contexts more than random sets of equally frequent signs.",
    "class_association": "Texts containing any sign of a set have a given value of a context field more often than chance.",
    "class_contrast": "Two sets of signs are followed by different signs (their successor distributions differ more than chance).",
    "unit_position": "Multi-sign units (kept whole) sit at a given position (start or end of a text) more often than chance.",
    "unit_recurrence": "A list of multi-sign units learned elsewhere recurs in these texts more than in the same texts with their signs shuffled.",
    "group_contrast": "Texts in one group (e.g. unicorn seals) use a different mix of signs from the other texts, more than chance.",
    "pair_specificity": "Each sign that follows a member of a set (e.g. numerals) tends to take its own particular member: the pairing carries more information than chance (fixed phrases rather than free combination).",
}

REQUIRED_PARAMS = {
    "precedes": ["a", "b"],
    "position": ["a", "where"],
    "association": ["a", "field", "value"],
    "class_cohesion": ["signs"],
    "class_association": ["signs", "field", "value"],
    "class_contrast": ["signs", "other"],
    "pair_specificity": ["signs"],
    "unit_position": ["units", "where"],
    "unit_recurrence": ["units"],
    "group_contrast": ["field", "value"],
}

FINGERPRINT_FIELDS = ["kind", "params", "statement", "prediction", "alpha", "source_key", "n_perm", "seed",
                      "data_settings"]


@dataclass
class TestResult:
    observed: float
    null_mean: float
    p_value: float
    n_perm: int
    n_support: int  # how many occurrences the result rests on
    note: str = ""

    @property
    def effect_ratio(self) -> float:
        return self.observed / self.null_mean if self.null_mean else float("inf")


# --------------------------------------------------------------------------
# Hypothesis records
# --------------------------------------------------------------------------

def new_hypothesis(kind: str, params: dict, statement: str, *, author: str = "",
                   source_key: str = "indus_website", alpha: float = 0.05,
                   n_perm: int = 2000, seed: int = 12345, data_settings: dict | None = None) -> dict:
    if kind not in KINDS:
        raise ValueError(f"unknown kind {kind!r}")
    missing = [p for p in REQUIRED_PARAMS[kind] if p not in params]
    if missing:
        raise ValueError(f"missing parameters for {kind}: {missing}")
    return {
        "kind": kind, "params": params, "statement": statement.strip(),
        "prediction": "greater",
        "alpha": alpha, "source_key": source_key, "n_perm": n_perm, "seed": seed,
        "author": author,
        # Cleaning choices the confirmatory test must reuse (part of the fingerprint).
        "data_settings": data_settings or {"drop_damaged": True, "dedupe": False, "drop_unidentified": True},
    }


def fingerprint(h: dict) -> str:
    core = {k: h.get(k) for k in FINGERPRINT_FIELDS}
    blob = json.dumps(core, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


def freeze(h: dict) -> dict:
    h = dict(h)
    h["frozen_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    h["sha256"] = fingerprint(h)
    h["id"] = f"H-{h['frozen_utc'][:10]}-{h['sha256'][:8]}"
    return h


def verify(h: dict) -> bool:
    """True if the record has not been edited since it was frozen."""
    return "sha256" in h and fingerprint(h) == h["sha256"]


# --------------------------------------------------------------------------
# Test statistics
# --------------------------------------------------------------------------

def stat_precedes(seqs, a, b) -> float:
    return float(sum(1 for s in seqs for x, y in zip(s, s[1:]) if x == a and y == b))


def stat_position(seqs, a, where) -> float:
    """Share of A's tokens (in texts of 2+ signs) that sit at `where`.

    `a` may be one sign or a list of signs (a class). `where` is "start",
    "end", or "not_end" (anywhere but the last position)."""
    members = {a} if isinstance(a, str) else set(a)
    hit = tot = 0
    for s in seqs:
        if len(s) < 2:
            continue
        last = len(s) - 1
        for i, x in enumerate(s):
            if x in members:
                tot += 1
                if ((where == "start" and i == 0) or (where == "end" and i == last)
                        or (where == "not_end" and i != last)):
                    hit += 1
    return hit / tot if tot else float("nan")


def _successor_vectors(seqs):
    after: dict[str, Counter] = {}
    for s in seqs:
        for x, y in zip(s, s[1:] + ["</s>"]):
            after.setdefault(x, Counter())[y] += 1
    return after


def _restrict(df: pd.DataFrame, within):
    """Keep only texts matching one condition or a list of them, e.g.
    [{"field": "object_type", "value": "seal"}, {"field": "site", "value": "Mohenjo-daro"}]."""
    if not within:
        return df, list(df["signs"])
    conds = within if isinstance(within, list) else [within]
    keep = np.ones(len(df), dtype=bool)
    for c in conds:
        keep &= (df[c["field"]].astype(str) == str(c["value"])).to_numpy()
    df = df[keep]
    return df, list(df["signs"])


def _jsd(c1: Counter, c2: Counter) -> float:
    """Jensen-Shannon divergence (bits) between two count distributions."""
    keys = sorted(set(c1) | set(c2))
    p = np.array([c1.get(k, 0) for k in keys], float)
    q = np.array([c2.get(k, 0) for k in keys], float)
    if p.sum() == 0 or q.sum() == 0:
        return float("nan")
    p, q = p / p.sum(), q / q.sum()
    m = (p + q) / 2

    def kl(x, y):
        nz = x > 0
        return float(np.sum(x[nz] * np.log2(x[nz] / y[nz])))
    return (kl(p, m) + kl(q, m)) / 2


def _successor_tokens(seqs, members: set) -> list[tuple[str, str]]:
    """(sign, following sign) for every token of a member sign."""
    out = []
    for s in seqs:
        nxt = list(s[1:]) + ["</s>"]
        out += [(x, y) for x, y in zip(s, nxt) if x in members]
    return out


def merge_units(seqs, units: list[list[str]]) -> list[list[str]]:
    """Replace each occurrence of a unit with one token 'A+B+C' (longest first),
    so a shuffle moves the unit as a whole."""
    ordered = sorted((tuple(u) for u in units), key=len, reverse=True)
    out = []
    for s in seqs:
        s, merged, i = list(s), [], 0
        while i < len(s):
            for u in ordered:
                if tuple(s[i:i + len(u)]) == u:
                    merged.append("+".join(u))
                    i += len(u)
                    break
            else:
                merged.append(s[i])
                i += 1
        out.append(merged)
    return out


def count_units(seqs, units: list[list[str]]) -> int:
    ts = [tuple(u) for u in units]
    return sum(1 for s in seqs for u in ts for i in range(len(s) - len(u) + 1) if tuple(s[i:i + len(u)]) == u)


def _mutual_information(pairs: list[tuple[str, str]]) -> float:
    """Mutual information (bits) between the two halves of a list of pairs."""
    n = len(pairs)
    if n == 0:
        return float("nan")
    joint = Counter(pairs)
    left = Counter(a for a, _ in pairs)
    right = Counter(b for _, b in pairs)
    return float(sum(c / n * np.log2((c * n) / (left[a] * right[b])) for (a, b), c in joint.items()))


def _cosine(c1: Counter, c2: Counter) -> float:
    keys = set(c1) | set(c2)
    v1 = np.array([c1.get(k, 0) for k in keys], float)
    v2 = np.array([c2.get(k, 0) for k in keys], float)
    d = np.linalg.norm(v1) * np.linalg.norm(v2)
    return float(v1 @ v2 / d) if d else 0.0


def stat_cohesion(after: dict, signs: list[str]) -> float:
    present = [s for s in signs if s in after]
    if len(present) < 2:
        return float("nan")
    sims = [_cosine(after[x], after[y]) for i, x in enumerate(present) for y in present[i + 1:]]
    return float(np.mean(sims))


# --------------------------------------------------------------------------
# Permutation tests
# --------------------------------------------------------------------------

def _p_greater(obs, null):
    null = np.asarray(null, float)
    null = null[~np.isnan(null)]
    return float((1 + np.sum(null >= obs)) / (len(null) + 1)), float(null.mean()) if len(null) else float("nan")


def run_test(h: dict, df: pd.DataFrame, n_perm: int | None = None, seed: int | None = None) -> TestResult:
    """Run one hypothesis on a corpus dataframe (columns: signs + context)."""
    kind, p = h["kind"], h["params"]
    n_perm = n_perm or h.get("n_perm", 2000)
    r = controls.rng(h.get("seed", 12345) if seed is None else seed)
    seqs = list(df["signs"])

    if kind == "precedes":
        obs = stat_precedes(seqs, p["a"], p["b"])
        null = [stat_precedes(controls.shuffle_within_texts(seqs, r), p["a"], p["b"]) for _ in range(n_perm)]
        support = int(obs)
        note = "Null: signs shuffled within each text (keeps each text's signs, destroys order)."
    elif kind == "position":
        obs = stat_position(seqs, p["a"], p["where"])
        null = [stat_position(controls.shuffle_within_texts(seqs, r), p["a"], p["where"]) for _ in range(n_perm)]
        members = {p["a"]} if isinstance(p["a"], str) else set(p["a"])
        support = sum(1 for s in seqs if len(s) >= 2 for x in s if x in members)
        note = "Null: signs shuffled within each text."
    elif kind == "association":
        has = np.array([p["a"] in s for s in seqs])
        lab = (df[p["field"]].astype(str) == str(p["value"])).to_numpy()
        obs = float(lab[has].mean()) if has.any() else float("nan")
        null = []
        for _ in range(n_perm):
            perm = lab[r.permutation(len(lab))]
            null.append(float(perm[has].mean()) if has.any() else float("nan"))
        support = int(has.sum())
        note = f"Null: '{p['field']}' labels permuted across texts (keeps label totals)."
    elif kind == "class_association":
        df, seqs = _restrict(df, p.get("within"))
        members = set(p["signs"])
        has = np.array([any(x in members for x in s) for s in seqs])
        lab = (df[p["field"]].astype(str) == str(p["value"])).to_numpy()
        obs = float(lab[has].mean()) if has.any() else float("nan")
        null = [float(lab[r.permutation(len(lab))][has].mean()) if has.any() else float("nan")
                for _ in range(n_perm)]
        support = int(has.sum())
        note = f"Null: '{p['field']}' labels permuted across texts (keeps label totals)."
    elif kind == "class_contrast":
        a_set, b_set = set(p["signs"]), set(p["other"])
        toks = _successor_tokens(seqs, a_set | b_set)
        labels = np.array([x in a_set for x, _ in toks])
        nxt = [y for _, y in toks]

        def jsd_for(lbl):
            return _jsd(Counter(y for y, l in zip(nxt, lbl) if l), Counter(y for y, l in zip(nxt, lbl) if not l))
        obs = jsd_for(labels)
        null = [jsd_for(labels[r.permutation(len(labels))]) for _ in range(n_perm)]
        support = int(min(labels.sum(), (~labels).sum())) if len(labels) else 0
        note = "Null: class labels permuted among the two sets' tokens (keeps each set's size)."
    elif kind == "unit_position":
        merged = merge_units(seqs, p["units"])
        tokens = ["+".join(u) for u in p["units"]]
        obs = stat_position(merged, tokens, p["where"])
        null = [stat_position(controls.shuffle_within_texts(merged, r), tokens, p["where"]) for _ in range(n_perm)]
        support = sum(1 for s in merged if len(s) >= 2 for x in s if x in set(tokens))
        note = "Null: each unit kept whole and shuffled with the other signs of its text."
    elif kind == "unit_recurrence":
        obs = float(count_units(seqs, p["units"]))
        null = [float(count_units(controls.shuffle_within_texts(seqs, r), p["units"])) for _ in range(n_perm)]
        support = int(obs)
        note = "Null: signs shuffled within each text (keeps every text's signs, destroys order)."
    elif kind == "group_contrast":
        df, seqs = _restrict(df, p.get("within"))
        lab = (df[p["field"]].astype(str) == str(p["value"])).to_numpy()
        if p.get("versus"):  # compare against one other value instead of all the rest
            other = (df[p["field"]].astype(str) == str(p["versus"])).to_numpy()
            keep = lab | other
            seqs = [q for q, k in zip(seqs, keep) if k]
            lab = lab[keep]

        def contrast(labels):
            a, b = Counter(), Counter()
            for q, l in zip(seqs, labels):
                (a if l else b).update(q)
            return _jsd(a, b)
        obs = contrast(lab)
        null = [contrast(lab[r.permutation(len(lab))]) for _ in range(n_perm)]
        support = int(min(lab.sum(), (~lab).sum()))
        note = ("Null: group labels permuted across texts (keeps group sizes). Statistic: Jensen-Shannon "
                "divergence between the two groups' sign frequencies.")
    elif kind == "pair_specificity":
        members = set(p["signs"])
        pairs = [(a, b) for s in seqs for a, b in zip(s, s[1:]) if a in members and b not in members]
        left = np.array([a for a, _ in pairs], dtype=object)
        right = [b for _, b in pairs]
        obs = _mutual_information(pairs)
        null = [_mutual_information(list(zip(left[r.permutation(len(left))], right))) for _ in range(n_perm)]
        support = len(pairs)
        note = ("Null: the set members (e.g. which numeral) permuted among the pairs, keeping how often each "
                "member and each following sign occur. Small samples inflate mutual information; the null "
                "has the same inflation, so only the excess counts.")
    elif kind == "class_cohesion":
        signs = list(p["signs"])
        after = _successor_vectors(seqs)
        obs = stat_cohesion(after, signs)
        null = []
        for _ in range(n_perm):
            rand = []
            used = set(signs)
            for s in signs:
                m = controls.frequency_matched_signs(seqs, s, 1, r, exclude=used)
                if m:
                    rand.append(m[0])
                    used.add(m[0])
            null.append(stat_cohesion(after, rand))
        support = sum(1 for s in seqs for x in s if x in set(signs))
        note = "Null: random sets of signs with matched frequencies."
    else:
        raise ValueError(kind)

    if obs != obs:  # NaN: the sign never occurs in this split
        return TestResult(obs, float("nan"), float("nan"), n_perm, 0, "No occurrences in this data; cannot test.")
    pval, null_mean = _p_greater(obs, null)
    return TestResult(obs, null_mean, pval, n_perm, support, note)


def benjamini_hochberg(pvals: list[float]) -> list[float]:
    """Adjusted p-values (q-values) controlling the false discovery rate."""
    p = np.asarray(pvals, float)
    n = len(p)
    if n == 0:
        return []
    order = np.argsort(p)
    ranked = p[order] * n / (np.arange(n) + 1)
    q = np.minimum.accumulate(ranked[::-1])[::-1]
    out = np.empty(n)
    out[order] = np.minimum(q, 1.0)
    return out.tolist()


MIN_SUPPORT = 5


def verdict(q: float, alpha: float, support: int) -> str:
    if support < MIN_SUPPORT or q != q:
        return "Inconclusive (too few occurrences)"
    return "Supported" if q < alpha else "Not supported"


def sensitivity_check(h: dict, df: pd.DataFrame, rate: float = 0.05, trials: int = 20,
                      n_perm: int = 200, seed: int = 7) -> float | None:
    """Positive control for 'precedes' hypotheses: plant the A->B pattern at
    `rate` into shuffled data and report how often the test detects it at
    p < alpha. Low power means a 'Not supported' verdict says little."""
    if h["kind"] != "precedes":
        return None
    r = controls.rng(seed)
    seqs = list(df["signs"])
    hits = 0
    for _ in range(trials):
        planted = controls.plant_bigram(controls.shuffle_within_texts(seqs, r),
                                        h["params"]["a"], h["params"]["b"], rate, r)
        res = run_test(h, pd.DataFrame({"signs": planted}), n_perm=n_perm, seed=int(r.integers(1e9)))
        hits += res.p_value < h.get("alpha", 0.05)
    return hits / trials
