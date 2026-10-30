# Prior-work check: copper-tablet minimal pairs and the elephant formula

*30 Oct 2026. This checks `copper_minimal_pairs.md` and `elephant_sign_paradigm.md` against published work. Method: WebSearch (standard and extended) and WebFetch. Quotes are verbatim as WebFetch returned them. Fetch output is extracted by a model, so check every quote against the original before citing it.*

Markers:
- **[V]** I read the source here; the URL and quote are given.
- **[U]** Not verified here.
- **[R]** Taken from an earlier project note, not re-read today.

---

## Sources I could NOT read (most likely places for anticipation)

**Parpola 2008, "Copper tablets from Mohenjo-daro and the study of the Indus script"**
- In Olijdam & Spoor (eds), BAR IS 1826, pp. 132–139.
- The record is [V] at https://researchportal.helsinki.fi/en/publications/copper-tablets-from-mohenjo-daro-and-the-study-of-the-indus-scrip/
- The PDF failed twice (client_error): https://researchportal.helsinki.fi/files/127257447/Parpola_A_2008._Copper_tablets_from_Mohenjo_daro._ECL_During_Caspers_Vol.pdf
- **Erin has a copy (see [R] below). Check it by eye first.**

**Parpola 1994, *Deciphering the Indus Script*, pp. 108–112 and 234**
- Archive.org lists OCR full text for two uploads (`decipheringtheindusscriptaskoparpola_711_R`, `..._bookmarked_300_F`).
- The text and PDF links were blocked by the fetch allowlist, so I read nothing.

**Not read for other reasons**
- **Ganesan et al. 2009** (rmrl.in): blocked today. The quotes below come from the 20 Oct check.
- **Mukhopadhyay 2019**, *Palgrave Comms* 5:73: nature.com URL blocked today.
- **Wells 2011/2015**: book only, no PDF.
- **Fuls 2023/2024**: Academia only, blocked.
- **Mackay 1931**: not online in a form I could reach.

## What the project already recorded [R]

From `results/parpola2005_notes.md`, notes Erin made on 20 Oct from the Parpola 2008 PDF. These are a summary, not verbatim:
- "Mackay (1931: 400) saw the link: hare tablets share one inscription, elephant tablets another. Hunter (1934) disputed it."
- "Parpola (1975, 2008) gave a full typology of 46 types": he wrote that the inscription "is enough to predict what is engraved on the other side", and he named image-to-sign pairs "pictorial bilinguals".
- The notes end: "Not ours: the observation itself, and the substitutions."

**So the text–image link, the sets, and the sign-for-image substitutions are anticipated.** The open question is narrower: did anyone compare *different* sets whose texts differ by one sign?

## A finding inside the repo that matters for both claims

`data/crosswalk_G_to_P.csv` maps G704, G705 and G706 all to one CISI/Parpola sign, **P316**:
- G705 → P316: 10 aligned pairs, 100%
- G706 → P316: 3 pairs, 100%
- G704 → P316: 1 pair

Consequences:
- In Parpola's transcription (CISI), the "composite" tablet and the "elephant" tablets probably carry **the same inscription**. That would make them not a minimal pair at all, but another "same text, two motifs" case.
- The 20 Oct check quotes Mahadevan's review of Parpola 1994 describing a known case of this kind: "two sets of copper tablets, both with the same inscription on one side but two different motifs on the other" (fig tree + crab vs. horned archer). [V on 20 Oct, https://www.harappa.com/script/maha15.html]
- The G705 vs. G706 contrast exists only in the ICIT/Wells sign list. Before building on it, someone has to look at the actual drawings of G705 and G706 on the composite tablet and the elephant tablets.

Related point: Indus "composite animals" often include elephant parts.
- Farmer (INDOLOGY, 2000) quotes Mackay on a composite: "a ram, with the horns of a bull, a human face, and the trunk and tusks of an elephant" [V, https://list.indology.info/pipermail/indology/2000-August/022273.html].
- Whether the composite on *this* tablet has a trunk is [U]. If it does, "elephant text → composite with elephant parts" is not a contrast.

---

## Claim 1: one-sign swaps change the copper image; fish-variant swaps do not

**Verdict: PARTLY ANTICIPATED.**

**Anticipated:**
- The text predicts the image, tablets come in sets, and a sign can stand in for an image (Mackay 1931; Parpola 1975/1994/2008/2009).
- Parpola 2009, p. 51 [V, https://www.harappa.com/sites/default/files/pdf/script-indus-parpola.pdf]:
  - "there is a clear interdependence between the inscription on the obverse and the iconographic motif on the reverse."
  - "The numerous duplicates form sets of identical tablets."
  - "In some sets, a single sign on the reverse has the same inscription on the obverse" … "where the reverse shows an animal or human figure."
  - "It appears as if the single sign stood for the name of the divinity illustrated"
- Mackay 1931: 400, that elephant and hare tablets each share an inscription [R].

**Not found:**
- No accessible source makes a systematic comparison of *different-image* sets whose texts differ by exactly one sign. That covers G423/G424 gaur/buffalo, G63/G61 unknown/tiger, and G905/G904.
- No accessible source contrasts these with fish-variant swaps that keep the image.
- Parpola 2009 has no such passage. Its copper section (pp. 51–52) never mentions elephant, hare, tiger, buffalo or gaur [V, same PDF].
- **Caveat:** Parpola's 46-type typology (2008) lays the texts side by side, so the pairs may be visible in his tables even if he does not discuss them [U].

**Weakened:**
- G705/G706 may be one sign in CISI (see above).
- G423/G424, G63 and G905 have no confident crosswalk entry, so I could not check whether CISI splits them.

**Possible tension worth stating** (my inference, not a source claim):
- Parpola reads fish signs as divine names, and the copper images as deities.
- The project finds that swapping fish variants does *not* change the image.
- That fits the project's "fish as modifier" reading better than "each fish sign names the depicted deity". It rests on 2 pairs and 5 tablets.

## Claim 2: G706 G33 recurs on seals with other animals, in a slot shared only with G705 ([marked fish] + G705/G706 + G33 (+ G520))

**Verdict: PARTLY ANTICIPATED (general point); specific formula NOT FOUND.**

**Anticipated in general:** copper-tablet texts recur on seals.
- Mukhopadhyay 2023, *HSSC* 10, doi:10.1057/s41599-023-02320-7 [V, https://www.nature.com/articles/s41599-023-02320-7]:
  - "copper-tablets, contained obverse-side inscriptions that were very similar to the seal-inscriptions"
  - Fig. 15b shows "certain seals and copper tablets containing identical or similar inscriptions."
  - The paper names no elephant tablet. Elephants appear only as seal or sealing images, e.g. M-1155 and L-161 to L-172.
- Ganesan et al. 2009, *Bull. Indus Research Centre* 1, p. 6 [V on 20 Oct, https://rmrl.in/bulletin/bulletin-No-1-Sept-2009.pdf]:
  - "one notable exception is the association of significant text segments with particular field symbols on the copper tablets, (e.g. texts with the field symbol 'hare facing a bush')."
  - "The FS=16 (Hare) occurs only with the following triplets". The triplets are given as glyphs only, so I could not match them to G-numbers.

**Not found:**
- The elephant tablet's text (G706 G33 …) recurring on unicorn, gaur or zebu seals.
- The slot that G706 shares with G705 before G33 G520.
- The formula [inside-marked fish] + X + three long strokes (+ G520).
- Sources checked: Parpola 2009 [V], Mahadevan's review [V], Mukhopadhyay 2023 [V], Abro 2024 on elephant seals [V; abstract only, no sequences, https://data.mendeley.com/datasets/kxk77zrh6n/1], Rao 2018 [V, https://arxiv.org/pdf/1812.00049], and Parpola 2008 "Airāvati" [V; no copper content].

**Weakened:**
- If CISI's P316 merges G704/G705/G706, then in Mahadevan/Parpola numbering "the slot is filled only by G705 or G706" reduces to "the slot is filled by one sign".
- The paradigm claim (two words, one slot) stands only if G705 ≠ G706 is a real distinction. Check by eye.

**Mahadevan's sign numbers:** not mapped. No reliable mapping was found online, and I did not guess.

---

## To do before any novelty claim

1. In Erin's Parpola 2008 PDF, find the type listing that holds the elephant set and the composite tablet. Does he transcribe them with the same sign? Does he list the gaur/buffalo and tiger sets one sign apart?
2. Read Parpola 1994 pp. 108–112 and fig. 13.13 (p. 234) on paper or through the library.
3. Compare the CISI vol. 1 photographs of the G705 composite tablet with the elephant tablets: the sign form, and whether the composite has a trunk.
4. Check whether CISI splits G423/G424, G61/G63 and G904/G905.

## Other sources looked at (nothing relevant)

- Parpola 2019/2020 on ivory rods: https://helda.helsinki.fi/server/api/core/bitstreams/5994c972-f2c5-4520-954d-8a9b63d27b25/content
- Parpola 2011 "Crocodile": https://www.harappa.com/sites/default/files/pdf/Parpola_Asko_2011._Crocodile_in_the_Indu.pdf
- C. Subramanian lecture slides: https://www.imsc.res.in/~sitabhra/meetings/bitsscripts25/assets/talks/C_Subramanian_Lecture_2.pdf
- Neukart 2025 preprint: https://www.preprints.org/manuscript/202502.0699/v1
- harappa.com "Do fish signs denote deities": https://www.harappa.com/content/do-fish-signs-denote-dieties
