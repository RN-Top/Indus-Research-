# Scouting: comparison corpora for the "function theory"

*Scouting note, not results. 15 October 2026. No comparison data has been downloaded into the project and no cross-script analysis has been run. Nothing registered; the holdout was not touched.*

## The idea being prepared

The opener → content → closer skeleton holds across every Indus site (`functional_by_site.md` D). The "function theory" asks whether **other ancient administrative and seal scripts** show the same skeleton, because it follows from what seals and tablets *do* rather than from any one language.

The plan is to run the same slot-learning code on a comparison corpus. Corpora whose meaning is **already known** are the most valuable, because they give an answer key: if the code finds "openers" and "closers" there, we can check whether they really are headings and endings.

## What the existing code needs

A table of texts, one row per text, each a list of sign IDs in reading order. Site and object type are optional extras. That is what `scripts/functional_skeleton.py` and the `template_order` test kind read.

## Candidates

| Corpus | What it is | Where | Licence and terms | Size | Format | Fit |
|---|---|---|---|---|---|---|
| **Proto-Elamite tablets** (Iran, about 3100–2900 BCE; undeciphered accounting) | Administrative tablets: header, numbered entries, sometimes a final "subscript" | [sfu-natlang/pe-headers](https://github.com/sfu-natlang/pe-headers) (Born et al., [EMNLP 2022](https://aclanthology.org/2022.emnlp-main.620.pdf)); texts from CDLI | Repository states no licence. The underlying CDLI texts: "may be freely copied, aggregated and re-used according to common and fair academic practice", citing CDLI ([terms](https://cdli.earth/terms-of-use)) | **1,467 texts**, about 26,000 readable tokens | One ATF file per tablet. Signs `M001`–`M521`; numerals as `1(N14)`; damage marks. **Headers already labelled** by experts (`# header`, `data.csv`), and subscripts marked | **Best first candidate.** Built-in answer key: experts have marked where headers are |
| **Proto-cuneiform** (Uruk IV–III, about 3300–3000 BCE; the earliest Mesopotamian accounting) | Account tablets | [Nino-cunei/uruk](https://github.com/Nino-cunei/uruk) (Text-Fabric; [DOI 10.5281/zenodo.1482791](https://doi.org/10.5281/zenodo.1482791)); texts from CDLI | Code MIT; data "derived from CDLI" (CDLI terms as above) | Several thousand tablets (exact count to check) | ATF in `sources/`, and Text-Fabric features | Good. Same family of tools as Proto-Elamite; a natural neighbour of the Indus period |
| **Mesopotamian seal legends** (e.g. Ur III seals: "Name / title / son of Name2 / servant of King or God") | Short seal inscriptions with **known meaning** | [CDLI Seal portal](https://cdli.earth/artifacts/seals); the full dump is at [cdli-gh/data](https://github.com/cdli-gh/data) | CDLI terms as above | Large (thousands); the seal subset needs filtering | One large ATF dump in Git LFS (last updated August 2022) plus a catalogue CSV. Transliterated Sumerian and Akkadian, not sign IDs | **Most important for the theory**, being seals of the same era with a known slot structure. More work, and the LFS download may be blocked here |
| **Linear B** (Mycenaean Greek, about 1400–1200 BCE; **deciphered** administrative tablets) | Accounting tablets with known language | [DAMOS](https://damos.hf.uio.no/about/online/) (Oslo) | Content CC BY-NC-SA 4.0; software GPL-3.0 | All published Mycenaean texts | Searchable online; **no documented bulk download** | Strong positive control (known language, administrative), but access is uncertain. Ask DAMOS for an export |
| **Linear A** (Minoan, undeciphered) | Mostly short administrative and libation texts | [SigLA](https://sigla.phis.me/about.html) (CC BY-NC-SA 4.0); [HF ancient-scripts-datasets](https://huggingface.co/datasets/Nacryos/ancient-scripts-datasets/blob/main/data/linear_a/README.md) (CC BY-SA 4.0) | As listed | The Hugging Face set is only 60 libation (Za) inscriptions; SigLA is palaeographic | Syllabic transliterations split into words | Limited: the open part is small and mostly religious formulas, not accounting |
| **Cretan Hieroglyphic seals** | Seal inscriptions, a close analogue to Indus seals | Print corpus (CHIC, 1996); [DBAS](https://www.sagas.unifi.it/vp-386-dbas-chs-cretan-hieroglyphic-seals.html) database | No open dataset found | About 300 inscriptions (print) | Not machine-readable openly | Not usable without manual entry |

**Gap.** No open, machine-readable **non-linguistic** comparison system was found, such as heraldry, potters' marks or Vinča signs. Rao et al. used several in their entropy work, but did not release them openly as far as this scouting found. A non-linguistic control remains on the wish list.

## Work each would need

1. **Proto-Elamite** (small; about half a day):
   - Parse the 1,467 ATF files and keep sign tokens.
   - Decide how to treat numerals: keep them as a numeral class, as with Indus strokes.
   - Drop damage markers and broken texts.
   - Write a `data/` CSV with the same columns as the Indus corpus.
   - Use the expert header labels and the subscript markers as the answer key. The size is about 0.4 MB of text and could be fetched via git (GitHub is reachable from here).
   - **Caveat:** these are long, multi-entry accounts, not 5-sign seals. The comparison should be made at the level of the whole tablet (heading → entries → subscript) and, separately, at the level of each entry.
2. **Proto-cuneiform (Uruk):** similar ATF parsing, but bigger and more varied in genre. Choose administrative accounts only. About a day.
3. **Mesopotamian seal legends** (largest; one to two days):
   - Obtain the CDLI dump (Git LFS; access from here not yet confirmed).
   - Filter to seal inscriptions using the catalogue.
   - Tokenise into words or signs.
   - Tag the known parts (name, title, filiation, "servant of") as the answer key.
   - This is the direct test of "same job, same shape": short seal legends of the same era, with known meaning.
4. **Linear B:** request an export from DAMOS, or check whether its texts are in another open dump. Access first, then about a day.

## Recommended order

1. **Proto-Elamite first.** It is quick, open, has expert labels, and is a contemporary undeciphered accounting script.
2. **Mesopotamian seal legends second.** It is the true seal-to-seal comparison, with meaning known.
3. Then Linear B as the deciphered-administrative control, if DAMOS can provide data.

The safeguards carry over:

- **Fix the comparison method before looking at results**, and use the same role rule (`functional_by_site.md` D.1) unchanged.
- **Report both outcomes.** A skeleton that does not appear elsewhere is also a finding.
- **Keep these analyses separate from the Indus holdout.** They are different corpora with their own correction family.
