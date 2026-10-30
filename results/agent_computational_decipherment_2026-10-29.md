# Computational decipherment methods: what has worked, and what could transfer to the Indus script

Compiled 2026-10-29 for the Indus-Research- project (Erin Rae Toppe). Research agent report; no repo files were changed except this one.

**Marks.**
- **[V]** = I fetched the page in this session. Each [V] item gives the URL and a short quote or close paraphrase of what the page says.
- **[U]** = not verified this session. It comes from search-result snippets, background knowledge, or a page I could not open.

Do not cite a [U] item without checking it first.

**Access limits.**
- arXiv abstract pages, the DSAL search, De Gruyter (ZA), cambridge.org abstracts and pmc.ncbi.nlm.nih.gov were blocked or allowlist-refused in some cases.
- I used arXiv PDFs, ACL Anthology pages, MIT DSpace, Wikipedia, ANE Today, LRB and Language Log instead.
- academia.edu and researchgate were not used.

---

## Bottom line first

1. **Every successful computational decipherment so far tested a script that was already deciphered**: Ugaritic, Linear B and Gothic.
   - Each test supplied a known, closely related language as a word list: Hebrew, Greek, or Proto-Germanic/Old Norse/Old English.
   - Each script was alphabetic or a plain syllabary, with words separated or close to it.
   - None of these conditions holds for Indus.
2. **The one real-world application to an undeciphered script was Iberian (Luo et al. 2021).** It produced a negative or inconclusive result: no strong support for Basque.
3. **Linear Elamite (Desset et al. 2022) was deciphered by hand, not by computer.** It rested on three things:
   - royal and divine names already known from cuneiform;
   - a monument carrying both Akkadian cuneiform and Linear Elamite;
   - the fact that the language (Elamite) was already partly known.
4. **I found no published or preprint application of a phonetic-prior method to Indus with any candidate language**, whether Proto-Dravidian, Munda, Burushaski or Indo-Aryan. There are Indus claims that call themselves "computational" (Yajnadevam 2024, glossa-lab, and a ResearchGate preprint on "185 Proto-Dravidian readings"). None uses the Snyder/Luo family of models, and none is peer-reviewed.
5. **The realistic computational experiment for this project is a power test, not a decipherment.** It asks whether a phonetic-prior or cognate-matching method could even tell Dravidian from Indo-Aryan, given Indus-like conditions: short texts, logo-syllabic writing, no segmentation. The repo already holds two control corpora that are needed for it (Tamil-Brahmi and Prakrit). See the final section.

---

## Part 1. Methods: inputs, results, failure cases, code

### 1.1 Snyder, Barzilay & Knight 2010, "A Statistical Model for Lost Language Decipherment" (ACL), Ugaritic → Hebrew — [V]
- **URL:** https://pages.cs.wisc.edu/~bsnyder/papers/bsnyder_acl2010.pdf. ACL Anthology id P10-1107.
- **Quote:** "Given a non-parallel corpus in a known related language, our model produces both alphabetic mappings…"
- **Inputs.** The paper takes these as given:
  - a known related-language corpus: Biblical Hebrew, with a morphologically analysed lexicon (POS tags, affix inventory);
  - unanalysed Ugaritic word types.
- **Assumptions.** It assumes that:
  - the script is alphabetic;
  - graphemes are transcribed unambiguously;
  - words are separated;
  - the language family is known.
- **Results.**
  - Letters: 29 of 30 Ugaritic letters mapped correctly.
  - Cognate translation: about 60.4% by type.
  - Morphological segmentation: 88.5% F-measure.
- **Failure cases and limits.**
  - The model works at the vocabulary level only.
  - It confuses the masculine plural suffix with a possessive suffix.
  - It was initialised from an HMM baseline.
- **Code:** No public code found [U].

### 1.2 Berg-Kirkpatrick & Klein 2011, "Simple Effective Decipherment via Combinatorial Optimization" (EMNLP) — [V]
- **URL:** https://aclanthology.org/D11-1029.pdf
- **Quote:** "Our system requires only a list of words in both languages as input."
- **Method.**
  - It jointly matches the alphabet (with a linear program) and the lexicon (with the Hungarian algorithm), using block coordinate descent.
  - It assumes "a close correspondence between the alphabets of the two languages exists, but is unknown".
- **Results.**
  - Ugaritic: 90.4% lexicon accuracy, with 28 of 33 alphabet mappings recovered.
  - Romance cognates: about 90%.
- **Failure cases.** The method assumes one-to-one character correspondence and a closely related language.
- **Code:** [U] (not checked).
- **Related work** [U]: Berg-Kirkpatrick & Klein, "Decipherment with a Million Random Restarts" (EMNLP 2013) works on substitution ciphers, not lost languages.

### 1.3 Luo, Cao & Barzilay 2019, "Neural Decipherment via Minimum-Cost Flow: from Ugaritic to Linear B" (ACL) — [V]
- **URL:** https://arxiv.org/pdf/1906.06718. ACL Anthology id P19-1303.
- **Quote:** "When applied to the decipherment of Ugaritic, we achieve a 5.5% absolute improvement over state-of-the-art results."
- **Linear B setup.**
  - The data were 919 Linear B–Greek word pairs drawn from a compiled lexicon.
  - The names subset had 455 Greek proper nouns, with about 50% of the Linear B words left unpaired.
- **Results.**
  - Linear B cognate translation: 84.7% with no noise, falling to 67.3% on the names subset ("correctly translates 67.3% of cognates").
- **Limits stated.**
  - Syllabic scripts are "significantly harder".
  - It needed random restarts with model selection.
  - It needs a known related language and a substantial share of cognates.
- **Code:** "Code and all datasets are hosted in https://github.com/j-luo93/NeuroDecipher" (quoted from the PDF). I did not open the repository.

### 1.4 Luo, Hartmann, Santos, Barzilay & Cao 2021, "Deciphering Undersegmented Ancient Scripts Using Phonetic Prior" (TACL 9) — [V]
- **URLs:** https://arxiv.org/pdf/2010.11054; https://aclanthology.org/2021.tacl-1.5; MIT DSpace https://dspace.mit.edu/handle/1721.1/143521
- **Quotes:**
  - "We capture the natural phonological geometry by learning character embeddings based on the International Phonetic Alphabet (IPA)."
  - "For Iberian, the method does not show strong evidence supporting Basque as a related language…"
- **Inputs.** This is the method closest to the Indus problem.
  - Lost side: unsegmented or undersegmented inscriptions. The lost characters are **orthographic tokens and do not need phonetic values**.
  - Known side: a vocabulary of stems in IPA, assumed to be correct.
  - Prior knowledge of the lost script's sound values is optional. The paper defines three levels:
    - base: no knowledge;
    - partial (Gothic): k, l, m, n, p, s, t known;
    - full: all values known.
- **Results.**
  - Gothic–Proto-Germanic: base-model P@10 of 0.865.
  - Ugaritic–Hebrew: P@1 of 0.778.
  - Iberian, matched against Latin personal names: P@10 of about 60% for the base model and about 75% for the full model. Note that Iberian sound values are largely known, because the script is a deciphered semi-syllabary.
  - A "language-closeness" measure correctly picked out the relatives of Gothic and Ugaritic.
- **Failure cases and limits stated.**
  - It handles alphabetic lost scripts only.
  - It compares one language pair at a time.
  - The closeness measure is not conclusive for isolates.
  - The Iberian evaluation relies on personal names only.
- **Code:** https://github.com/j-luo93/DecipherUnsegmented/ (link quoted from the arXiv PDF). My fetch of GitHub was refused, so whether the repo still exists and works is [U].
- **Supporting dataset (third party) [V].** HF dataset `Nacryos/ancient-scripts-datasets` (CC-BY-SA, cites arXiv 2010.11054), https://huggingface.co/datasets/Nacryos/ancient-scripts-datasets/blob/main/docs/DATABASE_REFERENCE.md.
  - It contains a Proto-Dravidian list `dra-pro` with 406 entries, phonemicised following Krishnamurti, sourced from Wiktionary.
  - It contains Proto-Austroasiatic with 180 entries.
  - It has no Munda-specific or Burushaski list visible.
  - It includes a parser for the DSAL edition of the DEDR.

### 1.5 Proto-Elamite (Born, Kelley, Monroe, Sarkar et al.): structural, not phonetic
- **2019, "Sign Clustering and Topic Extraction in Proto-Elamite" (LaTeCH 2019) [V].** https://aclanthology.org/W19-2516/
  - Methods: hierarchical clustering, n-grams and LDA.
  - Quote: the methods "reveal previously-unobserved relationships between signs".
  - The authors present this as an aid to manual decipherment. It decodes nothing.
- **2022, "Sequence Models for Document Structure Identification in an Undeciphered Script" (EMNLP) [V].** https://aclanthology.org/2022.emnlp-main.620
  - It gives the "first thorough analysis of 'header' signs" using unsupervised neural and statistical sequence models.
- **2022/23, Kelley, Born, Monroe & Sarkar, "Image-aware language modeling for Proto-Elamite," *Lingue e linguaggio* 21(2) [V].** https://rivisteweb.it/doi/10.1418/105965
  - Point made: the transliteration a specialist chooses "determines the ways" an algorithm learns sign relations.
  - The authors propose modelling with sign images to reduce that bias.
- **Born's SFU thesis [U].** "Applications of NLP to Archaeological Decipherment: A Survey of Proto-Elamite" (2023), https://summit.sfu.ca/_flysystem/fedora/2023-12/etd22782.pdf. The page was blocked by a bot wall.
- **Code [U].** Papers with Code lists one code implementation for the 2019 paper.
- **Transfer to Indus: high.** The task matches Indus closely: an undeciphered logographic and numerical system with no known language. The output is sign classes and document structure, not readings.

### 1.6 Linear A
- **Nepal & Perono Cacciafoco 2024, "Minoan Cryptanalysis…", *Information* 15(2):73 [V].** https://www.mdpi.com/2078-2489/15/2/73
  - Method:
    - match sign shapes to Carian and Cypriot signs;
    - build a new phonetic grid from those matches;
    - run a brute-force comparison of consonant clusters against Egyptian, Luwian, Hittite, Proto-Celtic and Uralic dictionaries.
  - Result: only 43 sign matches. The authors call the matches "not significantly conclusive".
  - Code: https://github.com/L-Colin/Linear-A-decipherment-programme
- **Manoj & Perono Cacciafoco 2024/25, "Minoan and the Machines", *Annals Univ. Craiova* 46 [V].** https://anale-lingvistica.reviste.ucv.ro/index.php/laucv/article/view/134
  - A review covering min-cost flow, generative phonetic comparison, the brute-force consonant-cluster approach, and feature similarity.
- **Univ. Melbourne MDAP 2024 project, Davis, Tour et al. [V].** https://www.unimelb.edu.au/mdap/research/2024-collaborations/using-deep-neural-network-models-in-the-decipherment-of-linear-a
  - Plan: pre-train on candidate languages, then fine-tune on Linear A.
  - Quote: "The identification of a cognate language for Linear A would lay the groundwork for machine decipherment."
  - No results are published on the page.
- **Di Mino 2026 Semitic/Linear A claim, Python built with Claude Code [V, secondary report].** https://braindetox.kr/en/posts/ai_decodes_linear_a_2026.html
  - The page says the claim is "unverified by the academic community".
  - Critics point to the small corpus and to Cyrus Gordon's earlier rejected Semitic hypothesis.
- **Braović et al. 2024, "A Systematic Review of Computational Approaches to Deciphering Bronze Age Aegean and Cypriot Scripts," *Computational Linguistics* 50(2) [V].** https://aclanthology.org/2024.cl-2.7.pdf
  - It defines 15 challenges and outlines a model that would simulate traditional decipherment.
  - This is the best single survey for this project.

### 1.7 Cypro-Minoan
- **Corazza, Tamburini, Valério & Ferrara 2022, PLOS ONE 17(7) e0269544 [V].** https://cris.unibo.it/handle/11585/897490, with details from Braović 2024.
  - Method: Sign2Vec, a DeepCluster-v2 variant, trained on 2,899 sign images from 213 inscriptions.
  - Finding: the results point toward "the validation of a unitary, single Cypro-Minoan script".
  - This is sign-inventory work, not phonetic decipherment.
  - Code: none given in Braović's review [U].
- **Valério 2016 PhD thesis, Barcelona [V].** https://tesisenred.net/handle/10803/385842
  - Method: manual triangulation, comparing sign forms and values with Linear A and the Cypriot syllabary, plus internal positional and morphological analysis. The values are then tested by transliterating texts and checking them against outside linguistic data.
  - Values proposed for 60 sign forms, of which 9 are "confirmed".
  - Ugarit tablet RS 20.25 is read as a list of names attested in cuneiform.
  - Not a full decipherment, by the author's own statement.
- **Transfer lesson:** for Cypro-Minoan, the anchors that move things forward are again **personal names attested in cuneiform**.

### 1.8 Rongorongo
- **Korovina 2026, "A Computational Evaluation of Syllabic Hypotheses for Rongorongo: Evidence from N-gram Analysis," LT4HALA @ LREC 2026 [V].** https://aclanthology.org/2026.lt4hala-1.16/
  - Method: a genetic algorithm with an n-gram fitness score, calibrated on controlled texts. Fitness correlates with accuracy at 0.75, with a "noise threshold" of 2.5M.
  - Results: the CEIPP transliteration scores well below the noise threshold. The rongopy transliteration falls in a "gray zone".
  - Conclusion: a pure syllabic model appears insufficient.
  - **Methodologically important for this project:** it **calibrates the solver's noise floor on known texts before testing the unknown one**. The Indus experiment below copies this design.
- **Ferrara et al. 2024, Scientific Reports, radiocarbon dating of a Rongorongo tablet [U]** (from search snippets only). Not a computational decipherment.

### 1.9 Linear Elamite: see Part 2. No computational method was involved [V: LRB says the article "does not mention any computational or software-based methods"].

---

## Part 2. How Linear Elamite was deciphered (Desset et al. 2022): its anchor strategy

**Paper.** F. Desset, K. Tabibzadeh, M. Kervran, G. P. Basello & G. Marchesi, "The Decipherment of Linear Elamite Writing," *Zeitschrift für Assyriologie* 112 (2022), doi:10.1515/za-2022-0003.
- The full author list is [U]. I could not open the De Gruyter page.
- The steps below come from the authors' own general-audience article (ANE Today), Wikipedia and the LRB.

**Anchor 1: the "Table au lion" from Susa, 22nd c. BCE.** It carries Akkadian cuneiform and Linear Elamite on the same monument, both of Puzur-Inšušinak. [V]
- ANE Today, https://anetoday.org/desset-irans-linear-elamite-deciphered/: "The starting point for the decipherment of Linear Elamite was provided by a small number of monuments from Susa."
- The cuneiform names the ruler Puzur-Sušinak and the god Inšušinak. The two names share their final part, which helped locate the matching sign sequence.
- Wikipedia (https://en.wikipedia.org/wiki/Linear_Elamite) [V]: Bork (1905, 1924) and Frank (1912) used this monument to get "a fairly certain reading of nine signs".
- The two texts are not word-for-word translations of each other. The anchor is the **shared proper names**.

**Anchor 2: the silver beakers (*gunagi/kunanki*), Mahboubian collection, c. 2050–1850 BCE, unprovenanced.**
- Desset saw a recurring four-sign sequence at the start of the inscriptions. Its first sign was already known as *ši* and its last two signs were identical.
- He tested it against the cuneiform-attested ruler **Šilhaha**: *ši-l-ha-ha*.
- He then read **Eparti/Ebarat** (*e-pa-r-ti*) and the deity **Napiriša**.
- ANE Today [V]: "These three names alone allowed me to read eight additional signs." It also says: "This was the key, and after that, the rest came quite quickly."
- LRB (https://www.lrb.co.uk/the-paper/v47/n04/tom-stevenson/beyond-mesopotamia) [V]: Desset says "without the silver kunanki the decipherment would have been impossible".
- There is no bilingual for the beakers. Desset compared them with contemporary cuneiform objects naming the same rulers.
- Wikipedia [V] compares the method to Grotefend's work on Old Persian: repeated sequences at the start of a text, guessed to be royal names.

**Anchor 3: digraphia and known Elamite.**
- Later Elamite royal inscriptions exist in cuneiform, giving shared names, titles and formulae.
- ANE Today [V] says this "digraphia… is what really made it possible to decipher the Linear Elamite script in the end".
- ANE Today [V] also says the decipherment rested on "a previously established (albeit partial) knowledge of the Elamite language".

**Scale of the claim.**
- LRB [V]: "72 of the 77 hypothesised signs", covering about 96% of sign occurrences.
- The proposed system has 5 vowels, 12 consonants and 60 CV signs. The decipherers claim no logograms.

**Dissent.**
- Wikipedia [V] reports M. Mäder's view that "only around 70 percent" of signs are likely phonographic, the rest being logograms.
- LRB [V] quotes J. Dahl: "It irritates me that this was even published because it's so full of errors."
- There are also concerns about authenticity and provenance.

**What this means for Indus.**
- Every Linear Elamite anchor came from outside the script: names in cuneiform, a language that was partly known, and a mostly phonographic script with about 80 signs.
- Indus has none of these:
  - no digraphic monument;
  - no securely known language;
  - an inventory of 400–700 signs, so it is not mainly phonographic.
- The transferable strategy is the **Grotefend/Desset name hypothesis**:
  1. find recurring sequences in the "name" slot of seals;
  2. pair them with personal names that cuneiform attests for Meluhhans;
  3. check that each sign value stays consistent across independent names.
- The project's existing file `results/agent_cuneiform_anchors_2026-10-22.md` lists those candidate cuneiform-side names. That file also notes there is **no true Indus–cuneiform bilingual**.

---

## Part 3. Indus-specific computational work after about 2015

| Work | What it does | Mark |
|---|---|---|
| **Nair 2026**, "How Non-Linguistic Is the Indus Sign System? A Synthetic-Baseline Scorecard," arXiv:2604.17828 | Compares the Indus corpus with heraldic and administrative synthetic generators and with 7 real non-linguistic corpora. Corpus: 1,916 deduplicated texts, 584 signs, 11,110 tokens (ICIT/Yajnadevam digitisation). Finds Zipf slope −1.49 and conditional entropy 3.23 bits. Quotes: "Neither a heraldic nor an administrative generator can reproduce all four properties at once"; "We do not claim to resolve the linguistic/non-linguistic question." No language candidate tested. Code only "upon acceptance" or by email. | [V] https://arxiv.org/abs/2604.17828 and https://arxiv.org/pdf/2604.17828 |
| **Mukhopadhyay 2019**, "Interrogating Indus inscriptions to unravel their mechanisms of meaning conveyance," *Humanities & Social Sciences Communications* 5 | Argues the texts are mostly logographic, standing for "content-morphemes and functional-morphemes". Sorts logograms into 9 functional classes. Assigns no sound values. | [V] https://ideas.repec.org/a/pal/palcom/v5y2019i1d10.1057_s41599-019-0274-1.html |
| **Palaniappan & Adhikari 2017**, "Deep Learning the Indus Script," arXiv:1702.00523 | Image pipeline, an OCR-style task. Detects the "jar" sign with 92% accuracy. Not decipherment. | [V] https://arxiv.org/abs/1702.00523v1 |
| **Daggumati & Revesz 2019**, "Data Mining Ancient Scripts…," IDEAS '19 | CNN+SVM visual similarity across 8 scripts. Claims Indus is "visually closest to Sumerian pictographs". Used only 23 Indus signs. Shape similarity is not phonetic evidence. | [V] https://cse.unl.edu/~revesz/papers/IDEAS19-a26.pdf |
| **Geetha Ramani & Keerthi Kumar 2024**, IJCA 186(30) | Positional n-grams, MSA, VAE and k-means on ICIT. No sound values or language claimed. | [V] https://www.ijcaonline.org/archives/volume186/number30/deciphering-the-indus-script-computational-linguistic-techniques-and-positional-n-gram-analysis/ |
| **Rao, Yadav et al. 2009–2010** (Science, PNAS, PLoS One, CL 36(4) reply) | Conditional and block entropy, Markov and n-gram models. Rao's own page concedes "barring a full decipherment, one cannot prove either the linguistic or nonlinguistic thesis" and that estimates beyond N=6 are unreliable. These papers predate 2015 but are the baseline for all later work. | [V] https://homes.cs.washington.edu/~rao/IndusCompLing.html |
| **Sproat 2014**, "On statistical measures and ancient writing systems," *Language* | A critique of the entropy arguments, using non-linguistic corpora. | [U]: abstract page blocked |
| **Fuls** (TU Berlin), ICIT/epigraphic database | 2025 IMSc talk: "a relational database under development since 1990"; "comparison of known and unknown writing systems by entropic redundancy". | [V] https://www.imsc.res.in/~sitabhra/meetings/bitsscripts25/ |
| **IMSc 2nd Workshop on Computational Epigraphy**, Chennai, March 2025 | Talks by Fuls, Wells (ICIT), Yadav, Ashraf (recurring segments), Pal (unsupervised symbol classification), Siddharthan. | [V] same URL |
| **Yajnadevam 2024**, "A cryptanalytic decipherment of the Indus script" | Treats Indus as a substitution cipher for Sanskrit. Uses regex matching against a Sanskrit dictionary, set intersection, and a "unicity distance" of about 471 computed with 330 signs and redundancy 0.7. Claims "we translate 500+ inscriptions". **Not peer-reviewed.** The method assumes one sign = one sound. With hundreds of signs and a flexible dictionary that includes compounds and inflected forms, the search space makes spurious fits easy. | [V] https://rarebooksocietyofindia.org/book_archive/A_cryptanalytic_decipherment_of_the_Indu.pdf |
| **glossa-lab (BitConcepts)**, GitHub plus Zenodo preprint | Claims "161 H+M candidate readings", Proto-Dravidian, "90.96% of Holdat IVS tokens", "z=10.3" for positional grammar. Validation is self-reported, and agreement with Parpola is partly circular. Marked "Seeking peer review." Uses "SA-based sign-to-phoneme hypothesis generation" (SA undefined; perhaps simulated annealing [U]). LLM used as an assistant only. | [V] https://github.com/BitConcepts/glossa-lab |
| "A Computational Decipherment Hypothesis for the Indus Script: 185 Proto-Dravidian Readings Validated Across Two Independent Corpora" (ResearchGate 405297740) | Title seen in search only; probably related to glossa-lab [U]. | [U] |
| AI-EPIGRAPHY, ACM 2025 (doi 10.1145/3768633.3770145) | "Interactive Tool for Computational Decipherment of the Indus Valley Script." The page failed to load. | [U] |

---

## Part 4. Has anyone applied a phonetic-prior method to Indus with candidate languages?

**I found no such study. This is a negative search result, not proof of absence.**

**Searches run:**
- "Indus script phonetic prior Luo neural decipherment Proto-Dravidian experiment" (extended)
- "DecipherUnsegmented OR phonetic prior Indus script Dravidian Munda test"
- "Indus Proto-Dravidian cognate model unsupervised decipherment experiment Luo Barzilay applied Indus valley script result" (extended)
- "Indus script computational decipherment cognate Dravidian Munda statistical test language candidate 2024 2025 paper" (extended)

**What the searches returned:** only Parpola's manual rebus work, Yajnadevam (Sanskrit cipher), glossa-lab (Proto-Dravidian, its own method), and non-scholarly AI posts.

**Checks on the papers themselves:**
- The Luo et al. 2021 abstract and MIT DSpace record do not mention Indus [V: https://dspace.mit.edu/handle/1721.1/143521].
- The Nair 2026 scorecard names no language candidate [V].

**Closest analogue:** Luo 2021 on Iberian, a real undeciphered language with partly known sound values. It came back inconclusive (no strong Basque link).

**Why nobody has done it (my analysis):**
- The method's assumptions break on Indus:
  - the lost script must be alphabetic or phonographic;
  - stems must map character to character;
  - there must be enough distinct word types.
- Indus is probably logo-syllabic with 400–700 signs. Its texts average about 5 signs and are dominated by names, titles and formulae.
- If most signs are logograms, a character-level cognate model has nothing to align. It may still "find" a closest language through Zipf and length artefacts.

---

## Part 5. The single most feasible computational experiment

**Name:** *Discrimination-power test for language-closeness under Indus-like conditions*. This is a calibration study, the same design as Korovina 2026's noise floor.

**Question:** If the hidden language were Dravidian, or Indo-Aryan, could a phonetic-prior / cognate-matching model tell which one, given:
- Indus-like text length (about 5 signs);
- corpus size (about 4,000 texts, 2–3k unique sequences);
- sign inventory of about 400–700 signs, a logo-syllabic mix;
- no word boundaries?

If it cannot do so on known languages, no Indus result from such a model means anything.

**Design:**
1. **Controls with known answers.** Use the repo's role-tagged corpora:
   - `data/tamil_brahmi/` (Dravidian: 110 inscriptions plus 75 short legends);
   - `data/prakrit_eiad/` (Indo-Aryan: 167 inscriptions).
   - Restrict both to name and title strings, which is how Indus seals are thought to work.
2. **Re-encode each control into a pseudo-Indus script.**
   - Replace a chosen share of frequent words or morphemes with single "logogram" tokens: for example 0%, 30%, 60% and 90% logography.
   - Write the rest as CV-syllable tokens.
   - Remove spaces.
   - Shuffle token IDs so that no phonetic information remains.
   - Truncate or sample to match the Indus length distribution (from `data/indus_website_real_corpus.csv` and the ICIT merged corpus).
3. **Run the matcher** against several known-side IPA stem lists:
   - Proto-Dravidian, or Old Tamil;
   - Old Indo-Aryan or Pali/Prakrit;
   - a distractor such as Proto-Austroasiatic or Sumerian;
   - a shuffled-phoneme null.
   - Matcher choices: Luo 2021 DecipherUnsegmented, the base model with no sound values; or, as a lighter fallback, the Berg-Kirkpatrick & Klein 2011 matcher.
   - Record the language-closeness score and its rank, over many random seeds.
4. **Output.** A table showing, for each logography level, whether the true family ranks first more often than chance. This gives an empirical false-positive and false-negative rate.
5. **Only if** discrimination survives at realistic logography levels: run the same pipeline on the real Indus corpus, and report closeness with the calibrated error bars from steps 1–4.

**Required inputs, and status:**

| Input | Status |
|---|---|
| Indus corpus as sign-ID sequences | **Have**: `data/indus_website_real_corpus.csv` (2,543 rows), `data/icit_merged_paragorth/` |
| Dravidian control corpus (word-segmented, roles) | **Have**: `data/tamil_brahmi/` |
| Indo-Aryan control corpus | **Have**: `data/prakrit_eiad/` |
| Proto-Dravidian IPA stem list | **Partly**: 406-entry Wiktionary-derived `dra-pro` in the HF dataset [V]. DEDR on DSAL is searchable but has no bulk download [V: https://dsal.uchicago.edu/dictionaries/burrow/index.html]. A third-party DEDR scraper exists (HF `parse_dedr.py`) [V]. A Krishnamurti 2003 reconstruction list in IPA is **missing**. |
| Old Indo-Aryan / Prakrit IPA stem list | **Missing** in the repo. It is derivable from public sources such as CDIAL on DSAL [U] or Wiktionary, but not yet assembled. |
| Munda (Proto-Munda) IPA list | **Missing.** Only Proto-Austroasiatic (180 entries) is in the HF set [V]. |
| Burushaski list | **Missing.** |
| Working Luo 2021 code | Repo URL cited in the paper [V]. It is 2020-era PyTorch, and whether it still runs is [U]. Needs a GPU or a long CPU run. |
| A logogram-vs-phonetic split of Indus signs | **Missing / hypothetical.** This is why the experiment sweeps the logography level instead of assuming one. |
| Word segmentation of Indus texts | **Missing.** The model infers segmentation, but on 5-sign texts that inference is weak. |

**Honest estimate of what it could show:**
- **Most likely outcome, in my judgment: a negative power result.** Once logography passes some moderate level (perhaps 30–50%) and texts are about 5 tokens long, the closeness score will probably stop separating Dravidian from Indo-Aryan controls.
- That is still a publishable and useful finding. It would show, with numbers, that phonetic-prior decipherment cannot settle the Indus language question on the current corpus. It would also be grounds to reject claims (Sanskrit-cipher, Proto-Dravidian "readings") that rest on looser versions of the same matching.
- **Best realistic case:** discrimination survives at low logography. The Indus run then gives a *weak, calibrated* preference for one family. That is evidence about the language, not a decipherment, and it would assign no confirmed sound value to any sign.
- **What it cannot do:** produce readings. Every real decipherment, including Linear Elamite in 2022, needed external name anchors with known pronunciations. For Indus, the only candidates are Meluhhan names in cuneiform, and none sits on a bilingual object.

---

## Sources fetched this session ([V])
- https://pages.cs.wisc.edu/~bsnyder/papers/bsnyder_acl2010.pdf
- https://aclanthology.org/D11-1029.pdf
- https://arxiv.org/pdf/1906.06718
- https://arxiv.org/pdf/2010.11054 ; https://dspace.mit.edu/handle/1721.1/143521
- https://aclanthology.org/W19-2516/ ; https://natlang.cs.sfu.ca/posts/2019-09-17-Logan-PE
- https://aclanthology.org/2022.emnlp-main.620
- https://rivisteweb.it/doi/10.1418/105965
- https://www.mdpi.com/2078-2489/15/2/73
- https://anale-lingvistica.reviste.ucv.ro/index.php/laucv/article/view/134
- https://www.unimelb.edu.au/mdap/research/2024-collaborations/using-deep-neural-network-models-in-the-decipherment-of-linear-a
- https://braindetox.kr/en/posts/ai_decodes_linear_a_2026.html
- https://aclanthology.org/2024.cl-2.7.pdf
- https://cris.unibo.it/handle/11585/897490
- https://tesisenred.net/handle/10803/385842
- https://aclanthology.org/2026.lt4hala-1.16/
- https://anetoday.org/desset-irans-linear-elamite-deciphered/
- https://en.wikipedia.org/wiki/Linear_Elamite
- https://www.lrb.co.uk/the-paper/v47/n04/tom-stevenson/beyond-mesopotamia
- https://languagelog.ldc.upenn.edu/nll/?p=56019 ; https://languagelog.ldc.upenn.edu/nll/?p=73472
- https://arxiv.org/abs/2604.17828 ; https://arxiv.org/pdf/2604.17828
- https://ideas.repec.org/a/pal/palcom/v5y2019i1d10.1057_s41599-019-0274-1.html
- https://arxiv.org/abs/1702.00523v1
- https://cse.unl.edu/~revesz/papers/IDEAS19-a26.pdf
- https://www.ijcaonline.org/archives/volume186/number30/deciphering-the-indus-script-computational-linguistic-techniques-and-positional-n-gram-analysis/
- https://homes.cs.washington.edu/~rao/IndusCompLing.html
- https://www.imsc.res.in/~sitabhra/meetings/bitsscripts25/
- https://rarebooksocietyofindia.org/book_archive/A_cryptanalytic_decipherment_of_the_Indu.pdf
- https://github.com/BitConcepts/glossa-lab
- https://huggingface.co/datasets/Nacryos/ancient-scripts-datasets/blob/main/docs/DATABASE_REFERENCE.md ; .../scripts/parsers/parse_dedr.py
- https://dsal.uchicago.edu/dictionaries/burrow/index.html
