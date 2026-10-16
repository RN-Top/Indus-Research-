# Candidate names: an inventory of rare signs in the name-like slots (EXPLORATION, not a registered test)

*16 October 2026. Exploration split only. The holdout was not read, and nothing was tested or registered. Script: `scripts/name_inventory.py`. Full inventory: `name_inventory.json`. Printout: `name_inventory_output.txt`. Follows `rare_signs_as_names_scouting.md`.*

**Caveat:** this is a list of candidates, not names. Any of these signs could instead be a rare word, a variant form or a rare heading.

## The inventory

- **Rare** means a non-numeral sign used 5 times or fewer in exploration.
- **Name-like slots** are the first sign of a text with no heading, and the sign right before the closer.

| | Sign types | Used once | Repeated (2–5 uses) |
|---|---|---|---|
| **Candidates** (used at least once in a name-like slot) | **215** | 98 | 117 |
| Other rare signs (never in those slots) | 148 | 100 | 48 |

## Do the candidates behave like names?

**1. Where repeats stay.** If a rare sign is a person's name, repeats might stay at one city.
- **Result:** 32% of repeated candidates occur at only one site.
- **Comparison:** 23% would by chance, given how the corpus is spread over sites; 27% for other rare signs.
- **Reading:** a slight lean to one place. Weak.

**2. Which ending follows them.** Of the 67 closers that come right after a rare sign:

| Closer | After a rare sign | All texts |
|---|---|---|
| G740 (the generic ending) | **72%** (48) | 54% |
| G400 | 15% (10) | 13% |
| G520 | **4%** (3) | 11% |

- Rare signs are followed by the **generic closer G740** more often than usual, and almost never by G520.
- **Reading:** in Mesopotamian seals, a name is followed by the generic *arad₂-zu*, "your servant". G520 behaves differently: it usually follows "three long strokes" (`number_system_scouting.md`), a fixed formula, not a name. This is **the most name-like result here.**

**3. Two kinds of candidate.** Looking at the repeated candidates one by one:
- **Signs that always start a text,** for example G201 (first sign in all 5 uses) and G370 (5 of 5). Each sits on seals at several sites. They could be names that always come first. They could equally be **rare headings,** openers too rare for the rule to recognise.
- **Signs tied to one site and object,** for example G137 (5 uses, all Harappa tablets) and G869 (4 uses, all Harappa tablets). These look like **series of similar tablets** (the Harappa moulded tablets often repeat) rather than personal names.
- **Signs spread around,** for example G66, G702 and G804. They appear at several sites, on several object types, in several positions. These look more like rare *words* than names.

**4. One curiosity:** **G924** is used 4 times: at Harappa, at Mohenjo-daro, and on the seals found at **Susa** and at **Ur**. Two of its four uses are in West Asia. It could be anything. But a rare sign that turns up on two seals that travelled abroad is worth noting next to the "abroad seals" thread (`sign_travel_water.md`).

## Synthesis

**Mixed, with one clearly name-like feature.**
- **For:**
  - candidates are followed by the generic ending G740, like names before "your servant";
  - repeats lean slightly to one site.
- **Against, or other explanations:**
  - some "candidates" are better read as rare headings (G201, G370);
  - some are tablet series (G137, G869);
  - many are spread too widely to be one person's name.
- **So:** the name slots probably hold a mixture of names, rare headings and rare words. This data cannot separate them yet.

## Possible next steps

1. **Split the candidates by behaviour,** before any test:
   - always first;
   - always before G740;
   - spread around.

   Then check each group against the Mesopotamian pattern separately.
2. **Possible registration,** after the first-sign test (`drafts/H-headless-first-rare.DRAFT.json`):
   - Claim: rare signs right before a closer are followed by G740 more often than other closers are.
   - Exploration: 72% against 54%.
   - Expected holdout support: about 17, borderline. Not registered.
