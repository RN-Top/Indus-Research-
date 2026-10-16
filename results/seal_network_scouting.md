# Seals as a network: do names stay home, and which cities are linked? (EXPLORATION, not a registered test)

*16 October 2026. Exploration split only. The holdout was not read, and nothing was tested or registered. Script: `scripts/seal_network.py`. Numbers: `seal_network.json`. Printout: `seal_network_output.txt`. This starts the "seals as a social and economic network" direction in `field_approaches_and_gaps.md`.*

**Caveats up front:**
- Rare signs are used only 2–5 times, so every rarity figure here rests on tiny counts.
- Site attribution comes from the ICIT-derived corpus and is imperfect.
- Two cities (Mohenjo-daro and Harappa) hold 84% of the texts.

## A. Do name-like rare signs stay at home?

**Method.** For each sign found in 2–5 texts, two things were measured: whether all its texts come from one site, and the share at its commonest site. Both were compared with random placement of the same number of texts across the corpus, which respects how big each site is.

| Group | Signs | All at one site | Random would give | Excess |
|---|---|---|---|---|
| Rare signs used in a name-like slot | 116 | 32% | 23% | **+9 points** |
| Other rare signs | 48 | 27% | 25% | +2 |
| Common signs (same number of texts drawn at random) | 268 | 21% | 16% | +5 |
| **Seals only**, name-slot rare signs | 85 | 34% | 34% | **0** |

- **Not supported, on seals.**
  - Across all objects, name-slot rare signs are a little more local than chance.
  - On **seals alone, where owners' names would be, the excess vanishes.**
  - So the excess comes from tablets, which matches the Harappa tablet series seen in `name_inventory_scouting.md`, not from seal "names".
- **How weak this is by nature:** with 2–5 texts per sign, even a real "local names" effect of 10 points could easily hide in the noise.

**But one comparison points the same way at the level of whole cities (B below):** Mohenjo-daro and Harappa share **fewer** rare signs than random mixing of their texts predicts (65 against 85). Rare signs tend to belong to one big city or the other. That is "rare signs stay home" between the two big cities, though the seal-level test above could not see it.

## B. Cities as nodes

- **Nodes:** sites with 10 or more texts, plus the 14 texts found abroad pooled as one node ("Abroad": West Asia, the Gulf, Central Asia).
- **Links:** for every pair, the number of sign types they share, all and rare-only, against 1,000 shuffles of which site each text came from (each site keeps its number of texts).

**Overall pattern.** Almost every pair shares **fewer** signs than shuffling predicts (for example, Harappa–Mohenjo-daro 215 shared against 243). Each city has a somewhat distinctive working vocabulary on top of the common script. That fits **one shared script with local usage**.

**Standout links carried by rare signs:**

| Pair | Shared rare signs | Expected | One-sided p | Which signs |
|---|---|---|---|---|
| **Abroad — Mohenjo-daro** | **8** | 3.3 | 0.02 | G127, G150, G160, G278, G285, G319, G426, G924 |
| Dholavira — Mohenjo-daro | 14 | 11.3 | 0.24 | |
| Kalibangan — Mohenjo-daro | 9 | 7.3 | 0.30 | |
| Harappa — Mohenjo-daro | 65 | 84.8 | (fewer than expected) | |

- **The one standout is Abroad ↔ Mohenjo-daro.** The inscriptions found abroad share rare signs with Mohenjo-daro more than twice as often as their numbers predict. They do **not** do so with Harappa (3 against 2.5).
- Mohenjo-daro is on the lower Indus, the end of the sea route to the Gulf (`findspots_waterways.md`). That is consistent with the overseas seals coming from, or through, the Sindh end of the civilisation rather than the Punjab end.
- **Weakness:** p = 0.02 is one of 28 pairs, so it would not survive correction for multiple tests. It also rests on 14 abroad texts.

### Signs that bridge distant places

| Sign | Uses | Where | Share abroad |
|---|---|---|---|
| **G91** | 9 | Karzakan (Bahrain) ×2, Saar (Bahrain), Luristan, Harappa ×2, Kalibangan, Dholavira, Mohenjo-daro | **4 of 9** |
| **G55** ("twelve") | 33 | mostly Mohenjo-daro and Harappa, plus Qala'at al-Bahrain, Saar and Susa | 3 of 33 |
| **G93** | 7 | Mohenjo-daro ×3, Dholavira, Kalibangan, plus Ur and Saar | 2 of 7 |
| **G924** | 4 | Harappa, Mohenjo-daro, plus **Susa** and **Ur** | 2 of 4 |
| **G426** | 4 | Harappa, Mohenjo-daro, Banawali, plus **Shortughai** (Afghanistan) | 1 of 4 |

Texts found abroad are only about 1% of the corpus, so these shares are striking. **G91 in particular looks like a "Gulf" sign:** nearly half its uses are on seals from Bahrain and Iran. This fits Laursen's observation that Gulf-type seals use unusual sign combinations.

## Synthesis

**What the emerging network looks like:**
- **One shared script everywhere,** with each city using a somewhat distinctive set of signs on top of it. Pairs of cities share fewer signs than random mixing would give.
- **Rare signs mostly stay with one of the two big cities,** but on seals the "names stay home" test showed nothing at the level of individual signs.
- **The overseas inscriptions link to Mohenjo-daro, not Harappa,** through rare signs. A handful of signs, especially **G91**, **G924**, **G93** and the twelve-stroke **G55**, recur on seals found in the Gulf and Mesopotamia.

**What is probably noise:**
- every link except Abroad ↔ Mohenjo-daro;
- the overall "names stay home" excess, which disappears on seals;
- any single bridging sign. G924 and G426 rest on 4 uses each.

## Worth registering later

1. **Abroad signs (the strongest candidate).**
   - Claim: in the holdout, signs from a frozen "abroad-linked" list (G91, G93, G924, G55) occur more often on texts found abroad than their overall frequency predicts.
   - **Problem:** the holdout has only 2 texts found abroad (`foreign_seals_scoping.md`). Not testable until the abroad sample is enlarged, for example from Laursen 2010.
2. **Big-city rare-sign separation.**
   - Claim: rare signs are shared between Mohenjo-daro and Harappa less often than random mixing predicts.
   - Expected holdout support: about 13 shared rare signs at 20% of the exploration figure, against about 17 expected. That gap is too small for good power. Better tested with a second transcription.

Neither is ready to register.
