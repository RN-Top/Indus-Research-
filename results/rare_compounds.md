# Are rare signs compounds of common signs? (scouting, exploration only)

*22 October 2026. Script: `scripts/rare_compounds.py`. "Derived" = the blind shape annotation (`data/sign_marks/marks_blind_2026-10-20.csv`) gives the sign a base sign (an added mark, doubling or ligature), followed to the root. 490 of the 530 signs used in the exploration split are annotated. Not a confirmatory test.*

| Uses in exploration | Signs | Derived from a base | Ligatures |
|---|---|---|---|
| 1 | 177 | 59% | 10% |
| 2–6 | 177 | 54% | 5% |
| 7–30 | 85 | 61% | 2% |
| 31+ | 51 | 37% | 4% |

- **Rare signs are not specially compounds.** 200 of 354 rare signs (≤ 6 uses) are derived, against 71 of 136 commoner ones (Fisher p 0.42). Derivation is productive at every frequency; only the commonest signs are more often plain.
- **The real inventory is about half the size.** Folding derived signs into their roots turns 530 signs into **259 base shapes**; the 100 commonest bases cover 96% of all sign uses.
- **A derived sign does not inherit its base's position.** Its mean position differs from its base's by 0.30 of a text's length, no closer than a random common sign (0.28; p 0.97). Adding a mark gives a sign a new role rather than a variant of the old one, as the mark classes showed for top and corner marks (`mark_classes.md`).

**Reading.** Rarity is not explained by compounding: rare signs are rare whether plain or built. But the script is more systematic than its 500+ sign list suggests: about 260 base shapes, roughly half of all signs built from them by a small set of marks, with the mark (not the base) deciding where the new sign goes.

**Caveats.** One annotator plus a partial second reading; "base" follows the annotation's single chain; position is one aspect of role.
