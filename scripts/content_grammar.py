"""Is there grammar (endings) inside the content slot? (EXPLORATORY; exploration split only.)

The content slot is what remains of a text after removing openers and closers
(roles from the rule in results/functional_by_site.md D.1). Two kinds of system
predict different fingerprints for its last (or first) sign:

  - a LIST OF NAMES or fixed labels: the last sign is mostly fixed by what comes
    before it (each name is one fixed string), and many different signs end units;
  - a LANGUAGE WITH ENDINGS (suffixes): a small closed set of signs ends most units,
    and the same stem turns up with different endings (cat / cats / cat's).

Measured for real content and for two synthetic systems built to the same size
and length profile, plus the real content with signs shuffled within each unit.
Never reads the holdout.

    python scripts/content_grammar.py
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from functional_skeleton import RULE, assign, load  # noqa: E402
from functional_slots import NUMERALS  # noqa: E402

RNG = np.random.default_rng(2026)
OUT = {}


def H(c: Counter) -> float:
    p = np.array(list(c.values()), float)
    p /= p.sum()
    return float(-(p * np.log2(p)).sum())


def fingerprint(units, edge="end", min_stem=3):
    """edge='end': ending = last sign, stem = the rest. edge='start': prefix = first sign."""
    us = [u for u in units if len(u) >= 2]
    if edge == "end":
        pairs = [(tuple(u[:-1]), u[-1]) for u in us]
    else:
        pairs = [(tuple(u[1:]), u[0]) for u in us]
    ends = Counter(e for _, e in pairs)
    by_stem = defaultdict(Counter)
    for s, e in pairs:
        by_stem[s][e] += 1
    rec = {s: c for s, c in by_stem.items() if sum(c.values()) >= min_stem}
    # H(edge | stem), averaged over recurring stems, weighted by use; compared with H(edge) over the same tokens
    tot = sum(sum(c.values()) for c in rec.values())
    h_cond = sum(sum(c.values()) / tot * H(c) for c in rec.values()) if tot else float("nan")
    pooled = Counter()
    for c in rec.values():
        pooled.update(c)
    h_marg = H(pooled) if pooled else float("nan")
    top5 = sum(v for _, v in ends.most_common(5)) / len(pairs)
    # productivity of the top-5 edge signs: distinct stems each attaches to, per use
    prod = np.mean([len({s for s, e in pairs if e == x}) / ends[x] for x, _ in ends.most_common(5)])
    alternating = sum(1 for c in rec.values() if len(c) >= 2) / len(rec) if rec else float("nan")
    return dict(units=len(pairs), distinct_edge_signs=len(ends), top5_share=top5,
                H_edge=H(ends), recurring_stems=len(rec), stem_tokens=tot,
                H_edge_given_stem=h_cond, H_edge_same_tokens=h_marg,
                freedom=(h_cond / h_marg) if h_marg else float("nan"),
                stems_with_2plus_edges=alternating, top5_productivity=float(prod))


def content_units(df, roles, drop_numerals=False):
    out = []
    for s in df["signs"]:
        u = [x for x in s if roles.get(x) not in (0, 2)]
        if drop_numerals:
            u = [x for x in u if x not in NUMERALS]
        if u:
            out.append(u)
    return out


def synth_names(units, rng):
    """Fixed names: a Zipfian inventory of whole sign strings, drawn as wholes."""
    alphabet = sorted({x for u in units for x in u})
    lengths = [len(u) for u in units]
    n_names = len({tuple(u) for u in units})
    names = []
    for _ in range(n_names):
        L = int(rng.choice(lengths))
        names.append([alphabet[int(i)] for i in rng.integers(len(alphabet), size=L)])
    w = 1 / np.arange(1, n_names + 1)
    w /= w.sum()
    return [names[int(i)] for i in rng.choice(n_names, size=len(units), p=w)]


def synth_suffixing(units, rng, n_endings=6):
    """A language with endings: stems from the same alphabet + one of a few endings."""
    alphabet = sorted({x for u in units for x in u})
    endings = [alphabet[int(i)] for i in rng.choice(len(alphabet), size=n_endings, replace=False)]
    ew = 1 / np.arange(1, n_endings + 1)
    ew /= ew.sum()
    n_stems = max(50, len({tuple(u[:-1]) for u in units if len(u) >= 2}) // 2)
    stems = []
    for _ in range(n_stems):
        L = int(rng.choice([len(u) - 1 for u in units if len(u) >= 2]))
        stems.append([alphabet[int(i)] for i in rng.integers(len(alphabet), size=max(1, L))])
    sw = 1 / np.arange(1, n_stems + 1)
    sw /= sw.sum()
    out = []
    for u in units:
        if len(u) == 1:
            out.append([alphabet[int(rng.integers(len(alphabet)))]])
            continue
        st = stems[int(rng.choice(n_stems, p=sw))]
        out.append(list(st) + [endings[int(rng.choice(n_endings, p=ew))]])
    return out


def shuffle_units(units, rng):
    return [list(rng.permutation(u)) for u in units]


def table(name, rows):
    print(f"\n== {name} ==")
    hdr = (f"   {'system':30} {'units':>5} {'edge signs':>10} {'top-5 share':>11} {'H(edge)':>7} "
           f"{'freedom':>7} {'stems w/ 2+':>11} {'stems':>5}")
    print(hdr)
    for k, r in rows.items():
        print(f"   {k:30} {r['units']:5d} {r['distinct_edge_signs']:10d} {r['top5_share']:11.0%} "
              f"{r['H_edge']:7.2f} {r['freedom']:7.2f} {r['stems_with_2plus_edges']:11.0%} {r['recurring_stems']:5d}")


def main():
    df = load(dedupe=True)
    roles, _ = assign(list(df["signs"]), RULE)
    print(f"Exploration split, duplicates removed: {len(df)} texts. Content = signs other than openers/closers.")
    print("freedom = H(edge sign | rest of unit) / H(edge sign), over stems used 3+ times: "
          "near 0 = the edge is fixed by the stem (names); near 1 = any stem takes any edge (productive endings).")

    for variant, drop in (("with numerals", False), ("numerals removed", True)):
        units = content_units(df, roles, drop)
        lens = Counter(min(len(u), 6) for u in units)
        print(f"\n[{variant}] {len(units)} content units; lengths {dict(sorted(lens.items()))} (6 = 6+)")
        OUT[variant] = {}
        for edge in ("end", "start"):
            rows = {
                "REAL content": fingerprint(units, edge),
                "real, shuffled within unit": np.mean([0]),  # placeholder replaced below
                "synthetic: list of names": None,
                "synthetic: language w/ endings": None,
            }
            sh = [fingerprint(shuffle_units(units, RNG), edge) for _ in range(20)]
            rows["real, shuffled within unit"] = {k: float(np.nanmean([s[k] for s in sh])) for k in sh[0]}
            for k in ("units", "distinct_edge_signs", "recurring_stems"):
                rows["real, shuffled within unit"][k] = int(round(rows["real, shuffled within unit"][k]))
            nm = [fingerprint(synth_names(units, RNG), edge) for _ in range(20)]
            sf = [fingerprint(synth_suffixing(units, RNG), edge) for _ in range(20)]
            for key, runs in (("synthetic: list of names", nm), ("synthetic: language w/ endings", sf)):
                rows[key] = {k: float(np.nanmean([s[k] for s in runs])) for k in runs[0]}
                for k in ("units", "distinct_edge_signs", "recurring_stems"):
                    rows[key][k] = int(round(rows[key][k]))
            table(f"{variant}: {'last' if edge == 'end' else 'first'} sign of the content", rows)
            OUT[variant][edge] = rows

        # Which signs end content units most, and how many different stems they attach to
        us = [u for u in units if len(u) >= 2]
        ends = Counter(u[-1] for u in us)
        print(f"   commonest content-final signs ({variant}):")
        lst = []
        for x, n in ends.most_common(8):
            stems = {tuple(u[:-1]) for u in us if u[-1] == x}
            elsewhere = sum(1 for u in us if x in u[:-1])
            lst.append(dict(sign=x, ends=n, distinct_stems=len(stems), used_inside=elsewhere))
            print(f"     {x:6} ends {n:3} units after {len(stems):3} different stems; also used inside units {elsewhere} times")
        OUT[variant]["top_final_signs"] = lst

    Path(__file__).resolve().parents[1].joinpath("results", "content_grammar.json").write_text(
        json.dumps(OUT, indent=1, default=float))


if __name__ == "__main__":
    main()
