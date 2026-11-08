"""Calibration: can a family signal survive Indus-like re-encoding?

Controls: Tamil-Brahmi (Dravidian, data/tamil_brahmi) vs Prakrit (Indo-Aryan, data/prakrit_eiad).
Re-encoding: texts are cut to 5 tokens (Indus-like length); a share p of word tokens is replaced
by a logogram ID (one ID per stem, random, carrying no phonetic value); the rest are written as
character tokens with no word breaks.
Classifier: character-bigram naive Bayes, 5-fold CV, with a label-shuffled null.

This is a first calibration, not the full matcher test. It does not use any stem list.
"""
import json, random, sys, collections, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TAMIL = ROOT / "data/tamil_brahmi/corpus_roles.jsonl"
PRAK = ROOT / "data/prakrit_eiad/tagged_roles.jsonl"
WIN = 5
LEVELS = [0.0, 0.3, 0.6, 0.9]
SEED = 7
N_SHUFFLE = 200


def load():
    docs = []
    for line in TAMIL.read_text().splitlines():
        r = json.loads(line)
        words = [(w["stem"], w["form"]) for w in r["words"]]
        docs.append(("tamil", words))
    for line in PRAK.read_text().splitlines():
        r = json.loads(line)
        words = [(w["stem"], w["form"]) for w in r["words"]]
        if words:
            docs.append(("prakrit", words))
    return docs


def encode(words, p, rng, logo_ids):
    toks = []
    for stem, form in words:
        if rng.random() < p:
            if stem not in logo_ids:
                logo_ids[stem] = f"<L{len(logo_ids)}>"
            toks.append(logo_ids[stem])
        else:
            toks.extend(list(form.lower()))
    # word breaks removed; cut to window
    return toks[:WIN]


def train_nb(X, y):
    counts = {c: collections.Counter() for c in set(y)}
    prior = collections.Counter(y)
    vocab = set()
    for feats, c in zip(X, y):
        counts[c].update(feats)
        vocab.update(feats)
    totals = {c: sum(counts[c].values()) for c in counts}
    return counts, prior, vocab, totals


def predict_nb(model, feats):
    counts, prior, vocab, totals = model
    best, bestlp = None, -1e18
    V = len(vocab) + 1
    n = sum(prior.values())
    for c in counts:
        lp = math.log(prior[c] / n)
        for f in feats:
            lp += math.log((counts[c][f] + 1) / (totals[c] + V))
        if lp > bestlp:
            best, bestlp = c, lp
    return best


def bigrams(toks):
    return [f"{a}|{b}" for a, b in zip(toks, toks[1:])] + [f"^{toks[0]}"] if toks else []


def cv_accuracy(X, y, rng, k=5):
    idx = list(range(len(y)))
    rng.shuffle(idx)
    folds = [idx[i::k] for i in range(k)]
    correct = 0
    for f in folds:
        test = set(f)
        tr_X = [X[i] for i in idx if i not in test]
        tr_y = [y[i] for i in idx if i not in test]
        model = train_nb(tr_X, tr_y)
        for i in f:
            correct += predict_nb(model, X[i]) == y[i]
    return correct / len(y)


def main():
    docs = load()
    rng = random.Random(SEED)
    results = {}
    for p in LEVELS:
        logo_ids = {}
        X, y = [], []
        for fam, words in docs:
            toks = encode(words, p, rng, logo_ids)
            if len(toks) < 2:
                continue
            X.append(bigrams(toks))
            y.append(fam)
        base = collections.Counter(y).most_common(1)[0][1] / len(y)
        acc = cv_accuracy(X, y, random.Random(SEED))
        null = []
        srng = random.Random(SEED + 1)
        for _ in range(N_SHUFFLE):
            ys = y[:]
            srng.shuffle(ys)
            null.append(cv_accuracy(X, ys, random.Random(srng.random())))
        null_mean = sum(null) / len(null)
        frac_ge = sum(n >= acc for n in null) / len(null)
        results[p] = dict(n=len(y), n_tamil=y.count("tamil"), n_prakrit=y.count("prakrit"),
                          majority=round(base, 3), accuracy=round(acc, 3),
                          null_mean=round(null_mean, 3), p_one_sided=round(frac_ge, 4))
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    sys.exit(main())
