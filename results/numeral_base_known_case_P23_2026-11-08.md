# P23 known-case check: coding rule on Tamil and Hebrew (8 Nov 2026)

Applied by hand, step by step, from the forms in `data/numerals/numerals/cldf/forms.csv` (numeralbank, CC BY 4.0). No Indus form was read.

| Language | 10 | 20 | 100 | Rule result | Source Base label |
|---|---|---|---|---|---|
| Tamil (India) | pattu (single root) | irubathu = iru "two" + pattu "ten" | nooru (single root) | Decimal (step 2) | decimal: agrees |
| Hebrew | eser (single root) | esrim (plural of eser, not "two + ten") | meah (single root) | Step 2 is ambiguous for 20 | unlabelled |

## Result
- Tamil: agrees with the source label. One of two known cases passes.
- Hebrew: the rule as written does not settle the 20 form. "esrim" is a plural of the word for ten, not "two + ten" and not a separate root. Step 2 needs a clause for this case.

## Rule gap (logged before any Indus form is read)
Step 2 should cover a 20 form that is a derived form of the word for 10 (for example a plural or dual of it). Proposed clarification: "a 20 form that is built from the 10 root by a plural or dual suffix counts as decimal." This is a revision made before the Indus side, and it is logged here, not on Indus data.

## Limits
- Two languages is far too few to call the method validated. This is a check that the rule runs and can disagree with a source label.
- Applied by hand. The rule has not been coded, so it can't yet be run on all families.
- The Hebrew revision above is not yet hashed. It needs its own hash before any Indus numeral is read.
