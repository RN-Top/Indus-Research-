# The two layers of a seal: held-out tests

*21 October 2026. Registrations `hypotheses/H-2026-10-21-74e127e6.json` and `H-2026-10-21-d797caf3.json` (commit `390e3ee`, pushed before the run). Raw output `confirmatory_2026-10-21.json`. Scouting: `emblem_scouting.md`, `two_kinds_of_seal_text.md`.*

## 1. The text barely knows the animal (bounded claim)

- Model trained on exploration seals, scored on 218 holdout seals whose exact text never occurs in the exploration split.
- Balanced accuracy, unicorn vs other: **0.49** (chance 0.50); bootstrap 95% upper bound **0.56**, below the pre-set bound of 0.60. p 0.006, q 0.007. **Supported.**
- Prior observation: Ganesan et al. 2009; Frenez 2017 (`prior_work_check_2026-10-20.md`). As far as we found, this is the first held-out predictive test.

## 2. Size follows the image type, not the text

- Unicorn seals with the ICIT sub-type code **W** are **25.7% larger** than other unicorn seals with the same text length at the same site (48 vs 76 holdout seals; p 0.0002, q 0.0003). **Supported.** Exploration: +24.9%.
- **What W means.** Wells (1998, MA thesis, p. 28): "the Type 1 Bull has markings similar to an upper case W, while the Type 2 Bull consists of two unconnected linear markings"; these body/neck markings "are repeated at all major Indus sites", and Type 1 (W) bulls are proportionally commonest at Harappa (the test compares within site). So Bull1:W = a unicorn carved with W-shaped body markings. Fuls (pers. comm. to E. R. Toppe, October 2026) points to Wells (2011), *Epigraphic Approaches to Indus Writing*, for the full classification (not yet read). The other sub-codes (J, S, I, L, U, …) are presumably the other marking shapes; unconfirmed.
- So: **unicorn seals with W-shaped body markings are about 26% larger** than other unicorn seals with the same text length at the same site.

## Together

On seals the image layer (animal, its sub-type, the seal's size) and the text layer are separate: the text does not predict the animal, and size tracks the image sub-type at fixed text length. With the scouting results (writing uniform across regions and neighbourhoods while carving styles were regional; Jamison 2018), the working model is a **two-layer object**: an image layer made and graded by workshops, and a standardized text layer.

**Not tested:** the time trend (too few strictly dated texts; see the correction in `context_scouting.md`) and per-animal size (weak once seals without an animal are excluded).
