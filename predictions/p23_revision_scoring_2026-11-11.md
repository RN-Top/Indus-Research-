# P23 revision 1: scoring instead of first-match (11 Nov 2026)

Reason: the synthetic control (results/synthetic_control_P23_2026-11-11.md) failed the per-base threshold under noise for decimal (0.68) and quinary (0.46). The first-match rule breaks when one defining form is a variant.

Revision: each base is scored by the fraction of its defining relations that hold. The defining relations are the ones used in steps 1-4 of the original rule. Predicted base = highest score, if that score is at least 0.75 and the score of the next base is lower. Otherwise "other".

Defining relations:
- vigesimal: 20 is one morpheme, not 2x10; 10 is a single root.
- decimal: 10 single root; 20 = [2, 10]; 100 single root; 11-19 = [10, n] (teen rule).
- quinary: 5 single root; 6-9 = [5, n]; 10 = [2, 5]; 20 = [4, 5] or [2, 10-as-2x5].
- duodecimal: 12 single root; 10 and 11 distinct single roots.

Pre-registered thresholds: clean accuracy >= 0.95 overall; noisy (10% variant forms) mean accuracy >= 0.80 and per-base >= 0.90.

Validation: the first seed (20261111) is no longer fresh, since it informed this revision. The revision is tested on seed 20261112. Its results count as the validation. The first seed is reported as a tuning run only.

This revision is logged before any real numeral is coded. The original rule stays in place for the record.
