# Does the writing vary by region? (scouting, exploration split only)

*20 October 2026. Script: `scripts/region_scouting.py`. Region labels from the ICIT export (see `context_scouting.md`). Seals only, duplicates removed, texts of 2+ signs. Not a confirmatory test.*

**Prompt.** Jamison (2018, in Uesugi ed., *Current Research on Indus Archaeology*, pp. 169–194) finds distinct **regional carving styles** on inscribed steatite seals: Ghaggar-Hakra seals are dominated by right-facing animals; none of the Gujarat seals he analysed face right, and 56 of 68 are unicorns. If the carvers were regional, was the writing?

| Region | Seals | Mean length | Heading | Closer | Jar G740 | Numeral | Enclosure-mark sign |
|---|---|---|---|---|---|---|---|
| Lower Indus (Mohenjo-daro etc.) | 724 | 5.2 | 31% | 70% | 53% | 63% | 7% |
| Inter-Riverine (Harappa) | 213 | 4.9 | 24% | 69% | 52% | 62% | 4% |
| Gujarat/Kutch | 84 | 4.7 | 26% | 68% | 44% | 60% | 2% |
| Eastern Headwaters (Ghaggar) | 13 | 3.2 | 15% | 54% | 38% | 38% | 15% |

- **Region from the text** (5-fold CV, balanced accuracy, 4 regions): **0.26 vs 0.25** with labels shuffled (p 0.34). The text carries no regional signature.
- **Single signs:** of about 60 signs with 15+ seals, the smallest regional p-values are 0.006 (G806), 0.012 (G405), 0.013 (G3), 0.025 (G590). About 3 would fall below 0.05 by chance; none survives correction.

**Reading.** On seals, the **writing is the same across the whole Indus area**, from Sindh to Gujarat, while the **carving of the images was regional** (Jamison). A standard taught or enforced across regions, separate from the local craft workshops that carved the seals, fits this; so does a single scribal tradition serving many workshops. It also matches the within-city result (`context_scouting.md`: no neighbourhood vocabulary).

**Caveats.** Gujarat (84) and especially the Ghaggar region (13) are small; the Ghaggar row is noise-level. A confirmatory version would need the holdout and probably pooled non-Mohenjo-daro sites.
