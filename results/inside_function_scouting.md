# "The inside is the function": two checks (scouting, exploration only)

*22 October 2026. Erin's idea: an inside mark or an enclosed sign tells what the thing does, as in Sumerian cuneiform, where a sign written inside the mouth sign gives the action (mouth + water = drink, mouth + bread = eat).*

## 1. Composites with a whole sign inside: cannot be tested

The blind annotation lists the composites where a recognisable sign is enclosed or joined: G859 (diamond G850 with the A-sign G465 inside), G751 (jar with a wheel and comb in the mouth), G117, G119, G111, G944 and other human ligatures. In the exploration split **each occurs once**, apart from G111 (7 uses). Their neighbours cannot be compared with those of the enclosed sign. The idea is not refuted, only untestable on this corpus size. These signs are rare everywhere (they are among the ~13% "complex" signs).

## 2. Do inside marks change the kind of partner?

*Script: `scripts/inside_partners_scouting.py`; output `inside_partners_scouting_output.txt` (and `_nofish_` without the fish family). 96 inner-only pairs, 869 marked tokens. Per pair: marked share minus plain share, weighted; null: labels permuted within pairs.*

| Partner | All pairs | Without fish |
|---|---|---|
| Numeral right before | −6.3 points (p 0.049) | −3.4 (p 0.28) |
| Numeral right after | +6.9 (p 0.73) | +8.9 (p 0.65) |
| Heading right before | −0.6 (p 0.13) | −0.4 (p 0.40) |
| Closer right after | −0.1 (p 0.98) | +1.8 (p 0.74) |

**Reading.** No reliable change. The one borderline result (fewer numerals before inside-marked signs) comes from the fish: the plain fish G220 is the commonest counted item, and its inside-marked forms (G231, G233) are counted less often. Without the fish it disappears; with four features checked it would not survive correction anyway.

**What this leaves.** For the fish only, an inside mark may turn "a fish that is counted" into something that is not counted, which would fit "the inside gives a use or kind". That is one family and descriptive; it is a lead for the new-data set, not a result.
