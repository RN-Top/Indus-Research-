"""Structural comparison battery (P20 framework).

Reads data/structure/languages.csv. Runs only rows with licence_status == 'checked'
and an existing corpus file. Compares structural features only; no sign values.

Usage: python scripts/structure_battery.py [--out results/structure_battery.md]
"""
import argparse
import csv
import hashlib
import math
import os
import random
from collections import Counter
from datetime import date

REG = "data/structure/languages.csv"
MIN_LEN, MAX_LEN = 3, 8
N_SHUFFLE = 1000
SEED = 20261107


def load_registry(path=REG):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_corpus(path):
    texts = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            units = row["units"].split()
            if MIN_LEN <= len(units) <= MAX_LEN:
                texts.append(units)
    return texts


def features(texts):
    """F1 first unit repeats; F2 last unit repeats; F3 mean unigram entropy;
    F4 share of units also found in another text."""
    if not texts:
        return [float("nan")] * 4
    f1 = f2 = 0
    ent = []
    vocab_texts = Counter()
    for t in texts:
        if t[0] in t[1:]:
            f1 += 1
        if t[-1] in t[:-1]:
            f2 += 1
        c = Counter(t)
        n = len(t)
        ent.append(-sum((k / n) * math.log2(k / n) for k in c.values()))
        for u in set(t):
            vocab_texts[u] += 1
    n = len(texts)
    shared_units = sum(1 for u, k in vocab_texts.items() if k > 1)
    f4 = shared_units / len(vocab_texts) if vocab_texts else float("nan")
    return [f1 / n, f2 / n, sum(ent) / n, f4]


def distance(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))


def shuffle_texts(texts, rng):
    out = []
    for t in texts:
        s = t[:]
        rng.shuffle(s)
        out.append(s)
    return out


def bh(pvals):
    """Benjamini-Hochberg adjusted p-values, in input order."""
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    adj = [0.0] * m
    prev = 1.0
    for rank, i in reversed(list(enumerate(order, 1))):
        val = min(prev, pvals[i] * m / rank)
        adj[i] = val
        prev = val
    return adj


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/structure_battery.md")
    args = ap.parse_args()

    reg_bytes = open(REG, "rb").read()
    reg_hash = hashlib.sha256(reg_bytes).hexdigest()
    rows = load_registry()

    target = next((r for r in rows if r["role"] == "target"), None)
    runnable, skipped = [], []
    for r in rows:
        if r["role"] == "target":
            continue
        ok = r["licence_status"] == "checked" and os.path.exists(r["corpus_path"])
        (runnable if ok else skipped).append(r)

    lines = [f"# Structural battery run {date.today().isoformat()}",
             "",
             f"Registry sha256: `{reg_hash}`",
             f"Seed: {SEED}; shuffles per language: {N_SHUFFLE}; texts of {MIN_LEN}-{MAX_LEN} units.",
             ""]

    tgt_ok = (target is not None and target["licence_status"] == "checked"
              and os.path.exists(target["corpus_path"]))
    if not tgt_ok:
        lines.append("**Not run:** the target (Indus) corpus is not checked or not present. "
                     "No comparison was computed.")
        skipped_names = ", ".join(r["language"] for r in skipped) or "none"
        lines += ["", f"Skipped: {skipped_names}"]
        write(args.out, lines)
        print("\n".join(lines))
        return

    rng = random.Random(SEED)
    indus = load_corpus(target["corpus_path"])
    f_indus = features(indus)
    results = []
    for r in runnable:
        texts = load_corpus(r["corpus_path"])
        f_lang = features(texts)
        d_obs = distance(f_indus, f_lang)
        null = []
        for _ in range(N_SHUFFLE):
            d_null = distance(features(shuffle_texts(indus, rng)), f_lang)
            null.append(d_null)
        p = (1 + sum(1 for d in null if d <= d_obs)) / (N_SHUFFLE + 1)
        results.append((r, f_lang, d_obs, p))

    adj = bh([p for _, _, _, p in results]) if results else []

    lines += ["## Indus features", "", "F1 first repeat | F2 last repeat | F3 entropy | F4 shared units",
              "| " + " | ".join(f"{x:.3f}" for x in f_indus) + " |", ""]
    lines += ["## Per language", "",
              "| language | role | F1 | F2 | F3 | F4 | distance | p (shuffled Indus) | BH q |",
              "|---|---|---|---|---|---|---|---|---|"]
    for (r, fl, d, p), q in zip(results, adj):
        lines.append(f"| {r['language']} | {r['role']} | " + " | ".join(f"{x:.3f}" for x in fl)
                     + f" | {d:.3f} | {p:.4f} | {q:.4f} |")
    lines += ["", "Closeness rule (P20): Indus is closer to both Aramaic and Hebrew than to the "
              "control on at least 3 of 4 features, read from the per-feature values above.",
              "", "Skipped (not checked or no corpus): "
              + (", ".join(r["language"] for r in skipped) or "none")]
    write(args.out, lines)
    print("\n".join(lines))


def write(path, lines):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
