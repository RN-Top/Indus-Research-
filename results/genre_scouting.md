# Can the kind of object be told from its inscription? (EXPLORATION)

*20 October 2026. Exploration split only. Script: `scripts/genre_scouting.py`.*

**Classes:** seal, tablet, other (pottery, tags and the rest), over 1,988 texts.

**Method:**
- logistic regression with balanced class weights;
- 5-fold cross-validation, **grouped by exact text**, so copies of one text never sit on both sides;
- score: balanced accuracy, where chance is 33.3%.

| Features | Balanced accuracy | Labels shuffled (20 runs) |
|---|---|---|
| **Position only:** length, opens with an opener, which closer it ends in, numerals present, first or last | **47.3%** | 33.1% (max 38.2%) |
| Position + which signs occur | 48.5% | 33.0% (max 35.6%) |

**Reading:**
- **The object type can be predicted from the inscription well above chance, and almost all of that comes from position alone.** Which closer a text ends in, how long it is, and whether it has a heading or numbers separate seals from tablets and other objects.
- Knowing the actual signs adds little.
- This supports **object-specific formats** ("genres"): seals and tablets are written to different templates.
- Wells (1998, p. 83) said in passing that artefact classes differ in sign sequences. This would be the held-out test of that statement.

**Possible registration:**
- Claim: on the holdout, a position-only model trained on exploration predicts the object type with balanced accuracy above the label-shuffled distribution.
- Size: the holdout has about 395 texts, enough for this.
- **Not registered.** It waits for Erin's go-ahead.
