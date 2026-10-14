"""Re-run the descriptive checks (results sections 1-2) on the current data.

Entropy at block sizes 1-3 against the three null models; bigram vs unigram
cross-validated on the exploration split against a shuffled control; the
most frequent sign's share at text end. Prints a Markdown table.
"""

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from indus_workbench import controls, data, entropy, hypotheses as hy, markov, stats  # noqa: E402


def main() -> None:
    print("| Corpus | Texts | Signs | H2 Indus | H2 within-shuffle | Bigram gain (bits/sign, folds) | Shuffled gain | Top sign at end vs chance |")
    print("|---|---|---|---|---|---|---|---|")
    for key in ["indus_website", "cisi_base", "cisi_allograph"]:
        raw, _ = data.load_raw(key)
        c = data.build_corpus(raw, key, collapse_variants=data.SOURCES[key].get("collapse_variants", False),
                              metadata=data.load_metadata(key))
        seqs, L = c.sequences, len(c.sign_inventory)
        h2 = entropy.block_entropy(seqs, 2, L)
        ws = np.mean([entropy.block_entropy(controls.shuffle_within_texts(seqs, controls.rng(k)), 2, L)
                      for k in range(10)])
        ex = data.explore_only(c)
        cv = markov.cross_validate(ex.sequences, 5)
        cvs = markov.cross_validate(controls.shuffle_within_texts(ex.sequences, controls.rng(1)), 5)
        top = stats.sign_frequencies(ex.sequences).sign.iloc[0]
        r = hy.run_test(hy.new_hypothesis("position", {"a": top, "where": "end"}, "x", n_perm=2000), ex.df)
        print(f"| {key} | {c.n_texts:,} | {L} | {h2:.3f} | {ws:.3f} | {cv['mean_gain_bits']:.2f} "
              f"({cv['folds_bigram_better']}/5) | {cvs['mean_gain_bits']:.2f} ({cvs['folds_bigram_better']}/5) | "
              f"{top}: {r.observed:.2f} vs {r.null_mean:.2f} (p {r.p_value:.4f}) |")


if __name__ == "__main__":
    main()
