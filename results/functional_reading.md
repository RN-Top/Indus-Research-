# Reading by function: what the signs and chunks do

*Exploratory. 14 October 2026. Exploration split only: 1,523 distinct texts, with damaged texts, unidentified signs and duplicates removed. The holdout was not read. To reproduce: `python scripts/functional_slots.py` (output in `functional_slots_output.txt` and `functional_slots.json`).*

## What "reading the function" can and cannot establish

**What it can establish.** Function analysis asks what job a sign or chunk does: where it sits, what it combines with, and what kind of object it appears on. It can show that inscriptions follow a fixed layout and that particular signs fill particular slots in it. It can also show that a slot tracks the kind of object.

**What it cannot establish.** It does not give sounds or words. A slot labelled "opener" could be a title, a name, a deity or an office; the data cannot say which. It also does not settle whether the script records language. A fixed slot layout is what writing produces, but so are labels and forms.

## 1. The slot structure

Each sign used at least 15 times was given a role from where it sits, compared with a shuffle of the signs within each text:

| Role | Rule | Signs | Examples |
|---|---|---|---|
| **O** opener | starts at least 40% of its texts, and at least 1.8 times the shuffled rate | 7 | G817 starts 88% of its texts (shuffle 20%); G820 78%; G861 70%; G692 83%; G920 68% |
| **N** numeral | stroke signs, classified by shape | 11 in use | G2, G32, G33, G1, G31, G3 |
| **Q** counted item | at least 30% of its uses directly after a numeral | 12 | G220 fish 41%; G900 50%; G585 72%; G803 33% |
| **C** closer | ends at least 50% of its texts, and at least 1.8 times the shuffled rate | 12 | G740 jar ends 69% (shuffle 22%); G400 79%; G520 80%; G90 71%; G527 86% |
| **B** body | none of the above | 38 | G240, G390, G235, G60, G741 |

**The order is almost fixed.** Taking every pair of signs from two roles that occur in the same text:

| Pair of roles | First role comes first | Shuffled |
|---|---|---|
| opener, closer | 94.6% of 425 pairs | 50% |
| opener, numeral | 88.0% of 499 pairs | 50% |
| opener, counted item | 92.9% of 154 pairs | 50% |
| numeral, closer | 89.7% of 1,035 pairs | 50% |
| counted item, closer | 91.7% of 533 pairs | 50% |
| body, closer | 91.9% of 2,053 pairs | 50% |

All have p < 0.01 (200 shuffles).

**The layout:** `[opener] → [numeral + counted item] / [body] → [closer]`.

The commonest templates, with repeats collapsed, are:

| Template | Share of texts |
|---|---|
| body + closer | 6.7% |
| opener + numeral + body + closer | 2.9% |
| numeral + counted + closer | 1.1% |
| opener + numeral + counted + closer | 1.1% |

Rarer signs fill many slots, so no single template dominates.

## 2. What the common chunks do

These are the most frequent two- and three-sign chunks in the exploration split. "Texts" counts distinct texts containing the chunk.

| Chunk | Texts | Where | Objects | Apparent job |
|---|---|---|---|---|
| G861 G2 | 89 | starts 82% | seals 82% | **opening formula** |
| G817 G2 | 69 | starts 97% | seals 88% | **opening formula** |
| G820 G2 | 59 | starts 95% | seals 86% | **opening formula** |
| G920 G60 (G741) | 38 | starts 97% | seals 95% | **opening formula** (confirmed, H8) |
| G692 G60 | 21 | starts 90% | seals 95% | **opening formula** (confirmed, H8) |
| G32 G220 | 39 | middle | seals 90% | **quantity + item**: two long strokes + fish (confirmed, H6) |
| G2 G803, G2 G240, G2 G233 | 16–28 | middle | seals ~90% | **numeral + item** |
| G740 G90 | 52 | ends 87% | seals 79% | **seal closing formula** (jar + man) |
| G33 G520, G220 G520, G705 G33 G520 | 17–30 | ends 81–90% | seals ~90% | **closing formula ending G520** (confirmed, H9) |
| G760 G740, G798 G740, G390 G740, G923 G740 | 19–52 | ends 84–96% | seals ~80% | **X + jar**: the jar closes a phrase |
| G740 G400 | 60 | ends 97% | **tablets 80%** (baseline 24%) | **tablet closing formula** (G400 confirmed for Harappa tablets, H10) |
| G590 G390 (G740) | 28–42 | middle, or closing with the jar | seals 86% | fixed phrase |
| G255 G435 G690 | 17 | middle | tablets 24–36% | fixed phrase, common on tablets |

### Three functional readings stand out

1. **The closing slot tells you the kind of object.** *(Weakened by the second pass, section 6: outside G400, the middle of a text says as much about the object as the end does.)* Seals close with the jar, jar + man, or a phrase ending G520. Tablets close with jar + G400. G400 is the only common sign whose texts lean strongly to one object other than seals: 64% tablets against a 24% baseline. Like a form whose last line says what kind of document it is, the end of the text marks the genre.

2. **The "two strokes" after an opener is not counting.** *(Weakened by the second pass, section 6: G2 elsewhere is also followed by numerals, so this argument does not hold. That G2 is the stroke sign that follows openers still stands.)* Of the 386 uses of G2 that follow another sign, 57% come directly after an opener. For the other short numerals the figure is at most 14%: G1 14%, G3 2%, G4 3%, G5 0%.

   After "opener + G2", other numerals often follow (G32, G4, G31, G1, G3). A number directly followed by another number makes little sense as a count. So in this slot, G2 looks like **part of a fixed opening formula** (a marker or particle) rather than the number two. This is the clearest case of reading function overriding the obvious picture-reading. (G6 and G7 also follow openers, but they occur only 1 and 3 times.)

3. **Quantities sit in the middle.** Numeral + item pairs come after openers and before closers about 90% of the time. They read like the content of a label ("2 long strokes + fish"), framed by a fixed opening and closing.

## 3. Which claims are testable

| Claim | Status |
|---|---|
| G740 ends texts; numerals precede items; opening and closing formulas keep their slots; G400 marks tablets at Harappa | **Already confirmed** on the holdout (10 of 13 pre-registered tests supported) |
| The whole slot order: opener → numeral/item → closer | **Testable**: proposed F1, F2 |
| G2 after openers is a formula marker, not counting | **Testable**: proposed F3 |
| The closing slot marks object type beyond G400 | Partly tested (H10, Harappa only). A general version needs a closer-by-object test; not drafted |
| What openers *mean* (title, name, deity, office) | **Not testable** with sign data alone |
| Whether the script records language | **Not settled** by this kind of analysis |

## 4. Proposed pre-registered tests (not run; awaiting approval)

All three use these settings:

- data settings `{drop_damaged: true, dedupe: true, drop_unidentified: true}`;
- 2,000 permutations, seed 12345, α = 0.05;
- one-sided, minimum support 5;
- Benjamini-Hochberg correction across all confirmatory tests ever run.

Role lists are fixed from the exploration split and listed in `functional_slots.json`.

### F1. Openers come before numerals and counted items

- **Kind:** `class_order` (new).
- **first:** G861 G820 G817 G920 G692 G503 G416.
- **second:** all numerals (G1–G7, G13–G19, G27, G28, G29, G55, G31, G32, G33, G35) plus the 12 counted-item signs (G220 G803 G840 G900 G61 G575 G904 G350 G790 G226 G585 G482).
- **Null:** signs shuffled within each text.
- **Exploration:** 89.1% of 653 pairs in order, against 50.0% shuffled; p ≤ 0.0005.

### F2. Numerals and counted items come before closers

- **Kind:** `class_order`.
- **first:** the numerals and counted items listed in F1.
- **second:** G740 G400 G520 G90 G151 G405 G527 G407 G617 G154 G156 G621.
- **Exploration:** 90.4% of 1,568 pairs in order, against 50.0% shuffled; p ≤ 0.0005.

### F3. G2 is the stroke sign that follows openers

- **Kind:** `pair_share` with `side: preceding` (new).
- **Members:** short numerals G1–G7.
- **Subset:** G2.
- **Targets:** the seven openers.
- **Statistic:** G2's share among short numerals that come directly after an opener, minus its share among those that come after other signs.
- **Exploration:** +37.6 points, with 220 supporting pairs; p ≤ 0.0005.

**Caveats.**
- **F1 and F2 overlap with results already confirmed.** Openers were picked for starting texts and closers for ending them, so part of each test re-checks that. The new information is that numerals and counted items, picked without regard to position, fall between them.
- **F3 is the most novel** of the three. If it holds, it supports reading G2 in this slot as a formula element rather than a count.
- **These are ordinary multiple comparisons.** Three more tests raise the correction family from 13 to 16.

## 5. Code added

- **`scripts/functional_slots.py`:** the exploratory analysis. It reads the exploration split only.
- **New test kind `class_order`** in `indus_workbench/hypotheses.py`.
- **`pair_share` test kind with a `side` option.** It also lives on the Parpola branch without `side`; the two versions need reconciling when that branch is merged.
- **Synthetic tests in `tests/test_core.py`.** Each new kind finds a planted pattern, and `class_order` ignores free order. All 42 tests pass.

## 6. Second pass (exploratory, 14 October, evening)

*Exploration split only. Script `scripts/functional_deeper.py`; output in `functional_deeper_output.txt` and `functional_deeper.json`. Nothing was registered and the holdout was not read.*

### 6.1 The layout holds for whole texts, and the roles are stable

- **Whole texts follow the order.** In 80.1% of the 1,160 texts that use signs from at least two slots, every role-assigned sign follows the order opener → middle → closer. Shuffling the signs within each text gives 22.1%, and none of 200 shuffles reached 27%.
- **Roles are stable across halves.** The exploration texts were split at random into two halves, and roles were assigned on each half separately:
  - 35 of 41 signs got the same role in both halves;
  - closers agreed completely (8 of 8);
  - openers agreed 4 of 5 or 6, and counted items 5 of 5 to 9.
  - Roles learned on one half put 79.0% of the other half's texts in order.
- **The middle is not just numeral + counted item.** After a numeral comes:

| What follows a numeral | Share |
|---|---|
| a body sign | 32% |
| a counted-item sign | 19% |
| a rarer, unassigned sign | 19% |
| another numeral | 16% |
| a closer | 12% |

The middle is better described as "content, which often includes numeral + item" than as a strict numeral-then-item slot.

### 6.2 The "two strokes" clue: partly withdrawn

- **What still holds.** G2 is overwhelmingly the stroke sign that comes right after an opener: 56% of its uses, against at most 18% for any other numeral. This is proposed test F3.
- **What does not hold.** The argument that G2 is "not counting" there because another numeral follows it fails. G2 after an opener is followed by a numeral 28% of the time, and G2 elsewhere 21%. The two kinds of G2 lead into the same mix of signs (Jensen-Shannon divergence 0.252 against 0.265 for shuffled labels; p = 0.74). Numeral followed by numeral is also common in general: G1 22%, G31 22%, G13 21%. That fits compound numbers such as "2 + 3" as well as it fits a formula.
- **Revised reading.** "Opener + G2" is a fixed opening construction. Whether G2 there means "two" or is a marker cannot be told from these statistics.

**Other fixed pairs (a sign tied to one particular sign before it):**

| Pair | How fixed | Note |
|---|---|---|
| G740 → G90 (jar → man) | 74% of G90's uses | the seal closing formula |
| G255 → G435 | 83% of G435's uses | |
| G435 → G690 | 45% of G690's uses | together with the pair above, the phrase G255 G435 G690 |
| G550 → G527 | 42% of G527's uses | a closer |

These are formula pieces: one sign predicts the next. None is followed by numerals more than 7% of the time, so none looks like a counting hinge.

### 6.3 Does the closer tell you the object? Only G400 clearly does

"Excess" below is the information each sign carries about seal versus tablet, over what shuffled labels give:

| Sign used | Excess information about seal vs tablet | p |
|---|---|---|
| first sign | 0.075 bits | 0.002 |
| middle sign | 0.118 bits | 0.002 |
| last sign | 0.122 bits | 0.002 |
| last sign, texts ending G400 removed | 0.067 bits | 0.002 |
| same, within Harappa only | 0.058 bits | 0.004 |
| same, within Mohenjo-daro only | 0.047 bits | 0.002 |

- **The last sign is no better than the middle sign.** Seals and tablets use somewhat different signs throughout the text, not just at the end.
- **Only G400 is a strong tablet closer.** It ends texts that are 71% tablets, against a 25% baseline. The next strongest are G617 at 40% (20 texts) and G407 at 32% (22 texts), both weak.
- **Revised reading.** G400 marks tablets (already confirmed for Harappa, H10). The broader claim that "the closing slot marks the genre" is not supported.

### 6.4 What is now worth a future pre-registered test

| Candidate | Exploratory strength | Recommendation |
|---|---|---|
| **Whole-text slot order** (new; replaces F1 and F2) | 80% in order against 22% shuffled; stable across halves | **Strongest.** One test covers the whole layout, with roles frozen from the exploration split. Needs a small new test kind (`template_order`). |
| F3: G2 is the stroke sign after openers | +37.6 points | Still strong as a fact; interpret only as "a fixed opening construction" |
| Fixed formula pairs (G740→G90, G255→G435→G690, G550→G527) | 42–83% attachment | Largely covered by the already-confirmed unit recurrence (H7) |
| Closer marks object type, beyond G400 | Last sign no better than the middle | **Drop** |

The holdout was not touched in this pass.
