# The frame-breaking "complex" texts (Fuls's ~13%): scouting (EXPLORATION, not a registered test)

*16 October 2026. Exploration split only (damaged dropped, duplicates removed, unidentified signs dropped). The holdout was not read, and nothing was tested or registered. Script: `scripts/complex_texts.py`. Numbers: `complex_texts.json`. Printout: `complex_texts_output.txt`.*

**Caveat up front: much of this may be the statistical tail of the corpus, not a hidden grammar.** The definition also leans the results in one direction, as explained below.

## The question

Andreas Fuls (email, 16 October 2026) points out that about 13% of complex Indus texts show no sign pattern: their sign pairs occur only once or twice in the corpus. No "slot" theory (heading, middle, closer) explains them. Do these texts have an order of their own that the frame misses?

**Definition used here:** a text of 3 or more signs in which every adjacent sign pair occurs at most twice in the exploration corpus. That gives **153 of 1,294 texts (12%)**, matching Fuls's figure.

**Comparisons:**
- all 1,141 ordinary texts of 3 or more signs;
- a sample of 153 ordinary texts **matched for length**.

## 1. Who they are

| | Complex (153) | Ordinary, length-matched (153) | All ordinary (1,141) |
|---|---|---|---|
| Length, median (mean) | 3 (3.8) | 3 (3.8) | 5 (5.3) |
| Seals | 65% | 65% | 74% |
| Tablets | 24% | 28% | 22% |
| Pottery | **4.6%** | 2.6% | 1.1% |
| Mohenjo-daro | 50% | 45% | 55% |
| Harappa | 33% | 41% | 31% |

- **They are short and spread everywhere.** Once length is matched, the mix of objects and sites is close to that of ordinary texts. Pottery is a little more common (7 texts against 4).
- **They are not a separate site or object class.**

## 2. Do they have the normal frame?

| | Complex | Ordinary, length-matched | All ordinary |
|---|---|---|---|
| Starts with an opener | **5%** | 20% | 30% |
| Ends with a closer | **38%** | 73% | 74% |
| Both | 3% | 12% | 22% |
| Has a numeral | 38% | 49% | 64% |
| Signs used 5 times or fewer in the corpus | **25%** | 6% | 7% |
| Median frequency of their signs | 34 | 75 | 89 |

- **Mostly they lack the frame,** and **they are built from much rarer signs.** A quarter of their signs are used 5 times or fewer in the whole corpus.
- **The definition partly causes this.** Openers and closers are common signs that form common pairs (opener + G2, item + G740). Any text containing such a pair cannot count as "complex". So "complex texts lack the frame" is partly built in.

## 3. Their own signs

**Over-represented** (rate in complex texts against ordinary; signs used 5 or more times in complex texts):

| Sign | In complex texts | In ordinary texts | Ratio |
|---|---|---|---|
| G892 | 8 | 15 | ×5.3 |
| G595 | 8 | 16 | ×5.0 |
| G717 | 6 | 20 | ×3.0 |
| G55 (twelve stacked strokes) | 7 | 24 | ×2.9 |
| G125 | 7 | 30 | ×2.4 |
| G405 | 6 | 27 | ×2.2 |
| **G400** (the Harappa tablet closer) | **23** | 129 | ×1.8 |

**Nearly only in complex texts:** just two signs, each on 3 texts: G18 (3 against 1) and G150 (3 against 0). There is **no special sign set**.

**Absent or nearly absent:** the common opener G817 and the end-of-middle signs G760 and G100 (0–1 uses), plus the item signs G240, G231, G233 and G806. This again reflects the definition: these signs belong to frequent pairs.

## 4. Their own order?

Order was checked at the level of **sign classes**, using the classes from `open_patterns.py`. Only signs common enough to have a class were used.

| | Perplexity, real order | Perplexity, signs shuffled within each text | Gain from real order |
|---|---|---|---|
| Ordinary texts (held-out half) | **6.3** | 12.6 | large (2 times) |
| Complex texts | **15.5** | 17.1 | small (1.1 times) |

Perplexity is roughly how many equally likely options a model is choosing among, so lower is better. The model was a class-to-class bigram model fitted on the other half of the ordinary texts.

- **Ordinary texts follow a strong class-level order.** **Complex texts barely do.** Their class sequences are only a little more predictable than the same signs in random order.
- **Reference:** if every text's signs were shuffled, **23%** of texts would count as "complex", not 12%. The real corpus is far *more* patterned than chance. The complex texts are the part where that patterning is weakest.

There are too few complex texts (153, most only 3 signs long) to fit a separate order model on them alone. "Their own grammar" could not be tested.

## 5. What are they? Weighing the options

| Explanation | For | Against |
|---|---|---|
| **(d) The statistical tail** | Short texts built from rare signs. Spread over all sites and objects. No special signs. Shuffling the corpus doubles the share of such texts. | None strong |
| **(b) Damaged, garbled or unusual objects** | A little more pottery. Rare signs could include misreadings or variants. | Damaged texts were already dropped. Most are ordinary seals and tablets. |
| **(a) A different genre or content** | They lack the frame and favour a few signs (G892, G595, G717, G55, G400). | The over-represented signs rest on 6–23 uses each. Nothing appears only in them. |
| **(c) A different notation** | Weak class-level order. | Their order is only slightly above random, which is what noise looks like too. No positive pattern of their own was found. |

**Overall:** mostly (d), the tail. They are short texts with rare signs and without the formulaic frame. There are small hints of (a): G400, the twelve-stroke sign G55, and a few rare signs turn up more than expected. **No hidden grammar of their own was found,** though with 153 mostly three-sign texts, one could not have been detected even if it existed.

## For Fuls's point

He is right that a slot theory does not explain these texts. The data adds two things:
- They are **not a coherent second system**, as far as can be seen here.
- They look like the **rare-sign, frame-less edge** of the same script.

The real question they raise is **what the rare signs are**: personal or place names, variants, scribal idiosyncrasies or transcription choices. Statistics on this corpus cannot settle that.

## Worth registering later?

**Nothing clean yet.** The obvious claims (complex texts lack the frame; complex texts lack class order) are partly built into the definition.

**Two better next steps:**
1. **Check the 153 against an independent transcription** (CISI where it overlaps, which is mainly Mohenjo-daro). If many "rare" signs are read as common signs there, part of the 13% is a transcription effect. That is a real, checkable claim.
2. **Read Wells 1998 on these texts.** Fuls attached the thesis, and its Figure 4.6 and column analysis may already classify some of them.

The one possibly testable lead: **G400 and G55 are over-represented in frame-less texts**. The holdout support would be only about 6 and 2, which is too few.
