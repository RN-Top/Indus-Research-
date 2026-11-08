# ICIT plate check: status (6 Nov 2026, local, not committed)

Prediction: `predictions/icit_plate_check_P18_2026-11-06.json`
sha256: 5876d132b93efd1ab8bf8a224af952c5548802c4705deada0ad63493fb403e5f
Written and hashed before any seal from plate LXXXII was read.

## Status: blocked before any reading

- The merged ICIT corpus (`data/icit_merged_paragorth/merged-corpus-canonical.json`) has 1,341 Mohenjo-daro seal objects, but no field that records a Mackay plate number or seal number. Fields are `cisi`, `site`, `type`, `area-section`, `block-house`, `room-grid`, `seq` and related sequence fields.
- The prediction's matching step (seal 687-704 to an ICIT object by site, area and seal number) therefore can't be done as written. Any match would be a guess.
- No seal from plate LXXXII has been read or compared.

## What this means

The test as designed would have compared zero or very few seals, so it would not measure transcription error. I'm not changing the prediction after the fact. Options, to be decided before any reading:

1. Match by `area-section` and sign sequence, and report the match rule as part of the test. Risk: a match chosen by sequence makes agreement close to circular.
2. Compare plate LXXXII seals to ICIT by area only (DK vs SD, upper levels) and report it as an exploratory count, not as a pre-registered check.
3. Find a separate ICIT or CISI catalogue with Mackay numbers, if one exists, and state its licence first.

Recommendation: option 3 if a catalogue is found. Otherwise option 2, labelled exploratory, with P18 marked as not run.
