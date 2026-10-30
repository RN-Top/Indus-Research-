# Open sources for new multi-sign pottery graffiti (searched 30 October 2026)

**Purpose.** To find new material for the sealed prediction `predictions/new_finds_P15_pottery_graffiti_2026-10-30.json`. That prediction is evaluated only once there are **20 or more new multi-sign graffiti** that are not already in ICIT.

**What this note does not repeat.** It builds on `agent_primary_sources_2026-10-29.md` and does not repeat what that note and these files already cover:
- IAR availability
- museum collections
- Vinod 2023 basics (see also `data/extra_inscriptions/dholavira_graffiti_vinod2023_PROVISIONAL.md`)
- Nath 2014 (see `data/extra_inscriptions/rakhigarhi_nath_graffiti_NOTES.md`: 163 graffiti sherds, **no drawings**)

**Legend.**
- **[V]** = fetched in this session; a URL and a quote or close paraphrase are given.
- **[U]** = not verified.
- No count below is invented. "Figure legibility" is **[U]** everywhere, because the sandbox could not download any PDF or image. Every download attempt gave proxy 403: heritageuniversityofkerala.com, archive.org, asi.nic.in. WebFetch returns text only.

## 0. Corrected ICIT baseline (pottery, `merged-corpus-canonical.json`)

Counted this session:
- **543 pottery objects** in total. Of these, **271 have 2 or more signs**.
- **Harappa 267** (not about 350 as stated in the brief): 123 have 2 or more signs. By HARP period: Period 1 Ravi = 1 object; Period 2 = 16; Period 2/3 = 4; Period 3 = about 107; the rest are unphased.
- **Kalibangan 89** (39 with 2 or more signs). Phases: "2 Late" 16, "2 Early" 2, "2 Middle" 2, "1 Late" 1, the rest unphased.
- **Mohenjo-daro 71** (49), **Nausharo 21** (15), **Lothal 18** (7), **Kot-Diji 10** (5).
- Shikarpur 5, Banawali 5, Amri 5, Chanhu-daro 4, Rojdi 4, Surkotada 4, Alamgirpur 3.
- Farmana 2, Kanmer 2, Dholavira 2, and **Karanpura 1, Rakhigarhi 1, Bala-kot 1, Juna Khatiya 1**.
- Absent: Rangpur, Bhirrana, Kunal, Mitathal, Masudpur, Bagasra/Gola Dhoro pottery, Kuntasi, Sanauli.

## 1. Heritage journal (University of Kerala): volume-by-volume check

**Archive page fetched [V]:** https://www.heritageuniversityofkerala.com/Archive.aspx
- It lists Vols. 1 (2013) to 12 (2024; Vol. 11 in 2 issues; Vol. 8 in 2 issues).
- Each volume links only to `VolumeDetails.aspx?VID=…`. **Those pages are not on this session's fetch allowlist**, so I could not read the tables of contents directly.
- Instead, I searched the PDF space (`site:heritageuniversityofkerala.com` with "graffiti", "Harappan inscribed potsherd script signs", and site names).

| Hit | Content | Graffiti? |
|---|---|---|
| Vol. 10/22, Vinod, "Signs of the Past" [V] | "185 Harappan graffiti marks which include 9 inscriptions and 66 Harappan symbols"; numerals 29.24%; 40 signs match Mahadevan, 26 are "new"; **only one pottery figure, Fig. 13 "Pottery inscriptions from Dholavira"**; Dholavira only. Format of the drawings (photo or line) is not stated. | Yes. **9 drawn** (already transcribed provisionally in the repo). Panel 5 is a *stamped* goblet base, not incised, so **8 qualify** for P15. |
| Vol. 10/42, Jadeja et al., Gajod (Kachchh) [V] | Survey of a Sorath Harappan site; figures cover pottery, copper and shell | **No** graffiti, script or seals |
| Vol. 4/1, Uesugi et al. 2016, Bhirrana seal [V] | Surface seal with "three inscribed characters"; Fig. 3 redraws 3 excavated Bhirrana seals (after Rao et al. 2005) | No graffiti (seals only) |
| Vol. 5/1, Bagasra unicorn seals [V title] | seals | Not graffiti |
| Vol. 8.1/1, Farmana seals; Vol. 11.1/1, Sanauli | covered 29 Oct | No graffiti |
| Vol. 1 (2013) special Harappan issue (page-range PDFs, e.g. `Volume1/356-371.pdf` "Diachronic Changes of the Harappan Pottery", `466-474.pdf` geometric patterns, `486-499.pdf` beads) [V titles] | Titles only seen; no graffiti title surfaced | [U]. Worth a manual look at the Vol. 1 table of contents in a browser. |

**Verdict.** Searching this journal surfaced **one graffiti paper (Vinod) and nothing else**. A manual browser pass over `VolumeDetails.aspx?VID=1…112` is still needed to be sure.

## 2. New sources found (not in earlier notes)

### 2.1 Karanpura (Hanumangarh, Rajasthan; Early to Mature Harappan)

- **Report [V]:** V. N. Prabhakar & Jaseera C. Majid, "Preliminary Results of Excavation at Karanpura" (seasons 2012–14), https://www.harappa.com/content/preliminary-results-excavation-karanpura-harappan-settlement-district-hanumangarh-rajasthan
  - It mentions "spindle whorls with graffiti marks" resembling "the earliest Indus writing found at Harappa".
  - Fig. 2: "Graffiti marks on spindle whorls from the same floor level of an early Harappan house". These are **whorls, not pots**.
- **Video [V]:** "Inscribed Material from the Harappan Site of Karanpura, Rajasthan (India)", 19:14, https://www.harappa.com/video/inscribed-material-harappan-site-karanpura-rajasthan-india
  - The summary page (node/5245) says: "Key signs on ceramics are discussed among the **130 distinct ones identified**, including some new ones", and mentions "graffiti markers that may have designated ownership in early Indus phases".
- **No written catalogue found** [U]. ICIT has 1 Karanpura pottery object.
- **Potential: high but not reachable as text.** The video slides may show sherds, so screen-grabs could be legible [U]. Ask the authors (V. N. Prabhakar, IIT Gandhinagar / ASI) for the paper.

### 2.2 Kenoyer 2020: HARP early graffiti figures

- **Citation [V]:** Kenoyer, "The Origin and Development of the Indus Script: Insights from Harappa and other Sites", in K. Lashari (ed.), *Studies on Indus Script*, Karachi 2020, pp. 217–236.
- **PDFs:** https://www.harappa.com/sites/default/files/pdf/Kenoyer2020%20Origin%20of%20Indus%20Script.pdf (and a `-2.pdf` variant).
- **Figures:**
  - Fig. 4: "Balakot Potter's Marks, Graffiti and Painted motifs (from Dales 1974, Fig. 11)".
  - Fig. 5: "Harappa, Ravi and Kot Diji Phase Potter's marks and post-firing graffiti".
  - Fig. 6: H98/8440-202 (Ravi) and H99-4367/8946-37 (Kot Diji).
- **Multi-sign items drawn:** a handful at most [U]. Period 1 items "involve up to three combined symbols".
- **Overlap with ICIT is likely.** ICIT already has H-1522 (Ravi, 3 signs) and 16 Period 2 items.
- **Value:** comparison and dating, not volume.

### 2.3 Lal 1960, *Ancient India* 16: 4–24 (open scan)

- **Text layer [V]:** https://ia803202.us.archive.org/24/items/in.ernet.dli.2015.56562/2015.56562.Ancient-India-1960_text.pdf (Digital Library of India item `in.ernet.dli.2015.56562`).
  - Sites in Fig. 1 include Amri, Harappa, Kalibangan, Lothal, Mohenjo-daro, **Rangpur**, plus chalcolithic and megalithic sites.
  - "out of the total of sixtyone symbols … fortyseven are common" to both groups.
  - The paper catalogues **single symbols**. It notes that some pots bear "two or three different symbols" without drawing them as texts.
- **Multi-sign count:** about 0 usable [U].
- **Licence:** ASI 1962, DLI scan. Free to read.
- **Use:** single-sign Rangpur forms; not a source for P15.

### 2.4 *Excavations at Kalibangan: The Harappans (1960–1969)*, Part II, MASI 110 (ASI 2015?)

- **URL [V from search result]:** https://asi.nic.in/pdf/Excavation-at-Kalibangan-Part-II-min-1-compressed_compressed.pdf
- WebFetch is refused here ("robots_disallowed"); a normal browser should work [U].
- Whether there is a graffiti chapter or plates is [U].
- ICIT has 89 Kalibangan pottery objects, very likely from CISI 3.2, so the overlap is probably high.
- **Use:** the pottery the final report adds beyond CISI 3.2, if any [U].
- The same ASI path also hosts other MASI volumes, e.g. "EXCAVATIONS-AT-HULAS.pdf" (Late Harappan, MASI 113), also robots-blocked [U].

### 2.5 Bhirrana (ASI Excavation Branch page)

- **Page [V]:** https://excnagasi.in/excavation_bhirrana.html
  - "Pottery graffiti at Bhirrana show 'mermaid' type deities and dancing girls."
  - The dancing-girl sherd is "engraved on a potsherd in the form of graffiti".
  - Also "inscribed celts of copper" (Period II-B).
- The graffiti are **pictorial, not script**, so not usable for P15.

### 2.6 Sydney thesis: Sareeta Zaid 2022, "The Indus Civilisation: A contextual approach to script"

- **Record [V]:** https://ses.library.usyd.edu.au/handle/2123/29416
- Sites: Harappa, Mohenjo-daro, Lothal, Chanhudaro, Dholavira, Surkotada, **Rakhigarhi, Farmana**.
- Licence: author retains copyright, research and study use only.
- Pottery graffiti are not mentioned in the abstract [U]. Probably built from existing corpora, so low novelty.

### 2.7 Shodhganga

- Theses checked [V], all CC BY-NC-SA 4.0, with no graffiti signalled in their metadata:
  - 10603/156149: Manchanda 1969, Harappan pottery.
  - 10603/72203: Panjwani 1981, Gujarat ceramics.
  - 10603/151570: Wakankar 1973, rock shelters.
- Vinod's 2010 thesis (10603/72283, noted 29 Oct) is still the best Shodhganga lead. Its graffiti content is [U].
- Shodhganga full-text search is not reachable here.

### 2.8 Not reachable or nothing found

- **Possehl 1996**, *The Indus Age: The Writing System*: no PDF on harappa.com [V].
- **Kanmer**: "Harappan/Indus Script Material from Kanmer" exists on academia only (blocked). The book *Indus Civilization: Text & Context* II is not open.
- **RIHN Kanmer report**: no open PDF found.
- **Rojdi** (Possehl & Raval 1989): no PDF [V, harappa.com and upenn pages].
- **Mitathal** (Suraj Bhan 1975), **Kunal** (Khatri & Acharya, *Puratattva*), **Masudpur**, **Alamgirpur** (ResearchGate, blocked), **Gola Dhoro/Bagasra** pottery graffiti, **Rakhigarhi 2011–17** (Archaeopress vol. 1 is paywalled and about the cemetery [V]): **no open drawings found**.
- *Ancient Asia* and the *Journal of Indian Ocean Archaeology*: no relevant open article surfaced.
- Painted (not incised) script on ceramics: https://www.harappa.com/content/painted-indus-script-ceramics-and-steatite-new-insights-indus-script-calligraphy-and [title V; content U]. Out of scope for P15 unless the protocol is widened.

## 3. Has anyone said the earliest multi-sign graffiti are "sign + numeral" (item + count)?

**Short answer: not found.** No source I could read states it. The closest statements:

1. **Kenoyer 2020** [V, PDF above]:
   - Period 1 has "16 post-firing graffiti"; some "appear to be more complex and involve up to three combined symbols (Figure 5)".
   - Period 2 has "175 graffiti that include some relatively simple signs" and "more examples of multiple signs combined together".
   - The highlighted early combination is **Mahadevan 342 + 347** ("this sign is also combined with another sign (Mahadevan sign 347) in a sequence" that "also appears in later Indus seals").
   - **Numerals are not mentioned** for early graffiti. On Kalibangan: "three sherds had the single sign that is the most common sign".
2. **harappa.com** "Evolution of Indus Script" [V]: "Many sherds inscribed after firing have single geometric signs" and "On some sherds, two signs of the Early Indus script (Kot Dijian Phase) appear together. The sign on the left eventually becomes one of the most common signs." No numerals mentioned.
3. **Parpola** (harappa.com lecture PDF `indusscript%282%29.pdf`) [V]:
   - "A baked seal impression and a potsherd with short inscriptions that include the most frequently attested sign … suggest that the Indus script was created during the last phase of the Early Harappan period, between 2800–2600 BCE."
   - His numeral + "fish" discussion concerns **Mature seals**.
   - harappa.com Q&A quotes him [V]: "most of the graffiti from this phase are not writing in the real sense".
4. **Meadow 1999** (Indology list) [V]: "The 'spontaneous' inscriptions begin in the Ravi phase and continue through the Kot Dijian into the Harappan." He does not describe content.
5. **Witzel 2000** (Indology list) [V]: a V-like sign "alongside numbers, such as 'III V' and 'IIII V'" on Harappa *tablets*, possibly "a measure of". This is an item + count reading, but for Mature tablets, not early graffiti.
6. **Mukhopadhyay 2023**, *Humanities & Social Sciences Communications* [V]: a sign that "sometimes occurs on rims and bodies of vessels accompanied by stroke-numerals (Fig. 20b)". This is Mature Harappan material.
7. **Nath 2014** (from the repo's notes, not re-fetched): at Rakhigarhi, Early Harappan marks are "mostly 1–14 strokes", and belly/neck marks made after firing "may be the owner's name".
8. **Lal 1960** [V]: stroke-count symbols (2–5 lines; 1–7 horizontal strokes) are catalogued as ordinary graffiti symbols. "To stress the point that the symbols do have a phonetic, syllabic or alphabetic value would indeed be presumptuous."
9. **Not readable here [U]:**
   - Kenoyer 2006 (RIHN pre-symposium; filename on harappa.com, URL not allowlisted)
   - Kenoyer & Meadow 2010, "Inscribed Objects from Harappa Excavations 1986–2007" (fetch failed twice)
   - Kenoyer & Meadow 2000, "The Ravi Phase"
   - Possehl 1996
   - Fuls (academia, blocked)

   These remain the places to check before claiming priority.

**Our own exploratory check of ICIT** (computed this session; not a confirmatory test):
- Numerals = G1–7, the stacked forms (G13–19, 27–29, 55) and the long forms (G31–33, 35), as in `scripts/functional_slots.py`.
- **Loose "early" set:** Harappa Periods 1, 2 and 2/3; Kalibangan "Early"; plus Kot-Diji, Amri, Hissam-dheri, Bala-kot and Karanpura objects without phase labels. In this set, **9 of 21** multi-sign pottery texts are exactly "one sign + one numeral" pairs, against **61 of 250** for all other multi-sign pottery (Fisher one-sided p = 0.06).
- **Strictly dated subset** (HARP Periods 1, 2, 2/3 plus Kalibangan Early): 4 of 10.
  - Examples: H-1545 [893, 31], H-1550 [700, 31], K-416 [861, 2], Hd-3/Hd-4 [480, 1].
- Suggestive, but the sample is tiny and the site phasing is weak.
- The observation looks **unclaimed in the literature I could reach**. It is not confirmed as novel, because Kenoyer & Meadow 2010 and Possehl 1996 were not read.

## 4. Ranked sources and running total of reachable new multi-sign graffiti

"Reachable" means drawn or photographed in an open source, not in ICIT, and incised or scratched (not stamped or painted), with 2 or more signs.

| Rank | Source | Site / period | Multi-sign drawn | Legibility | Licence | Running total |
|---|---|---|---|---|---|---|
| 1 | Vinod, *Heritage* 10/22, Fig. 13 [V] | Dholavira, Stages III–VII (mostly IV–V, Mature) | 9 (8 incised; 1 stamped) | Low; read from phone screenshots; high-resolution copy requested from the author | Open-access journal, terms not stated | **8** |
| 2 | Karanpura video and report (harappa.com) [V] | Karanpura, Early–Mature | Unknown; "130 distinct" signs discussed | [U]; video only | harappa.com, all rights reserved | 8 (+? if the slides or the authors deliver) |
| 3 | Vinod 2010 thesis, Shodhganga 10603/72283 [V record] | Gujarat Harappan sites | [U] | [U] | CC BY-NC 4.0 | 8 (+?) |
| 4 | *Kalibangan* Part II, MASI 110, asi.nic.in [V URL] | Kalibangan, Mature | [U] | [U]; browser only | ASI | 8 (+?, likely mostly in CISI 3.2) |
| 5 | Kenoyer 2020, Figs. 4–6 [V] | Harappa Ravi/Kot Diji; Balakot I | A few [U] | [U] | harappa.com | 8 (+0–3; overlap with ICIT likely) |
| 6 | Lal 1960, *Ancient India* 16, archive.org DLI [V] | Harappan + Rangpur + Megalithic | about 0 (single symbols) | [U] | ASI / DLI | 8 |
| – | Nath 2014 Rakhigarhi [repo notes] | Rakhigarhi | 0 drawn (163 catalogued, no drawings) | – | ASI draft | 8 |
| – | Bhirrana (excnagasi.in) [V] | Bhirrana | 0 (pictorial) | – | ASI | 8 |

**Running total: 8 reachable new multi-sign incised graffiti, all low-legibility (Dholavira).** That is below P15's 20-item threshold.

**Most promising paths to 20 or more:**
- (a) Vinod's full Dholavira catalogue: 185 marks, of which 9 are "inscriptions", so the multi-sign ceiling there is about 9–20 [U]. Email vinodarchaeo2003@gmail.com.
- (b) The Karanpura inscribed-material paper or slides from Prabhakar & Majid.
- (c) A browser download of the Kalibangan MASI 110 Part II and Vinod's Shodhganga Chapter 4 and Appendix.

## Sources consulted (URLs)
- https://www.heritageuniversityofkerala.com/Archive.aspx
- https://www.heritageuniversityofkerala.com/JournalPDF/Volume10/22.pdf ; …/Volume10/42.pdf ; …/Volume4/1.pdf
- https://www.harappa.com/content/preliminary-results-excavation-karanpura-harappan-settlement-district-hanumangarh-rajasthan ; https://www.harappa.com/video/inscribed-material-harappan-site-karanpura-rajasthan-india ; https://www.harappa.com/node/5245 ; https://www.harappa.com/node/4230
- https://www.harappa.com/sites/default/files/pdf/Kenoyer2020%20Origin%20of%20Indus%20Script.pdf ; …Script-2.pdf
- https://www.harappa.com/sites/default/files/pdf/indusscript%282%29.pdf (Parpola)
- https://www.harappa.com/blog/evolution-indus-script ; https://www.harappa.com/slide/inscribed-sherds ; https://www.harappa.com/slide/inscribed-sherd-kot-dijian-phase ; https://www.harappa.com/answers/how-old-oldest-ancient-indus-writing
- https://list.indology.info/pipermail/indology/1999-May/017203.html (Meadow) ; https://list.indology.info/pipermail/indology/2000-July/021777.html (Witzel)
- https://www.nature.com/articles/s41599-023-02320-7 (Mukhopadhyay 2023)
- https://ia803202.us.archive.org/24/items/in.ernet.dli.2015.56562/2015.56562.Ancient-India-1960_text.pdf (Lal 1960)
- https://excnagasi.in/excavation_bhirrana.html
- https://ses.library.usyd.edu.au/handle/2123/29416 (Zaid 2022)
- https://shodhganga.inflibnet.ac.in:8443/jspui/handle/10603/156149 ; …/72203 ; …/151570
- https://www.archaeopress.com/Archaeopress/Products/9781803275918
- https://asi.nic.in/pdf/Excavation-at-Kalibangan-Part-II-min-1-compressed_compressed.pdf (URL from search; not fetched)
