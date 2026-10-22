# Seal text vs animal emblem (scouting, exploration split only)

*20 October 2026. Script: `scripts/emblem_scouting.py` (plus inline checks recorded here). Not a confirmatory test.*

**Lens:** a seal is a badge with two parts, an animal emblem and a short text. On copper tablets the text predicts the picture almost perfectly (`copper_image_test.md`). Does the same hold on seals?

| Check | Result |
|---|---|
| Text predicts unicorn vs other animal (815 seals, 5-fold CV, balanced accuracy) | **0.49** vs 0.50 shuffled (p 0.61): no signal |
| Same, Mohenjo-daro only (547 seals) | 0.47 vs 0.50 (p 0.75) |
| Text predicts the exact animal (8 animals) | 0.175 vs 0.124 (p 0.025): weak |
| Text predicts the unicorn's carving style (ICIT sub-codes) | 0.21 vs 0.17 (p 0.05): weak, probably workshop/site |
| Seals with an *identical* text (30 texts, 77 seals, duplicates kept) share their animal | 77% of pairs vs 71% with animals shuffled within site (p 0.14) |
| Text length, unicorn vs other | 5.1 vs 4.8 signs (median 5 both) |

**Reading.** On seals the emblem and the text are two largely **independent channels**, unlike the copper tablets. Identical texts recur across cities (Harappa, Mohenjo-daro, Lothal, Banawali) under different animals, e.g. `G3 G156` on a gaur seal and five unicorn seals; `G61 G740` on a goat seal and four unicorn seals. A text that recurs across cities under different emblems does not behave like one person's name; it looks like a **title, office or formula** that many holders shared, while the emblem marks something else (a group, an office type, or simply the default unicorn).

**Caveats.** The unicorn dominates (82% of labelled seals), so "other" is a mixed bag; repeated texts are short; the multi-animal weak signal may be site mix. Possible confirmatory version: register the copper-vs-seal contrast (text predicts image on copper, not on seals) rather than a bare null.

**Prior work.** The observation is old: Ganesan et al. 2009 (*Bulletin of the Indus Research Centre* 1, §7.1(7)): "the same text occurs with different field symbols and vice versa"; Farmer and Ruzsa on INDOLOGY (2000); Frenez 2018 (p. 172): the animal had a function separate from the inscription. No predictive test found. See `prior_work_check_2026-10-20.md`.

## Multi-headed (composite) animals

*Added 20 October 2026, exploration only.* Prompted by the uninscribed three-headed seal from Mohenjo-daro (DK 7734; Mackay 1938, pl. XCVI, 494; harappa.com slide).

- Only **2** inscribed exploration seals show the multi-headed animal (`G215 G740`; `G853 G16 G390 G401`): too few to compare with other seals.
- The motif is mainly on **moulded clay and faience tablets** (28 at Harappa and Mohenjo-daro).
- Its texts never appear with another identified image: `G347 G741 G176 G740 G90` ×6 (Harappa), `G4 G700 G97 G400` ×4 (Mohenjo-daro), `G736 G904 G158 G400` ×2, `G137 G400` ×2 (plus 3 with no image recorded).
- **Caveat:** moulded tablets come from moulds, so identical copies share text and image automatically; that tie is not evidence. The informative part is the other direction: **one image goes with at least four different texts**, and the two cities use different texts with it. Here the text does not name the image, unlike the individually engraved copper tablets.
- Across all non-copper tablets, 20 of 32 repeated texts keep a single image.

## Do copper-tablet image signs carry over to seals? (added 22 October 2026)

Signs tied to images on the copper tablets (`copper_image_test.md`): G706 (elephant; 2 of 2 copper uses in exploration on elephant tablets). On exploration seals, G706 appears on **0 of 23 elephant seals** and on 23 of 824 seals with other animals (Fisher p 1.0); G850, G321, G777 and G781 are too rare on seals with the matching image to test. The text-to-image link is specific to the copper tablets, where whole texts act as fixed labels; on seals the same signs are ordinary vocabulary.
