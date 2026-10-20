# Beyond copper: do other tablets and seals tie text to image? (EXPLORATION)

*20 October 2026. Exploration split only. Script: `scripts/tablet_text_image.py`. Numbers: `tablet_text_image.json`. Same method as `copper_sets.md`, with three changes:*
- *"Othr" is also treated as vague;*
- *pairs from the same object (two sides of one tablet) are excluded;*
- *copper objects are excluded.*

| Genre | Objects with a specific label | Same-text pairs | Same image | Shuffled | p |
|---|---|---|---|---|---|
| Non-copper tablets (mostly Harappa) | 210 | 424 | **69%** | 9% | 0.0002 |
| Harappa tablets only | 174 | 385 | **70%** | 10% | 0.0002 |
| **Seals (control)** | 923 | 77 | **21%** | 13% | 0.05 |

## Reading

1. **Seals hardly tie text to image** (21% against 13%). The same seal text appears with different animals. This fits the earlier finding that seal animals are not named in seal texts.
2. **Harappa tablets show a strong link, but there is a confound.**
   - Many Harappa tablets are **moulded**: identical copies pressed from one mould.
   - Identical text with identical image is then partly mechanical copying, not evidence that the text refers to the image.
   - **The copper tablets were engraved one by one** (Parpola 2008), so their consistency is not a copying artefact. That is why the copper result is the meaningful one.
3. **The real 70% is probably higher.** Disagreements are often subtypes of one animal: the 24-copy set G501 G405 G2 G240 G520 is "Bull1:I" ×19, "Bull1" ×3 and "Bull1:U" ×2, all bulls.

**Largest Harappa sets:**

| Text | Copies | Image label |
|---|---|---|
| G501 G405 G2 G240 G520 | 24 | bull (all three subtypes) |
| G803 G415 G220 G318 G920 G255 G436 G690 G590 G407 G740 | 10 | "Gavi", gharial |
| G347 G741 G176 G740 G90 | 6 | "Mult", multi-headed animal |
| G465 G806 G158 | 4 | "Phyt", plant |

## Verdict

- **Text–image pairing is a property of tablet genres, not of seals.** That is a functional difference between object types.
- For moulded tablets it cannot be separated from mould copying, so **no holdout test is proposed for them.**
- A fair test would need mould identification: different moulds carrying the same text. The corpus does not record that.
