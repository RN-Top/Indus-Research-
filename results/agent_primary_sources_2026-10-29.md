# Primary sources for building new Indus data (searched 29 October 2026)

Builds on `agent_new_inscriptions_2026-10-22.md` and `new_finds_search_2026-10-29.md`, and does not repeat them (Bisht 2015 seals, Farmana OP6, Bagasra seals, Bhirrana surface seal, CISI 3.x coverage, post-2022 finds).

**Legend.** **[V]** = fetched in this session: URL plus a short quote or paraphrase of what the page says. **[U]** = unverified or inferred. No URL, count or plate number below was invented. Where a count is unknown, it says so.

**Access limits in this session.**
- The sandbox shell could not download from archive.org, nmma.nic.in, zenodo.org, asiaurangabadcircle.com or ctfassets (proxy 403). So no PDF was opened locally and **no plate was looked at**.
- WebFetch returns only a model summary of the text, which is often cut off partway through long PDFs. Plate legibility is therefore **[U]** throughout. "No mention" in a sampled volume can mean the text was cut off before that site's entry.

## 0. ICIT baseline used for overlap

Counted from `data/icit_merged_paragorth/merged-corpus-canonical.json` (5,369 objects), by object type:

| Site | Objects | Breakdown |
|---|---|---|
| Dholavira | 203 | SEAL 122, TAG 58, TAB 17, MISC 4, **POT 2** |
| Lothal | 202 | SEAL 92, TAG 87, POT 18 |
| Kalibangan | 199 | SEAL 56, POT 89, TAG 23 |
| Banawali | 24 | SEAL 16, POT 5 |
| Rakhigarhi | 11 | **POT 1** |
| Surkotada | 6 | |
| Kanmer | 7 | |
| Shikarpur | 6 | |
| Rupar | 5 | |
| Desalpur | 3 | |
| Daimabad | 2 | |

- Absent from the file: Kuntasi, Juni Kuran, Balu, Mitathal, Nageshwar, Kunal, Bet Dwarka.
- **Pottery graffiti outside Harappa, Kalibangan and Lothal is the thinnest category in ICIT.** Dholavira has only 2 pottery objects.

---

## 1. *Indian Archaeology – A Review* (IAR)

### 1.1 Availability (all [V])

| Host | What it holds | Notes |
|---|---|---|
| **NMMA portal**, https://nmma.nic.in/nmma/archReview.do | 56 volumes, **1953-54 to 2013-14**, with a gap for **2001-02 to 2005-06** | PDF pattern `https://nmma.nic.in/nmma/NAS1/nmma_doc/IAR/Indian%20Archaeology%201961-62%20A%20Review.pdf`. WebFetch refused it: "robots_disallowed". Download in a normal browser. |
| **ASI Aurangabad circle mirror** | e.g. https://asiaurangabadcircle.com/assets/files/publications/1959-1960.pdf, `…/1989-1990.pdf`, `…/admin/uploads/1964-1965.pdf`, `…/1953-1954.pdf`, `…/1967-1968.pdf`, `…/1968-1969.pdf` | WebFetch could read these. |
| **Contentful CDN copies** | 1957-58, 1961-62, 1968-69, 1973-74, 1974-75, 1996-97, e.g. https://downloads.ctfassets.net/l47hkrce4wip/3p5hZS6HRkWYu9Qh94WvVv/ee1e92ac66f0485110a86d153d48f56b/006_Indian_Archaeology_A_Review_1961-62.pdf | Hosting organisation not identified **[U]**. |
| **Zenodo** | 1961-62: https://zenodo.org/records/23140953 ("Creative Commons Attribution 4.0 International", 10.5 MB). 1962-63: zenodo.org/records/1408087. 1963-64: zenodo.org/records/3416858. 1964-65: zenodo.org/record/1442629 ("CC BY-NC-ND 4.0", community "ERC synergy project 609823 archive") | |
| **archive.org** | 1961-62: https://archive.org/details/indianarchaeology196162areview_495_p ("CC0 1.0", PDF 10.1M, hOCR, JP2 zip 136.6M). 1954: https://archive.org/details/dli.ernet.53679 (Digital Library of India) | |
| **Princeton DataSpace** | 1961-62: dataspace.princeton.edu/handle/88435/dsp01w0892f128 ("all rights reserved unless otherwise indicated") | |

**Licence.** IAR is an ASI (Government of India) publication. The CC0 and CC BY labels on archive.org and Zenodo were set by the uploaders, not by ASI. Treat it as **free to read; reuse for research and citation, not redistribution of the scans** **[U as to legal status]**.

### 1.2 Sampled volumes: Harappan inscribed material

Everything quoted here is [V], except where marked; plates were not seen.

| Volume | Harappan inscribed material (as quoted) | Plates cited | Likely in ICIT? |
|---|---|---|---|
| 1959-60 | Lothal: "eight steatite seals (pl. XVI B) and three terracotta sealings". Pl. XVI C–D show cloth and cord marks, not script. | XVI B | Yes. Lothal has 92 seals in ICIT and is in CISI 1. |
| 1961-62 | Lothal: "five Indus seals with unicorn and script (pl. XXI A)", "four others with only the script and terracotta sealings (pl. XXI C)", Persian Gulf seal (pl. XXI B). That is **9 inscribed seals on 2 plates**. | XXI A, XXI C | Yes |
| 1964-65 | Surkotada exploration only, with no seals. The text was cut off before any Kalibangan entry. | – | – |
| 1968-69 | Sanghol (Late Harappan): seals "conspicuous by their absence". Cut off at Bagor. | – | – |
| 1973-74 | No Harappan seals in the visible text (cut off). | – | – |
| 1974-75 | No Harappan seals in the visible text (cut off in Maharashtra). | – | – |
| 1989-90 | Dholavira pp. 17–19: "Seals bear short epigraphs in the Harappan script and many of them are engraved with unicorns"; the north-gate inscription of "nine large Harappan letters". **No plate numbers, no counts.** | none cited | Yes (Bisht 2015 is covered) |
| 1996-97 | **Bagasra** pp. 22–23, **pl. IX**: "Three fragmented pieces of terracotta sealings". One conical sealing has "five distinct stamped impressions" of a unicorn, with "faint impressions of an inscription in Harappan script at the top". **Balu** (Haryana) p. 32: "a knobbed-steatite seal with svastika symbol" (not script). | IX | Bagasra sealing **[U]**. ICIT has 5 Gola Dhoro objects, mostly seals. |

**How rich is IAR?** The sample shows **0–9 legible inscribed objects per volume**, and most volumes in the sample have **none**.
- When a volume illustrates seals, it gives **one plate per site**, with several seals per halftone. Sign-level legibility of these 1960s–90s halftones is **[U]**, and likely poor for small seals.
- IAR's main value is **leads**: site, season and accession numbers that point to final reports. It is not a corpus in itself.
- Almost everything it illustrates from big sites (Lothal, Kalibangan, Dholavira, Banawali) is in CISI 1, CISI 3.2 or ICIT.

**IAR volumes to read in full (download locally).** Expected contents are **[U]**, from known excavation dates:
- 1954-55 to 1962-63: Lothal, Rangpur.
- 1960-61 to 1968-69: Kalibangan.
- 1971-72: Surkotada.
- 1974-75 to 1988-89: Banawali.
- 1985-86 to 1990s: Nageshwar, Kuntasi, Padri, Kanewal, Shikarpur.
- 1989-90 to 2000-01: Dholavira.
- 1997-98 to 2000-01: Rakhigarhi.
- 2006-07 to 2013-14: Bhirrana, Farmana, Khirsara, Kanmer, Bagasra.

### 1.3 Leads for sites absent from ICIT

| Site | What was found | Status |
|---|---|---|
| **Kuntasi** | "a square faience seal without animal figure" (Rawat 2015, Gujarat ports PDF, https://www.ancientportsantiques.com/wp-content/uploads/Documents/PLACES/IndOc-Gulf/Gujarat-Rawat2015.pdf). No figure cited. Whether it bears signs is **[U]**. Final report: Dhavalikar, Raval & Chitalwala 1996, *Kuntasi: a Harappan emporium on west coast* (not online) **[U]**. | [V] |
| **Juni Kuran** | "Steatite seal and fishhooks of copper were also recovered" (same Rawat PDF). Whether it is inscribed is **[U]**. | [V] |
| **Mitathal** | "A broken steatite seal of Mature Harappan period was discovered in 2010" (Haryana State Archaeology PDF, https://www.archaeology.haryana.gov.in/sites/default/files/site-docs/Excavation-sites-A-and-M-website.pdf). No image. | [V] |
| **Kunal** | 11 seals and 1 sealing from phase IC(i), but these are **Early Harappan geometric/button seals, not script** (Konasukawa, https://easaa.org/wp-content/uploads/2023/01/Ayumu-Konasukawa-9.pdf, Figs. 1–2). Not usable for sign data. | [V] |
| **Nageshwar** | Bhan & Kenoyer 1984 (https://www.ancientportsantiques.com/wp-content/uploads/Documents/PLACES/IndOc-Gulf/Nageshwar-Bhan1984%20.pdf) mentions **no** seals, script or graffiti. | [V] |

---

## 2. Museum online collections

**Key finding.** CISI vol. 3 is titled "New material, untraced objects, and **collections outside India and Pakistan**" **[V]** (harappa.com/taxonomy/term/1594; prisma.fi listing). The V&A record confirms that a foreign museum object is catalogued in it: **IS.8:1-1951 = "Corpus … Volume 3, Part 1 … number M-1727"** **[V]** (https://collections.vam.ac.uk/item/O25161).

So **museum holdings of excavated Mohenjo-daro, Harappa and Chanhu-daro objects are essentially all in CISI, and hence in ICIT** **[U, strong inference]**. Undocumented dealer objects in art museums are risky to use (authenticity).

| Museum | Search/API | Indus inscribed objects | Image licence | Notes |
|---|---|---|---|---|
| **Metropolitan Museum** | Website search plus the public Collection API (endpoint not fetched here) | At least 3 seals seen: 49.40.1 (324062), 49.40.2? (324063) and 49.40.3 (324064). Full count **[U]**. | "Public Domain" **[V]** (324064) | 49.40.3: "acquired by John H. Marshall from the Montgomery district" (= Harappa), bought 1949. Likely in CISI 3.1 **[U]**. |
| **Cleveland Museum of Art** | Open Access API, e.g. https://openaccess-api.clevelandart.org/api/collectiononline/metadata/1973.160 (seen in search; record page fetched) | At least 1973.160, 1973.161 and 1964.104. Full count **[U]**. | "Public Domain … can copy, modify, and distribute" **[V]** | 1973.160 lists **no provenance and no citations** **[V]**. A purchase, so authenticity is unverifiable. Is it in CISI 3? **[U]** |
| **British Museum** | Collection online (no public API used here) | 1947,0416.2/.3/.4/.7 etc. are Mohenjo-daro stamp seals, e.g. .3 has a "short inscription in Indus script". **No CISI references** are listed **[V]**. | Not stated on page **[V]**. BM usually uses CC BY-NC-SA for images **[U]**. | Excavated material sent to London. Very likely in CISI 3.1 **[U]**. |
| **Penn Museum** | collections.penn.museum object pages; bibliography links | Chanhu-daro loan group L-141-*: **93 objects** linked to Mackay's Chanhu-daro report **[V]**. Seals include L-141-92 ("5 characters have been carved on the obverse") and L-141-177 ("a row of characters above a one-horned animal"). | No licence on the page; images not visible in the fetch **[V]** | Loans from MFA Boston (Chanhu-daro 1935-36). Chanhudaro is in CISI 3.2 **[V]**. |
| **MFA Boston** | mfa.org collection search | e.g. 36.976 seal-amulet, Chanhu-daro Mound II, "Joint Expedition … 1935–1936", on loan to Penn since 1976; "Requires Photography" **[V]** | Not stated | Same Chanhu-daro group, so in CISI 3.2. |
| **V&A** | collections.vam.ac.uk | IS.8:1-1951 = CISI M-1727 **[V]** | Non-commercial download terms **[V]** | Covered |
| **National Museum New Delhi** (via NVLI/IndianCulture) | wzcc.nvli.in/museums/pashupati-seal: text only, "Accession number: Not given", no image **[V]**. indianculture.gov.in pages are JS-rendered and unreadable here. | **[U]** | Not stated | CISI 1 photographed these. |
| **Sindh Antiquities Dept.** | https://antiquities.sindhculture.gov.pk/?p=2071 "Online Exhibition", "Page 1 of 31", 12 entries per page, mostly Mohenjo-daro seals; **no object numbers** **[V]** | Several hundred items in total? **[U]** | "Copyright © … Government of Sindh" **[V]** | Covered by CISI 2 **[U]** |
| LACMA, Ashmolean, Musée Guimet, Indian Museum Kolkata | Not reached in this session | **[U]** | **[U]** | Expect CISI coverage |

**Verdict.** Museums yield about **0 new texts**. Their one real use is **open, high-resolution images (Met and Cleveland, public domain)** for checking ICIT readings and building an allograph image set.

---

## 3. Scanned classic excavation reports

| Report | Online copy | Licence | Seals in CISI/ICIT? |
|---|---|---|---|
| Mackay, *Further Excavations at Mohenjo-daro*, **Vol. II (plates)**, 1937/38 | https://archive.org/details/in.gov.ignca.9954: "Public Resource" upload from ASI Central Archaeological Library, 308 pp., PDF 13.3M, JP2 zip 161.8M **[V]** | Pre-1947 Government of India work; public domain in India (60 years after publication) **[U, legal inference]** | Yes, CISI 1/2 plus Mahadevan |
| Marshall, *Mohenjo-daro and the Indus Civilization*, 1931 | harappa.com: "available for free at Archive.org, Volume I and Volume II", but "Vol. III, the plates does not seem to be among the versions here on Archive.org" **[V]**. Vol. III (Plates XV–CLXIV) is catalogued on an NVLI rare-books record, accession 48270; download status not stated **[V]** (icvtesting.nvli.in/rarebooks/mohenjo-daro-and-indus-civilization-0). | Public domain **[U]** | Yes |
| Vats, *Excavations at Harappa*, 1940 | Many single plates shown on harappa.com slide pages **[V, search results]**. No full archive.org scan located **[U]**. | Public domain **[U]** | Yes |
| Mackay, *Chanhu-daro 1935-36* (1936 bulletin reprint) | southasiacommons/HathiTrust: "Public domain", pp. 469–478 plus 5 leaves of plates **[V]**. The 1943 monograph (American Oriental Series 20) was **not found online** **[U]**. | Public domain | Yes (CISI 3.2) |
| Rao, *Lothal* (MASI 78, 1979/1985) | Only sales and catalogue records found **[V]** | ASI copyright | ICIT has 202 objects (18 pottery) |
| Lal et al. *Kalibangan*; Joshi *Surkotada*; Bisht *Banawali*; Dikshit | Not found open online in this session **[U]** | ASI copyright | Kalibangan is in CISI 3.2 **[V]**. Surkotada (6) and Banawali (24) are thin in ICIT but are CISI 1 sites. |
| Lal 1960, "From the Megalithic to the Harappa: Tracing Back the Graffiti on the Pottery", *Ancient India* 16: 4–24 **+ 34 plates** **[V]** (keibi.uni-tuebingen.de/Record/KEI00117012) | No open copy found. *Ancient India* issues are on the IndianCulture/NVLI portal (JS, unreadable here) **[U]**. | ASI | Harappan graffiti, single-sign heavy. Partly in Mahadevan/ICIT **[U]**. |

**Verdict.** These reports are free, but their seals are **already in CISI and ICIT**. Use them for **image-linked verification**: re-reading ICIT texts against original plates, and allograph images. They yield no new texts.

---

## 4. Untapped categories

### 4.1 Dholavira pottery graffiti: the clearest gap found

- **Source [V]:** Vinod V., "Signs of the Past: Unraveling the Continuity of Rock Art and Pottery Graffiti", *Heritage: Journal of Multidisciplinary Studies in Archaeology* 10 (2022-23), https://www.heritageuniversityofkerala.com/JournalPDF/Volume10/22.pdf
  - "The study had documented **185 Harappan graffiti marks which include 9 inscriptions and 66 Harappan symbols/scripts**."
  - "Dholavira has produced a total of 66 Indus signs/symbols in the form of pottery graffiti (Table 1, **Figure 13**)."
  - Caption: "Figure 13: Pottery inscriptions from Dholavira."
  - Table 1 gives phase shares (Stage IV 35.02%, Stage V 44.66%, …).
- **Related source:** "Harappan Graffiti from Dholavira" (academia.edu/41581628; blocked here; probably the same author **[U]**).
- **Gap:** ICIT has **2 pottery objects** for Dholavira. How many of the 185 marks are drawn legibly in Fig. 13 is **[U]**.
- **Author's thesis:** V. Vinod, *Specialization in Harappan Pottery Production: A Case Study from Gujarat*, Ph.D., M.S. University of Baroda, 2010 (guide K. Krishnan), Shodhganga hdl 10603/72283. Files: Chapter 4 is 18.86 MB, Appendix 7.3 MB. Licence **CC BY-NC 4.0** **[V]**. Whether it contains graffiti drawings is **[U]**.

### 4.2 Rakhigarhi graffiti

- A. Nath, *Excavations at Rakigarhi 1997–2000*, has a "Graffiti" chapter (Ch. 8, p. 205) (prior note).
- A second open copy: https://www.rarebooksocietyofindia.org/book_archive/196174216674_10153813006761675.pdf **[V]**. The fetch was cut off in Chapter 2, so the chapter's content and count are **[U]**.
- ICIT has 11 Rakhigarhi objects, **1 pottery**.

### 4.3 Harappa (HARP) graffiti

- Kenoyer 2020 (https://www.harappa.com/sites/default/files/pdf/Kenoyer2020%20Origin%20of%20Indus%20Script.pdf) **[V]**:
  - "a total of 1218 sherds with either simple incised marks" or more complex signs (1986–2003).
  - Period 1 has "16 post-firing graffiti"; Period 2 has "175 graffiti".
  - "most of the inscribed pottery and all seals … have been published in the major volumes edited by Asko Parpola", and the rest are "still being prepared for publication".
- So the unpublished HARP sherds are **not open**. Only Figs. 5–7 are illustrated.

### 4.4 Gujarat open-access papers (Heritage journal)

- Uesugi & Jamison 2020, *Heritage* 8.1: 1–37, https://www.heritageuniversityofkerala.com/JournalPDF/Volume8.1/1.pdf **[V]**:
  - Farmana seals FRN-1 (buffalo) and FRN-2 (unicorn), with photographs and SEM images of the signs (Figs. 4, 11–13).
  - "Four steatite square seals were recovered from … Farmana". FRN-3 and FRN-4 are treated "in a separate paper".
  - ICIT Farmana has 7 objects, so these are probably present **[U]**. Useful for high-resolution checking.
- Sanauli (Prabhakar, *Heritage* 11.1): no inscribed material **[V]**.

### 4.5 Kanmer

- Two academia papers, "Harappan Script Material from Kanmer" (4891402) and "Indus Script Material from Kanmer, Gujarat" (110107957): blocked here.
- Rawat 2015 **[V]**: "three terracotta sealings with identical impressions on the obverse but different incised signs on the reverse".
- ICIT Kanmer has 7 objects (1 seal, 3 implements, 2 pottery, 1 tag), so the published script material is perhaps partly covered **[U]**.

### 4.6 Other journals

- *Puratattva* and *Man and Environment* are **not open access** **[U, no open copies found]**.
- *Ancient Asia*: no relevant open article found in this search **[U]**.
- Late Harappan graffiti (Daimabad, Rojdi, Bet Dwarka, Bhagwanpura): **no open primary source with images found** **[U]**.

---

## 5. Ranked: the 5 best sources to build new data from

### 1. Dholavira pottery graffiti (Vinod V.)

- **URLs:**
  - https://www.heritageuniversityofkerala.com/JournalPDF/Volume10/22.pdf (Fig. 13)
  - Shodhganga thesis hdl.handle.net/10603/72283
  - academia.edu/41581628
- **Estimated legible inscribed objects:** up to 9 multi-sign "inscriptions" plus up to 66 sign-bearing sherds. How many are drawn legibly in Fig. 13 is unknown; a realistic guess is **10–40 [U]**.
- **ICIT overlap:** very low. ICIT has 2 Dholavira pottery objects.
- **Licence:** open-access journal (terms not stated on the PDF) and thesis under CC BY-NC 4.0. Fine for research transcription with citation; don't republish the figures.
- **Plan:**
  1. Download the *Heritage* 10/22 PDF in a browser. Extract Fig. 13 at native resolution (`pdfimages -all`).
  2. Download all Shodhganga files of thesis 10603/72283, especially Ch. 4 and the Appendix. Search them for a graffiti catalogue, plates or figures.
  3. Give each sherd an ID: `DHV-GR-<fig>-<n>`, with the stage from Table 1 where given.
  4. Transcribe each mark against `data/fuls_sign_list.csv` and the Wells glyphs (`data/sign_glyphs.csv`). Record pre- or post-firing, direction (sherd graffiti are not mirrored), confidence per sign, and NOMATCH with a description.
  5. Match against the 2 ICIT Dholavira pottery objects.
  6. Append the result to `data/extra_inscriptions/extra_texts.csv` with source, figure and page.
  7. Email the author for the full catalogue. He documented 185 marks, and the publication shows a subset.

### 2. Rakhigarhi: A. Nath 2014 report, Ch. 8 "Graffiti" plus the seal sections

- **URLs:**
  - https://www.harappa.com/content/excavations-rakigarhi-1997-98-1999-2000
  - https://www.rarebooksocietyofindia.org/book_archive/196174216674_10153813006761675.pdf
- **Estimated legible objects:** unknown. Perhaps 5–30 graffiti plus a few seals **[U]**.
- **ICIT overlap:** low. ICIT has 11 Rakhigarhi objects, 1 of them pottery.
- **Licence:** ASI draft report distributed free by harappa.com. Research use.
- **Plan:**
  1. Download the full PDF in a browser.
  2. Read Ch. 8 (p. 205 onwards) and the small-finds chapters. List every figure or plate showing graffiti, seals or sealings.
  3. Extract the images. Keep only marks that are Indus signs (drop simple strokes and crosses, or tag them `nonscript?`).
  4. Transcribe to Wells numbers as above.
  5. De-duplicate against the 11 ICIT objects by trench or accession number and by sign sequence.

### 3. IAR systematic sweep (1953-54 to 2013-14)

- **URLs:**
  - https://nmma.nic.in/nmma/archReview.do (all 56 volumes)
  - Mirrors: asiaurangabadcircle.com/assets/files/publications/<YYYY-YYYY>.pdf; archive.org; Zenodo.
- **Estimated legible objects:** sampled volumes show 0–9 illustrated inscribed objects each. Across the series, perhaps **100–200 illustrated, but mostly in ICIT**. Genuinely new and legible: about **5–25 [U]**, e.g. the Bagasra conical sealing (1996-97 pl. IX), Kuntasi, Juni Kuran, Mitathal, and Gujarat explorations.
- **ICIT overlap:** high for Lothal, Kalibangan, Dholavira and Banawali; low for minor sites.
- **Licence:** ASI. Free to read and cite.
- **Plan:**
  1. Download all 56 PDFs locally. This needs a normal browser or a machine without this proxy.
  2. Extract the text (`pdftotext`, or OCR with `ocrmypdf` where there is no text layer).
  3. Search for `seal|sealing|script|inscri|graffit|Harappan` and build a table: volume, site, page, quote, plate.
  4. Keep the rows for sites with fewer than 15 ICIT objects, or absent from ICIT.
  5. Extract the cited plates (`pdfimages`) and grade legibility A, B or C.
  6. Transcribe grade A and B items only.
  7. Treat each lead as a pointer to the final report or the excavator, for better images.

### 4. Shodhganga theses on Gujarat and Haryana Harappan sites

- **URL:** https://shodhganga.inflibnet.ac.in (e.g. hdl 10603/72283). Search the repository for site names: Bagasra, Shikarpur, Kanmer, Khirsara, Kuntasi, Bhirrana, Farmana, Rakhigarhi, "graffiti", "seal".
- **Estimated legible objects:** **0–50 [U]**. Theses often reproduce graffiti and seal catalogues in their appendices.
- **ICIT overlap:** mixed, unknown.
- **Licence:** CC BY-NC 4.0 or CC BY-NC-SA 4.0 per item **[V for two items]**.
- **Plan:**
  1. Query Shodhganga in a browser. Its site search is JS; use the Google `site:shodhganga.inflibnet.ac.in` operator with site names.
  2. For each hit, download the chapter PDFs listed in the "full" record view.
  3. Search them for figure captions with "graffiti", "seal" or "inscri".
  4. Extract and transcribe as for source 1. Record the thesis handle, chapter and figure as provenance.

### 5. Public-domain and open museum images, and classic report plates (verification set, not new texts)

- **URLs:**
  - Met: metmuseum.org/art/collection/search/324062, 324063, 324064 (Public Domain)
  - Cleveland: clevelandart.org/art/1973.160 and the openaccess-api (Public Domain)
  - Mackay 1937/38 Vol. II plates: https://archive.org/details/in.gov.ignca.9954
  - Marshall 1931 Vols. I–II on archive.org (via harappa.com)
- **Estimated legible objects:** hundreds of seals on Mackay's plates; a handful at the Met and Cleveland. **About 0 new texts.**
- **ICIT overlap:** about 100% (CISI 1, 3.1, 3.2).
- **Licence:** public domain (Met, Cleveland; pre-1947 Government of India reports **[U]**).
- **Plan:**
  1. Download the Mackay JP2 zip, which has per-page images.
  2. Crop each seal and key it to Mackay's catalogue number, then to the CISI M-number (through Mahadevan's concordance).
  3. Link each crop to its ICIT record.
  4. Re-read a random sample blind to measure the error rate of the ICIT transcription.
  5. Build a per-sign allograph image set. This turns the existing corpus into image-backed data, which is new data even with no new texts.

**Bottom line.**
- The only open source with a clear, measurable ICIT gap is **non-seal material, especially pottery graffiti**: Dholavira (2 pottery objects in ICIT against 185 documented marks) and Rakhigarhi (1 pottery object in ICIT).
- Seals in open primary sources are almost all in CISI and ICIT already.
- The largest step that cannot be avoided is **local download in a normal browser**. This sandbox could not fetch any PDF or plate image directly.
