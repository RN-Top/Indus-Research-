# Do complex texts spell syllables? A calibrated test of Wells's suggestion (scouting, exploration only)

*21 October 2026. Scripts: `scripts/syllable_test/` (paths point to the scratch copies of the paragorth codelib and the ICIT export; neither is copied here). Wells (2006, p. 145) suggested complex texts may be "syllabic spellings". Not a confirmatory test.*

## Calibration on a known mixed script (Linear B)

Linear B lines (DAMOS via paragorth `codelib`, 13,170 lines) were split into individual signs: syllabograms (from spelled words), logograms (OLE, VIR, GRA, …) and numbers. Per sign (10+ uses), features were measured after removing the effect of frequency. How well each separates syllabograms (87) from logograms (73):

| Feature | AUC |
|---|---|
| Diversity of the following sign (entropy) | **0.86** |
| Distinct right neighbours | **0.85** |
| Share of uses next to a number | **0.10** (i.e. 0.90 the other way: logograms sit next to numbers) |
| Diversity of the preceding sign; positional entropy; interior share | 0.35–0.47 (not used) |

## Indus

A logistic model on the three calibrated features (fitted on Linear B, features standardized within each corpus) gives each Indus sign a "syllable-likeness". Enrichment = log ratio of a sign's share in Wells's complex texts (SC, LC) vs patterned texts (SP, LP), exploration split.

- 90 signs with 10+ uses; 345 complex and 293 patterned texts.
- Spearman(enrichment in complex texts, syllable-likeness) = **−0.03** (texts' class labels shuffled: 0.00; one-sided p 0.61). Each feature separately: |ρ| ≤ 0.11.
- **No support** for complex texts being written with more syllable-like signs than patterned texts.

**Limits.** One calibration script only (Ur III legends could not be labelled reliably sign by sign); Linear B's logograms sit next to numbers because of its accounting format, so the number feature may not transfer; syllable-likeness of a sign type is a coarse lens on whether a *text* is a spelling. A negative here does not refute Wells's suggestion; it means this calibrated lens finds nothing to support it.
