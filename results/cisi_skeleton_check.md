# Does the slot order survive in an independent transcription? (CISI check)

*Exploratory. 15 October 2026. Script `scripts/cisi_skeleton_check.py`; numbers in `cisi_skeleton_check.json`. Nothing registered. Holdout protected twice: CISI seals in CISI's own holdout split were dropped, and so was any seal whose CISI number matches a text in the main corpus's holdout.*

## What was done

- **Roles:** the frozen role lists from `drafts/H-skeleton-transfer.DRAFT.json` (learned from Mohenjo-daro exploration texts in the main corpus) were translated into CISI's own sign numbers through the confident G→P crosswalk.
- **Mapped:** 6 of 9 openers and 5 of 8 closers.
- **Not mapped (no confident crosswalk entry):** openers G575 and G920; closers G407, G527 and G617.
- **Data:** the CISI transcription (Parpola's corpus volumes, via the bundled allograph file) of Mohenjo-daro seals, with damaged seals and unidentified signs removed, and both holdouts excluded. That leaves 62 seals, of which 46 have role signs from at least two slots.

## Result

| | Seals in slot order |
|---|---|
| CISI transcription | **80.4%** of 46 |
| Same seals, signs shuffled within each seal (2,000 runs) | 23.6% (95th percentile 32.6%) |
| p | 0.0005 |

The main corpus gave 76–83% for comparable sets of texts, so an independent scholarly transcription, with its own sign numbering, reproduces the slot order at the same strength.

## What this does and does not show

- **Shows:** the opener → content → closer order is not an artefact of one website's transcription or sign numbering. Another transcriber, working from the objects independently, records the same order.
- **Does not show:** that the order holds on new objects. These are Mohenjo-daro seals, the same site, and many of the same physical seals, that the roles were learned from. This checks the **transcription**, not generalisation to other sites (that is what the drafted holdout test is for).
- **Small sample:** 46 scorable seals; 5 role signs could not be mapped.
- **Prior work:** the slot structure itself was described before by Wells and Fuls (initial signs, the initial cluster terminal marker on sign 2, and terminal markers such as 740, 520 and 400; see the ICIT documentation). This check adds statistical confirmation against a shuffle and across transcriptions; it does not claim the structure as a new discovery.
