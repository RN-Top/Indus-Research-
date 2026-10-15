# Is there grammar inside the content slot?

*Exploratory. 14–15 October 2026. Exploration split only: 1,523 distinct texts. Nothing registered; the holdout was not read. Script `scripts/content_grammar.py`; output in `content_grammar_output.txt` and `content_grammar.json`.*

## The question

`functional_meaning.md` found that inscriptions read as **[fixed heading] + [individual content] + [category ending]**, and left open whether the content is language or a list of names and labels. A language that adds endings to words (cat / cats / cat's) leaves a fingerprint at the edge of words:

- **A small closed set of endings** ends most units.
- **The same stem appears with different endings.**

A list of fixed names leaves the opposite fingerprint: each name is one fixed string, so its last sign is fixed by what comes before it.

## Method

- **Content unit:** what is left of a text after removing its openers and closers. Roles come from the rule in `functional_by_site.md` D.1.
- **Ending:** the last sign of the unit. **Stem:** everything before it. The same measures were also taken at the start (prefixes).
- **Four systems compared:**
  - the real content;
  - the real content with signs shuffled inside each unit;
  - a synthetic **list of names** (whole sign strings, re-used with Zipf frequencies);
  - a synthetic **language with endings** (stems plus one of 6 endings).
  - The synthetic systems use the same sign inventory, number of units and length profile as the real content, and each is averaged over 20 runs.
- **Measures:**
  - **Top-5 share:** share of units ending in the 5 commonest end signs.
  - **Freedom:** H(ending | stem) / H(ending), over stems used 3 or more times. Near 0 means the ending is fixed by the stem (names); near 1 means any stem takes any ending (productive endings).
  - **Stems with 2+ endings:** share of recurring stems seen with more than one ending.

## Results: last sign of the content (numerals kept)

| System | Different end signs | Top-5 share | Freedom | Stems with 2+ endings |
|---|---|---|---|---|
| **Real content** | 262 | **22%** | **0.43** | **90%** |
| Real, shuffled inside units | 274 | 21% | 0.41 | 98% |
| Synthetic list of names | 281 | 33% | 0.01 | 9% |
| Synthetic language with endings | 6 | 93% | 0.85 | 97% |

With numerals removed, the results are nearly identical: real top-5 share 22%, freedom 0.42. The first sign of the content (prefixes) gives a similar pattern: real 30% / 0.37, against shuffled 21% / 0.41.

## What it shows

1. **No closed set of endings.** In the real content, the five commonest last signs cover only 22% of units, against 93% in the language-with-endings model. Whatever the content is, it does not end in a small paradigm of grammatical suffixes.
2. **Not fixed name strings either.** When a stem recurs, it appears with different last signs 90% of the time. In the list-of-names model it is 9%. The content is **built by combining signs**, not by repeating stock strings. That fits the earlier finding that 86% of content units are unique.
3. **At its edges, the content looks like its own signs in shuffled order.** On these measures, real and shuffled content are close. The edges of the content carry little ordering information beyond which signs are present. Order does matter inside texts overall (confirmed results; the bigram model). The structure is in the slots and fixed pairs, not in endings.
4. **A few signs do behave like endings.** These attach to many different stems and rarely appear anywhere else:

| Sign | Ends a content unit | After how many different stems | Used inside a unit |
|---|---|---|---|
| G760 | 50 | 49 | 7 |
| G100 | 55 | 48 | 9 |
| G142 | 23 | 21 | 6 |
| G390 | 97 | 84 | 49 |

Several sit just before the jar closer: G760 + G740, G100 + G740 and G390 + G740 are among the commonest chunks. They could be grammatical endings, classifier-like markers ("…of the type X"), or part of the closing formula. These statistics cannot tell which.

## Verdict

The content slot is **compositional**: individual combinations from a large sign inventory. It has neither a closed set of endings nor fixed repeated strings, plus a small group of suffix-like signs that come just before the closer. That is compatible with:

- **naming formulas** built from parts, like "son of X", a title plus a place, or a clan plus a personal element;
- **language** written with little grammar, as many early scripts do (word endings are often left unwritten).

It argues **against** two simpler pictures: a script that writes suffix-heavy sentences in full, and a fixed inventory of whole names. Language versus label stays open, but the target has narrowed: the most suffix-like signs (G760, G100, G142, G390) are where to look next.

## Limits

- **Word boundaries are unknown.** The "content unit" may hold several words, so its last sign is a word ending only for the last word.
- **The synthetic systems are deliberately simple caricatures**, meant to show what each extreme looks like, not to model any real language.
- **Freedom is measured on few recurring stems** (about 50), because most content is unique.
- **Exploration only:** none of this has been tested on the holdout.

## Possible next steps (not done)

- Profile the four suffix-like signs: what they follow, what objects and sites they occur on, and whether they swap with each other in otherwise identical texts. Swapping like that is the paradigm test.
- Run the same measures on a real comparison corpus of short seal legends in a known script.
