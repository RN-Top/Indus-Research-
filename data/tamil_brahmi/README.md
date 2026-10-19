# Early Tamil inscriptions: word roles (derived data)

**Source.** I. Mahadevan, *Early Tamil Epigraphy from the Earliest Times to the Sixth Century A.D.* (Harvard Oriental Series 62, 2003; revised 2014). Erin supplied the Internet Archive OCR text.

**How it was made.** An agent extracted the data on 19 October 2026. It was not told any Indus hypothesis.

## Files

| File | Contents |
|---|---|
| `corpus_roles.jsonl` | The book's corpus, 110 inscriptions: 89 Tamil-Brahmi (Nos. 1–89) and 21 Early Vatteluttu (Nos. 101–121). Each has the constituted text (B), word by word, with stem, suffixes and one role tag. |
| `objects_roles.jsonl` | 75 short legends quoted in the running text: 46 pottery, 16 coin, 10 ring, 3 seal. |

**Translations are left out** because they are the author's copyright. Only the transliterated texts, which are facts about the ancient inscriptions, and our own role tags are kept here.

## Role set

- PERSONAL_NAME
- PLACE_NAME
- TITLE_OR_OCCUPATION
- KINSHIP
- GIFT
- OBJECT_DONATED
- VERB
- PARTICLE_OR_DEMONSTRATIVE
- NUMERAL
- OTHER

## Limits

- **OCR lost most diacritics.**
- **Text quality:** 8 corpus entries are low confidence. No. 71 has no text.
- **Most object legends are a single name.** The book's catalogue tables were unreadable in the OCR, so these legends are thin for structural comparison.
- **The corpus is cave donation records,** a different genre from Indus seals.
