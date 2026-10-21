# Copper "anchor" phrases traced onto seals and tablets (EXPLORATION)

*20 October 2026. Exploration split only. Script: `scripts/copper_anchors.py`. Numbers: `copper_anchors.json`. Builds on `copper_image_test.md` (confirmed) and `copper_anchors_on_seals.md`.*

**Method:**
- From the 22 copper texts with a known image, every 2- and 3-sign sequence was split into two groups:
  - **anchor**: found with exactly one image (96 sequences);
  - **formula**: shared by two or more images (27).
- Anchors were then searched for on all non-copper objects.

## 1. Most anchors are ordinary seal phrases

| Anchor | Copper image | Uses off copper | Where | Seal animals |
|---|---|---|---|---|
| G415 G220 | loop/knot | 50 | 27 seals, 23 tablets | unicorn 17, none 9 |
| G32 G220 | composite animal | 37 | 35 seals | unicorn 24 |
| **G706 G33** | **elephant** | 24 | 24 seals | unicorn 13, none 9, gaur 2, **elephant 0** |
| G900 G740 | horned archer | 18 | 16 seals | unicorn 9 |
| G590 G405 | loop/knot | 16 | 11 seals, 5 tablets | |
| G752 G740 | horned animal with manger | 11 | 9 seals | |
| G176 G100 (G740) | goat | 10 | 6 seals, 4 tablets | |
| G235 G705 G33 | hare | 5 | 4 seals | |

**Reading:**
- The image-specific parts of copper texts are built from the **same phrase stock as seal texts**.
- On seals they do **not** go with the matching animal: no elephant seal carries the elephant phrase.
- They sit slightly more often fully inside the middle of the text: 76% of anchor occurrences, against 66% of all seal sign pairs.

## 2. Fish signs and the image-specific part: NOT supported by the cleaner check

*The sequence-level count below looked striking. The sign-level check at the end of this section, run the same day, shows it does not hold. The section is kept as a record.*

| Copper sequences | Containing a fish-family sign (G220–G244) |
|---|---|
| Anchors found off copper | **13 of 30 (43%)** |
| Formula sequences (shared across images) | **1 of 27 (4%)** |
| All copper text signs | 13% of signs are fish-family |

On the copper tablets the part that **changes with the picture** is often a fish compound, for example:
- G415 G220 with the loop;
- G32 G220 with the composite animal;
- G235 G705 with the hare;
- G798 G240 with the tiger.

The shared formula (G845 G407, G33 G923, G740) almost never contains a fish.

**At sequence level this looked like Parpola's proposal** (1994; 2005: 52–54; 2008) that fish signs form divine or celestial names, and that the copper images depict deities. It is independent support in the sense that it comes from position and image only, with no sound values. It does not show that the fish signs *are* divine names.

## Caveats

- The counts are sequences, not independent texts. Only 22 copper texts underlie them, and overlapping sequences from one text are counted separately.
- The fish family is taken as G220–G244, by shape from Fuls (2022), Table 2.6.
- **The cleaner check, done at sign level.**
  - Each sign in the 22 copper texts was marked image-specific (found with one image only) or formula (found with two or more images).
  - Fish-family share among image-specific signs: **7%**, of 27 signs.
  - Fish-family share among formula signs: **9%**, of 88 signs.
  - Shuffling the image labels across texts gives p = 0.90.
  - **No enrichment.** The sequence-level figure arose because fish signs such as G220 occur with several images, while their particular *pairings* are image-specific. **The fish claim is withdrawn.**
- Holdout copper texts mostly repeat exploration texts, so a holdout test of this claim would have little independent support.

## What it suggests about seals

If a fish compound on a copper tablet names what the image stands for, then the same compound on a unicorn seal is a **reference to that figure inside the seal text**, not a label for the seal's animal. That could be:
- part of a personal name, like Mesopotamian names built on a god's name;
- or a title or affiliation.

The data so far cannot decide between them.

## 3. Name or title? Checked against frequency-matched phrases (exploration)

*20 October 2026.*

**Method:**
- Seal texts, duplicates removed.
- Each anchor sign pair on a seal was placed in the text's layout:
  - **name start**: the first sign of a text with no heading;
  - **interior**: neither right after a heading nor right before the closer.
- Each anchor was compared with ordinary sign pairs of similar frequency, ±30%, with 2,000 draws.

| Position | Anchor pairs (127 uses, 18 anchors) | Frequency-matched pairs | 95% range |
|---|---|---|---|
| Name start | 16.5% | 19.6% | 13.4–26.4% |
| Interior | 52.0% | 38.5% | 24.8–52.4% |

**Reading:**
- **No difference at the name slot.** The picture phrases are no rarer there than ordinary phrases of the same frequency. The earlier raw gap (12% against 16%) was a frequency effect.
- **A lean towards the interior,** right at the edge of what chance gives.
- **Neither "name" nor "title" is supported clearly.**

**Not registered.** The holdout would hold about 33 anchor uses on seals. That is enough to pass the minimum, but power for a 13-point gap at the edge of the null is low, roughly a coin flip. A failed low-power test would read as "not supported" when the data simply cannot tell. Revisit with a second transcription or a larger corpus.
