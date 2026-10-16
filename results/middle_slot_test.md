# The end-of-middle slot: pre-registered test

*16 October 2026. Registered in commit `7ec7cd2` (`hypotheses/H-2026-10-16-a6cd844c.json`) before running. Run once on the locked Indus holdout with `scripts/run_confirmatory.py`. Raw output: `confirmatory_2026-10-16.json`. The lead came from `middle_flow_scouting.md`.*

## The claim

An inscription reads **[heading] + [middle] + [closer]**. Inside the middle, four signs (**G100, G760, G142, G923**) take the **last** place, immediately before the closer. They do this far more often than chance. In exploration they did so 94.5% of the time, against 31% when each middle's signs are shuffled.

## How it was tested

- **New hypothesis kind:** `middle_final_slot`, added to `indus_workbench/hypotheses.py`. It has a positive control, a negative control, a false-positive-rate check and a middle-extraction check in `tests/test_core.py`; all tests pass.
- **The middle:**
  - remove the leading openers, plus G2 or G60 right after them;
  - remove the trailing closers;
  - roles come from the frozen rule on all exploration texts;
  - only texts that end in a closer and have a middle of 2 or more signs are scored.
- **Statistic and null:** the share of the four signs' occurrences that are last in the middle. Null: each middle's signs shuffled, 2,000 times.
- **One change from the request:** a heading was **not** required. Requiring one would have left about 12 holdout occurrences, below the project's minimum support of 15. The registration states this choice and its reason.

## Result

| | Holdout |
|---|---|
| Occurrences of the four signs in scored middles (support) | **31** |
| Last in the middle | **90.3%** |
| Expected with each middle shuffled | 32.3% |
| p | 0.0005 (the minimum with 2,000 shuffles) |
| q (BH across all 18 confirmatory tests) | 0.0006 |
| **Verdict** | **Supported** |

**Running total: 18 pre-registered tests; 15 supported, 3 not supported.**

## What it means

- **The middle has a fixed final slot.** On inscriptions never used to find it, these four signs sit right before the closing sign nine times out of ten.
- **Inscription structure now confirmed on unseen texts:**
  - heading;
  - middle, ending in a fixed final slot;
  - closer (generic G740, or specific marks such as G407/G617 on copper tablets).
- **In the function reading,** this slot is where a Mesopotamian seal would put a title or relation ("son of …", "the scribe") before "your servant". That is an analogy, not a meaning.
- **Credit:** Wells and Fuls describe "late-medial" sign classes, and `content_grammar.md` noticed these signs. This test confirms the slot statistically; it did not discover it.

## Limits

- **Order, not cause.** This shows *where* the signs sit, not *why*. What makes them sit there ("the force") is the next question. One way to probe it: test whether the slot rule extends to signs it was not built on (grammar), or holds only for these exact signs (fixed phrases).
- **31 occurrences**, in one transcription (ICIT-derived).
- **Not evidence of language.** Fixed slots also occur in non-linguistic sign systems (Raghavendra 2026).
