# Function theory, first comparison: Proto-Elamite

*Exploratory. 15 October 2026. Script `scripts/proto_elamite_skeleton.py`; output in `proto_elamite_skeleton_output.txt` and `proto_elamite_skeleton.json`. Indus holdout untouched; nothing registered.*

## Data

- **Corpus:** Proto-Elamite tablets (Iran, about 3100–2900 BCE; undeciphered accounting) from Born et al. (2022), [github.com/sfu-natlang/pe-headers](https://github.com/sfu-natlang/pe-headers). The transliterations come from CDLI and may be reused under CDLI's terms with citation.
- **Not copied into this repository:** the script reads them from a local folder.
- **Holdout:** a 20% Proto-Elamite holdout (hash of the P-number, salt `pe-holdout-v1`, 294 tablets) is set aside and was not read.
- **Exploration set:** 1,173 tablets. Following Born et al., a tablet was kept when its first and last lines are intact, with broken signs elsewhere dropped. That leaves 437 tablets.

## Method

- **The rule is unchanged** from the Indus work (`functional_by_site.md` D.1): it was not tuned to Proto-Elamite.
- **Numbers:** each number group on a line counts as one numeral token.
- **Answer key:** experts have marked the end of each tablet's header (`# header`, 341 of the exploration tablets) and a closing "subscript" line (58 tablets). So we can check whether the blind rule finds what experts already know.

## Results

**1. The rule recovers the experts' headers.** It found 6 opening signs. M157 is the commonest: it starts 89% of its tablets, against 11% if signs were shuffled. Of all uses of these blind "openers", **81% fall inside the expert-marked header**, against **9%** for sign uses in general. In 59% of expert-headed tablets, the very first sign is one of the blind openers. On a script where the answer is known, the method finds the heading.

**2. Slot order.** 87.2% of 226 scorable tablets are in order, against 12.7% shuffled (p = 0.002). This is weaker evidence than it looks: with no closers, "in order" mostly means "the opener comes first".

**3. The endings differ, sharply.** The rule found **no closing signs** in Proto-Elamite. Instead, **80% of tablets end in a number** (usually a total).

| | Proto-Elamite tablets | Indus seals | Indus tablets |
|---|---|---|---|
| Last token is a number | **80%** of 437 | 3% of 1,057 | 5% of 350 |
| Ends with a closing sign | none found | G740 jar alone ends 35% of all texts | (same closers) |
| Share of tokens that are numbers | 34% | 16% (all Indus texts) | |

## What it suggests (exploratory)

- **Same opening convention.** Both scripts open with a small set of heading signs, found by the same blind rule. In Proto-Elamite those openers coincide with what experts independently call the header.
- **Different kind of document.** Proto-Elamite accounts end with a **total**. Indus inscriptions, on tablets as well as seals, almost never end with a number. They end with **closing signs**, which earlier work showed track object type and context, like a category mark. On this measure the Indus texts look less like account tablets and more like **labels or titles**.
- **For the function theory:** this is "same job, partly the same shape". It is not evidence of one origin. Both are administrative systems of the same era, and headers are a common solution. The difference in endings is itself informative.

## Limits

- **Different kinds of objects:** Proto-Elamite accounts are long clay tablets; Indus texts are short seals and tablets.
- **Numbers are coded differently** in the two corpora.
- **Damage filtering differs** between the two.
- **Proto-Elamite holdout unused:** it is kept for a pre-registered test. Candidates are "blind openers fall inside expert headers more than chance" and "Proto-Elamite texts end in numbers far more often than Indus texts".
- **Next comparison:** Mesopotamian seal legends, with known meaning, would test the "label" reading of Indus endings directly.
