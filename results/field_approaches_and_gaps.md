# What has been tried on the Indus script, why it stalled, and where the open ground is

*Background and orientation document, 16 October 2026. Not a test and not a claim. It summarises the field from general knowledge of the scholarship. Dates, titles and attributions marked **(verify)** should be checked against the original sources before anything here is quoted. Our own results are cited from `results/`.*

## 1. The routes tried, and why each stalled

### 1a. Identifying the language and reading the sounds

The aim is to propose a language and give signs sound values, as Linear B and Maya were deciphered.

| Language proposed | Main proponents (examples) | What they did | Where it stalled |
|---|---|---|---|
| **Dravidian** (proto-Tamil-like) | Asko Parpola (*Deciphering the Indus Script*, 1994); Iravatham Mahadevan; the Soviet team led by Yuri Knorozov (from the 1960s) **(verify dates)**; Walter Fairservis | Sign-by-sign readings, often by rebus (a picture stands for a word that sounds like it). The best known: "fish" read as Dravidian *mīn*, which also means "star". | The readings fit Dravidian, but nothing independent can confirm them. Other scholars cannot reproduce them from the data alone. |
| **Indo-Aryan / Sanskrit** | S. R. Rao (*The Decipherment of the Indus Script*, 1982); N. S. Rajaram and N. Jha (2000) | Alphabetic or syllabic readings, often tied to Vedic texts | Rao's alphabetic reading conflicts with the size of the sign inventory: hundreds of signs, too many for an alphabet. Rajaram and Jha's "horse seal" was shown to be a manipulated image (Witzel and Farmer, 2000) **(verify)**. |
| **Munda / "para-Munda"** | Michael Witzel, as a substrate-language suggestion **(verify)** | Loanwords in early Sanskrit traced to a lost language of the north-west | A hypothesis about the language of the region, not a reading of the script |
| **Sumerian, Elamite, Hittite, Easter Island rongorongo** and others | G. de Hevesy (1932, rongorongo); B. Hrozný (1930s, Hittite-based readings) **(verify)** | Comparisons of sign shapes or sound systems | Visual resemblance is not evidence. These are now generally set aside. |

**The common wall** (section 2): there is no bilingual text, inscriptions are very short, the language is unknown, and there is no way to check a proposed reading against anything outside the reading itself.

### 1b. "It isn't writing" against "it is language-like"

- **Farmer, Sproat and Witzel (2004)**, "The collapse of the Indus-script thesis". They argued the signs are a non-linguistic symbol system. Their reasons: texts are very short, many signs occur only once, and no long texts exist.
- **Rao and colleagues (2009, *Science*)**. Conditional entropy (how predictable each sign is from the one before it) puts Indus between rigid non-linguistic systems and fully free ones, close to known languages.
- **Sproat (2010, 2014)**. Replied that non-linguistic systems can produce the same entropy profile. **(verify exact titles)**
- **Raghavendra (2026, in this repository's references)** shows a constructed non-language reproducing Indus-like statistics.
- **Where it landed:** unresolved. The statistics show **structure**, but structure does not decide "language against non-language". Most specialists still treat it as writing of some kind, possibly mixing word signs and sound signs. The debate showed that statistical signatures alone cannot settle the question. That is why this project claims structure and function, not language.

### 1c. Corpora and sign lists: infrastructure, not decipherment

- **Mahadevan 1977:** *The Indus Script: Texts, Concordance and Tables* (often called "M77"), with its own sign list.
- **Parpola and colleagues:** the *Corpus of Indus Seals and Inscriptions* (CISI, several volumes from 1987 onwards), with photographs and its own sign list.
- **Wells and Fuls:**
  - Bryan Wells's sign list and positional work, including the 1998 MA thesis that Fuls cited (column analysis, Fig. 4.6, p. 104), his 2006 dissertation and *Epigraphic Approaches to Indus Writing* (2011);
  - the ICIT database (Wells and Fuls);
  - Andreas Fuls's positional and statistical studies.
- **What they gave:** the data everyone works from, sign classes, and position classes (initial signs, terminal markers).
- **Why they are not decipherment:** they describe *how signs are used*, not *what they say*. Different sign lists also split and merge signs differently, so results depend on the transcription.

### 1d. Iconography and rebus readings

- **Approach:** reading the meaning of signs from the animals and scenes on seals (unicorn, "proto-Shiva", fig deity), and the rebus chains in 1a ("fish" = "star").
- **Why they stay unfalsifiable:** each reading picks a language and a chain of sound puns *after* seeing the sign. Nothing in the data could prove a given chain wrong, so it cannot be tested.

## 2. What the failures have in common

The sound-based route is blocked by facts about the material, not by lack of effort:

1. **No bilingual.** No inscription is known to repeat its text in a readable script.
2. **Very short texts.** Most are around 5 signs. That is too little context to test sound values or grammar.
3. **Unknown language.** Even a correct sound value could not be checked against a known vocabulary.
4. **Probably a mixed system** of word signs and sound signs. Neither an alphabet-style nor a picture-style decipherment fits cleanly.
5. **Thin context.** Many objects lack precise dates or find spots, and the corpus is dominated by two cities.
6. **Transcription dependence.** Sign identification differs between sign lists (M77, CISI, Wells/ICIT).

**Realistically,** the sound route is unlikely to move without **new finds**: a bilingual, a long text, or a well-dated archive. That is a reason to work on questions that do not need sounds.

## 3. Where this project sits

**Approach:**
- Read signs by **function and position** only.
- Test every claim as a **prediction registered in advance**, run once on a **locked 20% holdout**.
- Correct for every test ever run (Benjamini–Hochberg).
- Claim **no sound values**.

**Established** on unseen data (`confirmatory_2026-10-14.md`; 19 tests, 16 supported):

| Finding | Notes |
|---|---|
| The positional layout: heading → middle → closer | Learned at Mohenjo-daro, holds at other sites (76% against 27%). It confirms Wells's description, as Fuls rightly notes; the project did not discover it. |
| The blind role rule finds real headings | On Proto-Elamite tablets, against expert-marked headers |
| Indus headings are a small fixed set | Unlike Mesopotamian seal openers |
| A fixed end-of-middle slot | G100, G760, G142 and G923 sit last, before the closer, 90% of the time |
| A closer tied to an object class | G407 and G617 on the copper tablets of Mohenjo-daro |
| **Rare signs at the start of inscriptions without a heading** | 32% against 17%, q = 0.0019. Consistent with names, not proven to be names. |

**Limits, honestly:**
- Function is not meaning, and meaning is not sound.
- Everything depends on one transcription, which derives from ICIT.
- Holdout counts are small for several claims.
- Structure does not prove language (1b).
- The layout itself is prior work.

## 4. Unworked or under-worked directions that do not need sounds

### 4a. The script as administration, not language

- **Idea:** proto-cuneiform and Proto-Elamite began as **accounting**: commodities, numbers, people.
- **What we have:**
  - Indus has numerals; "count-like" items that take many values (G220 "fish", G390, G900); and "formula-like" number + sign pairs (`number_system_scouting.md`).
  - The Proto-Elamite comparison showed the rule finds account headers.
  - But Indus texts almost never *end* in a number, unlike accounts (`proto_elamite_comparison.md`).
- **Status:** *promising but partly against:* Indus is not account-like overall, but the count-like items may be an administrative layer inside label texts.
- **Has it been worked?** Ideas that seals and tablets served trade or administration are common in the archaeology (Kenoyer, Possehl, and others) **(verify specifics)**, but a *sign-level* test of commodity behaviour is not something this search found.

### 4b. The seals as a social and economic network

- **Idea:** treat inscriptions as nodes in a network. Which signs travel between cities, which stay local, which reach Mesopotamia and the Gulf.
- **What we have:**
  - sign travel by site (`sign_travel_water.md`);
  - the find-spot map and the water results;
  - G924 on the Susa and Ur seals (`name_inventory_scouting.md`);
  - rare "name-like" signs with a slight tendency to stay at one site.
- **Status:** *promising, but limited by data.* Most texts are from two sites, and dating is poor.
- **Has it been worked?** Find-spot distribution and trade studies exist. A formal network of sign sharing between sites is uncommon **(verify)**.

### 4c. The script as a designed system

- **Idea:** ask how the signs were built: composite signs (ligatures), whether components keep their meaning, and whether the inventory looks engineered or evolved.
- **Status:** *long shot with current data.* Wells, Mahadevan and Parpola all catalogued composite signs, but testing "composition rules" needs a machine-readable breakdown of each sign into components, which this project does not have.

### 4d. Genres within the script

- **Idea:** different object classes may carry different *kinds* of text, each with its own slot fillers: seals, moulded tablets, copper tablets, pottery, tags.
- **What we have:**
  - G400 goes with Harappa tablets;
  - G407/G617 go with copper tablets;
  - the "complex" texts are mostly a rare-sign tail, not a genre (`complex_texts_scouting.md`).
- **Status:** *promising and directly testable.*

## Where the open ground actually is

These are directions that, as far as we know, nobody has really worked, that do not depend on sound, and that are within reach of the data and method already in place.

1. **Names as data.** The rare-first-sign result gives a *position-defined* list of possible personal names.
   - **Sharpest question:** do rare signs found in the name position recur **within one site** more than chance, and does that hold on the holdout? That would turn "maybe names" into "behaves like local personal names".
2. **Sign geography as a network.**
   - **Sharpest question:** do pairs of cities share more rare (name-like) signs than their sizes predict? Shared names would suggest movement of people, not just of goods.
3. **Genres by object class.**
   - **Sharpest question:** can the object type (seal, moulded tablet, copper tablet, pottery) be predicted from the inscription alone, using only position-based features, on unseen texts? If yes, the script has genre-specific grammar, and each genre can be read for its own function.
4. **The administrative layer.**
   - **Sharpest question:** in the holdout, do the count-like items (fish, G390, G900) take a wider spread of numbers than the formula items (G520, G585, G803)? That would show genuine counting inside the texts.
   - **Caveat:** it needs more data (a second transcription) to have enough power.

**Infrastructure that would strengthen every direction:**
- A **second transcription** (CISI or M77) for replication. It would answer much of Fuls's point about transcription and the 13%.
- **Better dating and find-spot data.**

## Sources to check

- Parpola, A. (1994). *Deciphering the Indus Script*. Cambridge.
- Mahadevan, I. (1977). *The Indus Script: Texts, Concordance and Tables*. Archaeological Survey of India.
- Parpola, A. et al. (1987–). *Corpus of Indus Seals and Inscriptions*.
- Wells, B. K. (1998), MA thesis (as cited by Fuls, Fig. 4.6, p. 104); (2006) PhD dissertation, Harvard; (2011) *Epigraphic Approaches to Indus Writing*. Oxbow.
- Farmer, S., Sproat, R. and Witzel, M. (2004). "The collapse of the Indus-script thesis." *Electronic Journal of Vedic Studies* 11(2).
- Rao, R. P. N. et al. (2009). "Entropic evidence for linguistic structure in the Indus script." *Science* 324: 1165.
- Sproat, R. (2014). "A statistical comparison of written language and nonlinguistic symbol systems." *Language* 90(2). **(verify)**
- Rao, S. R. (1982). *The Decipherment of the Indus Script*.
- Raghavendra (2026), in `novelty_assessment.md`.
