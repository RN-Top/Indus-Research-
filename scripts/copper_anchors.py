"""Anchor phrases: image-linked sign pairs/triples from the copper tablets, traced onto seals and other objects.
EXPLORATION split only. Image labels: the frozen lookup of H-2026-10-20-c3207807, with 'Othr' resolved from the
excavation drawings where results/copper_sets.md records it (tiger, rhinoceros, manger animal, markhor).

1. Anchors: contiguous 2- and 3-sign sequences found in copper texts of exactly ONE image (formula sequences, shared
   by two or more images, are excluded).
2. For each anchor: occurrences on non-copper objects, their object types, seal animals and slot.
3. Slot test (descriptive): share of anchor occurrences on seals that sit in the middle vs. random bigrams of
   matched frequency."""
import json, sys
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
from indus_workbench import data  # noqa: E402
from rare_signs import slots  # noqa: E402
from functional_skeleton import assign  # noqa: E402

RESOLVED = {"G798 G240 G845 G61 G407": "tiger", "G235 G233 G222 G740": "rhinoceros",
            "G503 G615 G752 G740": "horned animal with manger", "G231 G17 G585 G95 G520 G32 G407": "markhor goat"}
NAMES = {"Hare": "hare", "Elep": "elephant", "Anth": "horned archer", "Goat:8": "goat", "Loop": "loop/knot",
         "Bull1:W": "bull", "Gaur": "gaur", "Buff": "buffalo", "Rhin": "rhinoceros", "Comp": "composite animal"}

def grams(s, n):
    return [tuple(s[i:i + n]) for i in range(len(s) - n + 1)]

def main():
    h = json.load(open(ROOT / "hypotheses/H-2026-10-20-c3207807.json"))
    img = {}
    for t, lab in h["params"]["lookup"].items():
        lab = RESOLVED.get(t, NAMES.get(lab))
        if lab: img[t] = lab
    by_gram = defaultdict(set)
    for t, lab in img.items():
        s = t.split()
        for n in (2, 3):
            for g in grams(s, n): by_gram[g].add(lab)
    anchors = {g: next(iter(l)) for g, l in by_gram.items() if len(l) == 1}
    formula = {g: sorted(l) for g, l in by_gram.items() if len(l) > 1}
    raw, _ = data.load_raw("indus_website")
    c = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"), drop_damaged=True, dedupe=False, drop_unidentified=True)
    e = data.explore_only(c).df
    seqs = [list(s) for s in e.signs]; roles, _ = assign(seqs)
    nc = e[~e.material.astype(str).str.contains("opper", case=False)]
    occ = defaultdict(list)
    for s, o, m, site in zip(nc.signs, nc.object_type, nc.motif_group.astype(str), nc.site):
        s = list(s); lab = slots(s, roles)
        for n in (2, 3):
            for i, g in enumerate(grams(s, n)):
                if g in anchors:
                    occ[g].append(dict(obj=o, motif=m, site=site, slot=lab[i], text=" ".join(s)))
    print(f"copper image texts: {len(img)}; anchors: {len(anchors)}; formula sequences: {len(formula)}")
    print("formula sequences (shared by 2+ images):", {" ".join(g): l for g, l in formula.items()})
    rows = []
    for g, lab in sorted(anchors.items(), key=lambda kv: -len(occ[kv[0]])):
        o = occ[g]
        if not o: continue
        rows.append(dict(anchor=" ".join(g), image=lab, n=len(o), objects=dict(Counter(x["obj"] for x in o)),
                         seal_animals=dict(Counter(x["motif"] for x in o if x["obj"] == "seal")),
                         slots=dict(Counter(x["slot"] for x in o)), sites=dict(Counter(x["site"] for x in o).most_common(3)),
                         examples=[x["text"] for x in o[:3]]))
    for r in rows:
        print(f"\n{r['anchor']:16} [{r['image']}] n={r['n']} objects {r['objects']} slots {r['slots']}\n   seal animals {r['seal_animals']} sites {r['sites']}\n   e.g. {r['examples']}")
    # slot comparison for anchor bigrams on seals vs all bigrams on seals of similar frequency
    seal_bi = Counter(); seal_mid = Counter()
    for s, o in zip(nc.signs, nc.object_type):
        if o != "seal": continue
        s = list(s); lab = slots(s, roles)
        for i, g in enumerate(grams(s, 2)):
            seal_bi[g] += 1; seal_mid[g] += lab[i] in ("middle", "first middle") and lab[i + 1] in ("middle", "last middle")
    a = [g for g in anchors if len(g) == 2 and seal_bi[g] > 0]
    a_mid = sum(seal_mid[g] for g in a) / max(1, sum(seal_bi[g] for g in a))
    allmid = sum(seal_mid.values()) / sum(seal_bi.values())
    print(f"\nanchor bigrams on seals: {sum(seal_bi[g] for g in a)} occurrences of {len(a)} anchors; fully inside the middle {a_mid:.0%} vs {allmid:.0%} of all seal bigrams")
    (ROOT / "results" / "copper_anchors.json").write_text(json.dumps(dict(anchors=rows, formula={" ".join(g): l for g, l in formula.items()},
                                                                           seal_middle_share=a_mid, all_middle_share=allmid), indent=1))

if __name__ == "__main__":
    main()
