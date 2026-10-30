# Pottery inscriptions carry the writing without the seal formula (scouting, descriptive)

*30 October 2026. Script `scripts/pottery_vs_seals_scouting.py`, output `pottery_vs_seals_scouting_output.txt`.*

**Data.** The merged ICIT corpus (paragorth, MIT) holds **543 pottery inscriptions**, 271 of them with 2 or more signs. The project corpus has only 59. Groups:
- `POT:T:g`: scratched graffiti, 226 multi-sign.
- `POT:T:s`: stamped, 39 multi-sign.

**Prompt.** Nath (2014, Rakhigarhi report, p. 221) suggests that marks scratched after firing on pot bellies "may be the owner's name". Vinod (2023) finds numerals and chevrons dominate the Dholavira graffiti.

**Length-matched comparison.** "Closer" means one of the five commonest seal-final signs: G90, G390, G400, G520, G740.

| | Graffiti | Seals | Fisher p |
|---|---|---|---|
| 2 signs: ends in a seal closer | 28% (35/124) | 41% (166/408) | 0.015 |
| 3 signs: ends in a seal closer | 35% (24/69) | 49% (181/373) | 0.037 |
| Numeral tokens, 2 signs | 35% | 16% | |
| Numeral tokens, 3 signs | 27% | 16% | |
| Graffiti sign types also used on seals | 88% | | |

**Reading.**
- Graffiti on pots use the **same sign inventory** as seals: 88% of their sign types also occur on seals. So this is the same writing system, not a separate potters' code.
- But they use the **seal formula less** and **numbers about twice as often**.
- That fits a short owner or user mark plus counts or measures, without the administrative formula that ends seal texts.
- It also fits the Lothal result, where the seal text marks *who*, and the stamp-vs-scratch split: pre-firing marks come from the potter, post-firing marks from the owner.

**Status.** Descriptive only. All existing pottery has now been looked at, so the claim is sealed as prediction **P15** (`predictions/new_finds_P15_pottery_graffiti_2026-10-30.json`). It is to be tested only on new graffiti, such as Dholavira (Vinod) or Rakhigarhi (ASI), once 20 or more multi-sign texts are transcribed.

**Limits.**
- Pottery reading direction is less certain than for seals.
- The meaning of `POT:T:p` is not confirmed.
- Harappa contributes about half of the pottery texts.
