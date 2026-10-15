"""Function theory, first comparison: Proto-Elamite tablets. (EXPLORATORY.)

Does the same blind role rule used for the Indus script (results/functional_by_site.md
D.1) find an opener -> content -> closer layout in Proto-Elamite accounting
tablets, and do the "openers" it finds match where experts mark the tablet
header?

Data: Born et al. (2022) corpus, github.com/sfu-natlang/pe-headers (transliterations
from CDLI; reuse under CDLI terms with citation). Not redistributed here: pass the
path to its corpus/ folder.

A 20% Proto-Elamite holdout (hash of the P-number, salt 'pe-holdout-v1') is set
aside and never read here, for a later pre-registered test.

    python scripts/proto_elamite_skeleton.py /path/to/pe-headers/corpus
"""

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from functional_skeleton import RULE  # noqa: E402  (the same frozen rule as for Indus)

SALT = "pe-holdout-v1"
RNG = np.random.default_rng(7)
SIGN = re.compile(r"^\|?M\d{3}")


def split_of(pnum):
    h = int(hashlib.sha256(f"{SALT}:{pnum}".encode()).hexdigest(), 16)
    return "holdout" if h % 100 < 20 else "explore"


def norm(tok):
    """M157# -> M157 ; M302~t? -> M302 ; |M296+M296| -> M296+M296 (compound kept)."""
    t = tok.strip("[]#?!*")
    if t.startswith("|"):
        parts = re.findall(r"M\d{3}", t)
        return "+".join(parts) if parts else None
    m = re.match(r"M\d{3}", t)
    return m.group(0) if m else None


def parse(path):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    pnum = lines[0].split()[0].lstrip("&")
    toks, header_upto, line_damage = [], None, []
    sub_idx = set()
    last_line_tokens = []
    for ln in lines:
        s = ln.strip()
        if s.startswith("# header"):
            header_upto = len(toks)
            continue
        if s.startswith("#tr.en: (subscript)"):
            sub_idx |= set(last_line_tokens)
            continue
        if not re.match(r"^\d+[A-Za-z.']*\.?\s", s) and not re.match(r"^\d+\.", s):
            continue
        body = re.sub(r"^\S+\s", "", s)
        bad = "[" in body or "..." in body or bool(re.search(r"(^|\s)x(\s|$)", body))
        line_damage.append(bad)
        signs, _, nums = body.partition(",")
        last_line_tokens = []
        for t in signs.split():
            n = norm(t)
            if n:
                last_line_tokens.append(len(toks))
                toks.append(n)
        if re.search(r"\d\(N", nums):
            last_line_tokens.append(len(toks))
            toks.append("NUM")
    # Like Born et al., keep a tablet when its beginning and end are intact: only the
    # first and last text lines count as damage; broken signs elsewhere are dropped.
    damaged = bool(line_damage) and (line_damage[0] or line_damage[-1])
    return dict(pnum=pnum, toks=toks, header_upto=header_upto, sub=sorted(sub_idx), damaged=damaged)


def assign(seqs, rule=RULE):
    tok, st, en, exp = Counter(), Counter(), Counter(), Counter()
    for s in seqs:
        if len(s) < 2:
            continue
        for i, x in enumerate(s):
            tok[x] += 1
            exp[x] += 1 / len(s)
            st[x] += i == 0
            en[x] += i == len(s) - 1
    roles, table = {"NUM": 1}, []
    for x, n in tok.items():
        if x == "NUM" or n < rule["min_tokens"]:
            continue
        e = exp[x] / n
        if en[x] / n >= rule["close_share"] and en[x] / n >= rule["ratio"] * e:
            roles[x] = 2
            table.append(dict(sign=x, role="closer", uses=n, share=en[x] / n, shuffled=e))
        elif st[x] / n >= rule["open_share"] and st[x] / n >= rule["ratio"] * e:
            roles[x] = 0
            table.append(dict(sign=x, role="opener", uses=n, share=st[x] / n, shuffled=e))
        else:
            roles[x] = 1
    return roles, table


def scorable(s, r):
    return len({r[x] for x in s if x in r}) >= 2


def in_order(s, r):
    k = [r[x] for x in s if x in r]
    return all(a <= b for a, b in zip(k, k[1:]))


def conformance(seqs, r, n_null=500):
    sc = [s for s in seqs if scorable(s, r)]
    obs = float(np.mean([in_order(s, r) for s in sc]))
    null = np.array([np.mean([in_order(list(RNG.permutation(s)), r) for s in sc]) for _ in range(n_null)])
    return dict(n=len(sc), observed=obs, shuffled=float(null.mean()), p=float((1 + (null >= obs).sum()) / (n_null + 1)))


def main(corpus_dir):
    tabs = [parse(p) for p in sorted(Path(corpus_dir).glob("*.atf"))]
    for t in tabs:
        t["split"] = split_of(t["pnum"])
    ex = [t for t in tabs if t["split"] == "explore"]
    print(f"Proto-Elamite tablets: {len(tabs)}; exploration {len(ex)}; holdout {len(tabs) - len(ex)} (not read)")
    ex_ok = [t for t in ex if not t["damaged"] and len(t["toks"]) >= 2]
    L = [len(t["toks"]) for t in ex_ok]
    print(f"undamaged exploration tablets: {len(ex_ok)}; tokens per tablet median {np.median(L):.0f}, mean {np.mean(L):.1f}")
    out = {"rule": RULE, "tablets": len(tabs), "explore": len(ex), "explore_undamaged": len(ex_ok),
           "median_length": float(np.median(L))}

    # 1. Blind roles with the unchanged Indus rule
    seqs = [t["toks"] for t in ex_ok]
    roles, table = assign(seqs)
    print("\n== 1. Roles found by the unchanged Indus rule ==")
    for row in sorted(table, key=lambda r: (r["role"], -r["uses"])):
        k = "starts" if row["role"] == "opener" else "ends"
        print(f"   {row['role']:6} {row['sign']:10} uses {row['uses']:4}  {k} {row['share']:.0%}  (shuffled {row['shuffled']:.0%})")
    out["roles"] = table

    # 2. Slot order, against within-tablet shuffles
    c = conformance(seqs, roles)
    print(f"\n== 2. Slot order: {c['observed']:.1%} of {c['n']} tablets in order; shuffled {c['shuffled']:.1%}; p={c['p']:.4f}")
    out["conformance"] = c

    # 3. Answer key: do the blind openers fall inside the experts' headers?
    in_head = all_tok = op_in = op_all = 0
    for t in ex_ok:
        if t["header_upto"] is None:
            continue
        for i, x in enumerate(t["toks"]):
            if x == "NUM":
                continue
            all_tok += 1
            hdr = i < t["header_upto"]
            in_head += hdr
            if roles.get(x) == 0:
                op_all += 1
                op_in += hdr
    base = in_head / all_tok if all_tok else float("nan")
    share = op_in / op_all if op_all else float("nan")
    print(f"\n== 3. Answer key (tablets with an expert header mark) ==\n   sign tokens inside the expert header: {base:.1%} overall; "
          f"for blind openers: {share:.1%} ({op_in} of {op_all})")
    labelled = [t for t in ex_ok if t["header_upto"]]
    first_is_opener = np.mean([roles.get(t["toks"][0]) == 0 for t in labelled]) if labelled else float("nan")
    print(f"   expert-headed tablets whose first sign is a blind opener: {first_is_opener:.1%} of {len(labelled)}")
    out["answer_key"] = dict(base_share_in_header=base, opener_share_in_header=share, opener_tokens=op_all,
                             headed_tablets=len(labelled), first_sign_is_opener=float(first_is_opener))

    # 4. Closers vs expert subscripts
    sub_t = [t for t in ex_ok if t["sub"]]
    cl_in = cl_all = 0
    for t in sub_t:
        subs = set(t["sub"])
        for i, x in enumerate(t["toks"]):
            if roles.get(x) == 2:
                cl_all += 1
                cl_in += i in subs
    print(f"\n== 4. Closers vs expert subscripts: {len(sub_t)} tablets with a subscript; "
          f"closer tokens inside the subscript: {cl_in} of {cl_all}")
    out["subscripts"] = dict(tablets=len(sub_t), closer_tokens=cl_all, closer_in_subscript=cl_in)

    (ROOT / "results" / "proto_elamite_skeleton.json").write_text(json.dumps(out, indent=1, default=float))


if __name__ == "__main__":
    main(sys.argv[1])
