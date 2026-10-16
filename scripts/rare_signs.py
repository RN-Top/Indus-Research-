"""Do rare signs behave like names? (EXPLORATION ONLY: description from several angles, no tests.)

Rare sign = used 5 times or fewer in the exploration corpus. Angles: frequency
profile; where rare signs sit (heading / first middle / middle / last middle /
closer); object types; the frame around them; and counter-explanations
(damage, variant forms listed by the source, length). A Mesopotamian seal-legend
reference, where the middle is known to hold names, is computed the same way.
Exploration splits only; nothing tested or registered.

    python scripts/rare_signs.py [path/to/cdli_data]
"""

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
from functional_skeleton import assign  # noqa: E402
from functional_slots import DS, load  # noqa: E402
from indus_workbench import data  # noqa: E402

RARE = 5


def slots(s, roles):
    """Label each position: heading, first-middle, middle, last-middle, closer."""
    n = len(s); lab = ["middle"] * n
    i = 0
    while i < n and roles.get(s[i]) == 0:
        lab[i] = "heading"; i += 1
    if 0 < i < n and s[i] in ("G2", "G60"):
        lab[i] = "heading"; i += 1
    j = n
    while j > i and roles.get(s[j - 1]) == 2:
        lab[j - 1] = "closer"; j -= 1
    if j - i >= 1:
        lab[i] = "first middle"
    if j - i >= 2:
        lab[j - 1] = "last middle"
    return lab


def profile(seqs, roles, label, out):
    tok = Counter(x for s in seqs for x in s)
    types = len(tok); ntok = sum(tok.values())
    freq_of_freq = Counter(min(n, 11) for n in tok.values())
    rare_types = sum(1 for n in tok.values() if n <= RARE)
    rare_tok = sum(n for n in tok.values() if n <= RARE)
    print(f"\n== {label} ==")
    print(f"   1. {types} sign types, {ntok} tokens; used once {freq_of_freq[1]}, twice {freq_of_freq[2]}, 3x {freq_of_freq[3]}, "
          f"4x {freq_of_freq[4]}, 5x {freq_of_freq[5]}; rare (<= {RARE}) = {rare_types / types:.0%} of types, {rare_tok / ntok:.1%} of tokens")
    by = Counter(); rr = Counter()
    for s in seqs:
        for x, l in zip(s, slots(s, roles)):
            by[l] += 1; rr[l] += tok[x] <= RARE
    order = ["heading", "first middle", "middle", "last middle", "closer"]
    print("   2. share of signs that are rare, by slot: " + ", ".join(f"{l} {rr[l] / by[l]:.1%} (of {by[l]})" for l in order if by[l]))
    out[label] = dict(types=types, tokens=ntok, freq_of_freq=dict(freq_of_freq), rare_type_share=rare_types / types,
                      rare_token_share=rare_tok / ntok, rare_by_slot={l: [rr[l], by[l]] for l in order})
    return tok


def main(cdli=None):
    out = {}
    df = load(); df = df[df["signs"].map(len) > 0].reset_index(drop=True)
    seqs = [list(s) for s in df["signs"]]
    roles, _ = assign(seqs)
    tok = profile(seqs, roles, "Indus (exploration)", out)
    rare = lambda x: tok[x] <= RARE  # noqa: E731
    has_rare = np.array([any(rare(x) for x in s) for s in seqs])

    # 3. object types
    print("   3. by object type: texts with a rare sign / share of tokens that are rare")
    obj = {}
    for o, g in df.groupby("object_type"):
        if len(g) < 20:
            continue
        ix = g.index
        t = [x for i in ix for x in seqs[i]]
        obj[o] = dict(texts=len(g), with_rare=float(has_rare[ix].mean()), rare_tokens=float(np.mean([rare(x) for x in t])),
                      mean_len=float(np.mean([len(seqs[i]) for i in ix])))
        print(f"      {o:8} {len(g):5} texts: {obj[o]['with_rare']:.0%} have a rare sign; {obj[o]['rare_tokens']:.1%} of tokens rare; mean length {obj[o]['mean_len']:.1f}")
    out["objects"] = obj

    # 4. frame around rare signs
    shp = Counter()
    for s in seqs:
        if not any(rare(x) for x in s):
            continue
        lab = slots(s, roles)
        where = {l for x, l in zip(s, lab) if rare(x)}
        head = "heading" in lab; clo = "closer" in lab
        shp[("heading" if head else "-") + " + rare in " + "/".join(sorted(where)) + " + " + ("closer" if clo else "-")] += 1
    n_r = int(has_rare.sum())
    framed = sum(v for k, v in shp.items() if k.startswith("heading") and k.endswith("closer"))
    any_frame = sum(v for k, v in shp.items() if k.startswith("heading") or k.endswith("closer"))
    print(f"   4. {n_r} texts contain a rare sign; with heading AND closer around it: {framed} ({framed / n_r:.0%}); "
          f"with at least one of them: {any_frame} ({any_frame / n_r:.0%})")
    base_both = np.mean([("heading" in slots(s, roles)) and ("closer" in slots(s, roles)) for s in seqs])
    base_any = np.mean([("heading" in slots(s, roles)) or ("closer" in slots(s, roles)) for s in seqs])
    print(f"      all texts for comparison: both {base_both:.0%}, at least one {base_any:.0%}")
    print("      commonest shapes:", shp.most_common(6))
    out["frame"] = dict(rare_texts=n_r, framed=framed, any_frame=any_frame, base_both=float(base_both), base_any=float(base_any),
                        shapes=shp.most_common(15))

    # 5a. damage and length
    raw, _ = data.load_raw("indus_website")
    full = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"),
                             drop_damaged=False, dedupe=True, drop_unidentified=True)
    ex = data.explore_only(full).df
    dmg = ex["damaged"].astype(str).isin(["True", "true", "1"])
    def rshare(frame):
        t = [x for s in frame["signs"] for x in s]
        return np.mean([tok[x] <= RARE for x in t]), len(t)
    d, nd = rshare(ex[dmg]); u, nu = rshare(ex[~dmg])
    print(f"   5a. damaged texts (kept only for this check): {dmg.sum()} texts; rare-sign share {d:.1%} of {nd} tokens, "
          f"against {u:.1%} in undamaged texts (rarity measured on undamaged counts)")
    Lr = np.mean([len(s) for s, h in zip(seqs, has_rare) if h]); Ln = np.mean([len(s) for s, h in zip(seqs, has_rare) if not h])
    print(f"       mean length: texts with a rare sign {Lr:.1f}, without {Ln:.1f}")
    out["damage"] = dict(damaged_texts=int(dmg.sum()), rare_share_damaged=float(d), rare_share_undamaged=float(u),
                         len_with_rare=float(Lr), len_without=float(Ln))

    # 5b. variant forms listed by the source
    var = pd.read_csv(ROOT / "data" / "glyph_variants.csv")
    pairs = set(map(tuple, var.iloc[:, :2].astype(str).values))
    partner = {}
    for a, b in pairs:
        partner.setdefault(a, set()).add(b); partner.setdefault(b, set()).add(a)
    rare_signs = [x for x in tok if rare(x)]
    with_common_partner = [x for x in rare_signs if any(tok[p] > RARE for p in partner.get(x, ()))]
    common_signs = [x for x in tok if not rare(x)]
    cp_common = [x for x in common_signs if any(tok[p] > RARE for p in partner.get(x, ()))]
    print(f"   5b. rare sign types with a source-listed similar sign that is common: {len(with_common_partner)} of {len(rare_signs)} "
          f"({len(with_common_partner) / len(rare_signs):.0%}); for common signs: {len(cp_common) / len(common_signs):.0%}")
    out["variants"] = dict(rare_types=len(rare_signs), rare_with_common_partner=len(with_common_partner),
                           common_with_common_partner_share=len(cp_common) / len(common_signs),
                           examples=sorted(with_common_partner, key=lambda x: -tok[x])[:15])

    # Mesopotamian reference: the middle is known to hold names
    if cdli:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import mesopotamian_seals as ms
        import proto_elamite_skeleton as pe
        import hashlib
        folder = Path(cdli)
        cat = pd.read_csv(folder / "cdli_cat.csv", usecols=["id_text", "period", "object_type"], dtype=str, low_memory=False)
        cat["P"] = "P" + cat["id_text"].str.zfill(6)
        info = cat.set_index("P")[["period", "object_type"]].to_dict("index")
        leg = {}
        for pn, kind, lines in ms.parse(folder / "cdliatf_unblocked.atf"):
            meta = info.get(pn, {}); period = str(meta.get("period", ""))
            if not period.startswith(ms.PERIODS) or (kind == "object" and "seal" not in str(meta.get("object_type", ""))):
                continue
            t = [w for ln in lines for w in ln]
            if len(t) >= 2:
                leg.setdefault(" ".join(t), t)
        mex = [t for k, t in leg.items() if int(hashlib.sha256(f"{ms.SALT}:{k}".encode()).hexdigest(), 16) % 100 >= 20]
        mroles, _ = pe.assign(mex)
        mroles = {k: v for k, v in mroles.items() if k != "NUM"}
        profile(mex, mroles, "Mesopotamian seal legends (exploration; words; reference)", out)
    (ROOT / "results" / "rare_signs.json").write_text(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main(*sys.argv[1:2])
