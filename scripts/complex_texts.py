"""The frame-breaking 'complex' texts (Fuls's ~13%). (EXPLORATION ONLY: description, no tests.)

Complex text: 3+ signs, and every adjacent sign pair occurs at most twice in the
exploration corpus. Compared with ordinary texts of 3+ signs, and with ordinary
texts matched for length. Order is looked at with context-derived sign classes
(scripts/open_patterns.py): a class-bigram model is fitted on half of the
ordinary texts and scores the complex texts against the other half. Exploration
split only; nothing tested or registered.

    python scripts/complex_texts.py
"""

import contextlib
import io
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from functional_skeleton import assign  # noqa: E402
from functional_slots import NUMERALS, load  # noqa: E402
import open_patterns as op  # noqa: E402

RNG = np.random.default_rng(20261016)


def share(x):
    return f"{x:.0%}"


def main():
    df = load()
    df = df[df["signs"].map(len) > 0].reset_index(drop=True)
    seqs = [list(s) for s in df["signs"]]
    roles, _ = assign(seqs)
    bg = Counter((a, b) for s in seqs for a, b in zip(s, s[1:]))
    tok = Counter(x for s in seqs for x in s)
    long_ = np.array([len(s) >= 3 for s in seqs])
    cx = np.array([len(s) >= 3 and all(bg[(a, b)] <= 2 for a, b in zip(s, s[1:])) for s in seqs])
    ordi = long_ & ~cx
    out = {"complex": int(cx.sum()), "ordinary": int(ordi.sum())}
    print(f"Texts of 3+ signs: {long_.sum()}; complex: {cx.sum()} ({cx.sum() / long_.sum():.0%}); ordinary: {ordi.sum()}")

    # length-matched ordinary sample (by exact length, with replacement where needed)
    by_len = {}
    for i in np.flatnonzero(ordi):
        by_len.setdefault(len(seqs[i]), []).append(i)
    matched = []
    for i in np.flatnonzero(cx):
        L = len(seqs[i])
        pool = by_len.get(L) or by_len[min(by_len, key=lambda k: abs(k - L))]
        matched.append(int(RNG.choice(pool)))
    matched = np.array(matched)
    groups = {"complex": np.flatnonzero(cx), "ordinary (all 3+)": np.flatnonzero(ordi), "ordinary, length-matched": matched}

    # 1. who they are
    print("\n== 1. Length, object type, site ==")
    rows = {}
    for g, ix in groups.items():
        sub = df.iloc[ix]
        L = [len(seqs[i]) for i in ix]
        rows[g] = dict(n=len(ix), median_len=float(np.median(L)), mean_len=float(np.mean(L)),
                       objects=sub["object_type"].value_counts(normalize=True).round(3).head(5).to_dict(),
                       sites=sub["site"].value_counts(normalize=True).round(3).head(6).to_dict(),
                       damaged_flag=float(sub["damaged"].astype(str).isin(["True", "1", "true"]).mean()) if "damaged" in sub else None)
        print(f"   {g:26} n {len(ix):4}  length median {np.median(L):.0f} mean {np.mean(L):.1f}")
        print(f"      objects {rows[g]['objects']}")
        print(f"      sites   {rows[g]['sites']}")
    out["who"] = rows

    # 2. the frame
    print("\n== 2. Do they have the normal frame? ==")
    frame = {}
    for g, ix in groups.items():
        st = np.mean([roles.get(seqs[i][0]) == 0 for i in ix])
        en = np.mean([roles.get(seqs[i][-1]) == 2 for i in ix])
        both = np.mean([roles.get(seqs[i][0]) == 0 and roles.get(seqs[i][-1]) == 2 for i in ix])
        anyrole = np.mean([any(roles.get(x) in (0, 2) for x in seqs[i]) for i in ix])
        num = np.mean([any(x in NUMERALS for x in seqs[i]) for i in ix])
        rep = np.mean([len(set(seqs[i])) < len(seqs[i]) for i in ix])
        rare = np.mean([np.mean([tok[x] <= 5 for x in seqs[i]]) for i in ix])
        medfreq = np.median([np.median([tok[x] for x in seqs[i]]) for i in ix])
        frame[g] = dict(starts_opener=st, ends_closer=en, both=both, any_role_sign=anyrole, has_numeral=num,
                        repeats_a_sign=rep, share_rare_signs=rare, median_sign_frequency=float(medfreq))
        print(f"   {g:26} starts with opener {share(st)}, ends with closer {share(en)}, both {share(both)}, "
              f"has a numeral {share(num)}, repeats a sign {share(rep)}, signs used <=5 times {share(rare)}, "
              f"median sign frequency {medfreq:.0f}")
    out["frame"] = frame

    # 3. their own signs
    ctok = Counter(x for i in groups["complex"] for x in seqs[i])
    otok = Counter(x for i in groups["ordinary (all 3+)"] for x in seqs[i])
    cn, on = sum(ctok.values()), sum(otok.values())
    over = [(x, ctok[x], otok[x], (ctok[x] / cn) / ((otok[x] + 0.5) / on)) for x in ctok if ctok[x] >= 5]
    over.sort(key=lambda t: -t[3])
    only = [(x, ctok[x], otok[x]) for x in ctok if ctok[x] >= 3 and ctok[x] >= 3 * otok[x]]
    only.sort(key=lambda t: -t[1])
    print("\n== 3. Signs over-represented in complex texts (used >= 5 times there) ==")
    print("   " + "; ".join(f"{x} {c} vs {o} (x{r:.1f})" for x, c, o, r in over[:15]))
    print("   nearly only in complex texts (>= 3 uses, at least 3 times as many as in all ordinary texts): "
          + ("; ".join(f"{x} {c} vs {o}" for x, c, o in only[:15]) or "none"))
    under = sorted([(x, ctok[x], otok[x], (ctok[x] / cn) / (otok[x] / on)) for x in otok if otok[x] >= 40], key=lambda t: t[3])
    print("   most under-represented common signs: " + "; ".join(f"{x} {c} vs {o} (x{r:.2f})" for x, c, o, r in under[:10]))
    out["over"] = over[:30]; out["nearly_only"] = only; out["under"] = under[:15]

    # 4. order at class level
    with contextlib.redirect_stdout(io.StringIO()):
        cls_of = op.part_a(seqs, roles, {})
    C = lambda x: cls_of.get(x, -1)  # noqa: E731  (-1 = rare sign outside the classes)
    oi = groups["ordinary (all 3+)"].copy()
    RNG.shuffle(oi)
    train, held = oi[: len(oi) // 2], oi[len(oi) // 2:]
    cb = Counter(); cu = Counter()
    for i in train:
        p = ["S"] + [C(x) for x in seqs[i]] + ["E"]
        for a, b in zip(p, p[1:]):
            cb[(a, b)] += 1; cu[a] += 1
    K = len(set(cls_of.values())) + 3

    def score(ix):
        lp = []
        for i in ix:
            p = ["S"] + [C(x) for x in seqs[i]] + ["E"]
            lp.append(np.mean([np.log2((cb[(a, b)] + 0.5) / (cu[a] + 0.5 * K)) for a, b in zip(p, p[1:])]))
        return float(np.mean(lp))
    unk = {g: float(np.mean([np.mean([C(x) == -1 for x in seqs[i]]) for i in ix])) for g, ix in groups.items()}
    matched_held = [i for i in matched if i not in set(train)]
    sc = {"complex": score(groups["complex"]), "ordinary, held-out half": score(held),
          "ordinary, length-matched (held-out only)": score(matched_held)}
    print("\n== 4. Order at the level of sign classes (class-bigram model fitted on half the ordinary texts) ==")
    for g, v in sc.items():
        print(f"   {g:42} mean log2-probability per class step {v:.2f}  (perplexity {2 ** -v:.1f})")
    print("   share of signs too rare to have a class: " + ", ".join(f"{g} {share(v)}" for g, v in unk.items()))
    ctpl = Counter("-".join(str(C(x)) for x in seqs[i]) for i in groups["complex"])
    print("   commonest class sequences among complex texts:", ctpl.most_common(6))
    out["class_order"] = dict(scores=sc, rare_share=unk, top_templates=ctpl.most_common(15))
    (ROOT / "results" / "complex_texts.json").write_text(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
