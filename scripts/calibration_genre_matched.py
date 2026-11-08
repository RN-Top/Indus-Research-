"""Genre-matched calibration: name and title roles only, formula stems removed.

Formula stems = stems occurring in >= FORMULA_MIN texts across both corpora (data-driven,
so no hand list). Then the same encoding and classifier as calibration_family_discrimination.py.
"""
import json, random, sys, collections, pathlib, math, unicodedata
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
ROOT = pathlib.Path(__file__).resolve().parent.parent
TAMIL = ROOT / "data/tamil_brahmi/corpus_roles.jsonl"
PRAK = ROOT / "data/prakrit_eiad/tagged_roles.jsonl"
KEEP_ROLES = {"PERSONAL_NAME", "TITLE_OR_OCCUPATION"}
FORMULA_MIN = 10
WIN = 5
LEVELS = [0.0, 0.3, 0.6, 0.9]
N_SHUFFLE = 200

def fold(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

def load():
    docs = []
    for path, fam in [(TAMIL, "tamil"), (PRAK, "prakrit")]:
        for line in path.read_text().splitlines():
            r = json.loads(line)
            words = [(w["stem"], w["form"]) for w in r["words"] if w.get("role") in KEEP_ROLES]
            if words:
                docs.append((fam, words))
    df = collections.Counter()
    for _, words in docs:
        df.update({s for s, _ in words})
    formula = {s for s, n in df.items() if n >= FORMULA_MIN}
    out = []
    for fam, words in docs:
        w2 = [(s, f) for s, f in words if s not in formula]
        if w2:
            out.append((fam, w2))
    return out, formula

def encode(words, p, rng, logo):
    toks = []
    for stem, form in words:
        if rng.random() < p:
            logo.setdefault(stem, f"<L{len(logo)}>")
            toks.append(logo[stem])
        else:
            toks.extend(list(fold(form.lower())))
    return toks[:WIN]

def bigrams(t):
    return [f"{a}|{b}" for a, b in zip(t, t[1:])] + [f"^{t[0]}"]

def train(X, y):
    cnt = {c: collections.Counter() for c in set(y)}
    pri = collections.Counter(y)
    vocab = set()
    for f, c in zip(X, y):
        cnt[c].update(f); vocab.update(f)
    tot = {c: sum(cnt[c].values()) for c in cnt}
    return cnt, pri, vocab, tot

def predict(m, f):
    cnt, pri, vocab, tot = m
    V = len(vocab) + 1; n = sum(pri.values())
    best, bl = None, -1e18
    for c in cnt:
        lp = math.log(pri[c] / n)
        for x in f:
            lp += math.log((cnt[c][x] + 1) / (tot[c] + V))
        if lp > bl: best, bl = c, lp
    return best

def cv(X, y, rng, k=5):
    idx = list(range(len(y))); rng.shuffle(idx)
    folds = [idx[i::k] for i in range(k)]; ok = 0
    for fo in folds:
        ts = set(fo)
        m = train([X[i] for i in idx if i not in ts], [y[i] for i in idx if i not in ts])
        ok += sum(predict(m, X[i]) == y[i] for i in fo)
    return ok / len(y)

docs, formula = load()
print(f"kept texts: {len(docs)}  tamil={sum(f=='tamil' for f,_ in docs)} prakrit={sum(f=='prakrit' for f,_ in docs)}")
print(f"formula stems removed ({len(formula)}): {sorted(formula)}")
res = {}
for p in LEVELS:
    rng = random.Random(7); logo = {}
    X, y = [], []
    for fam, words in docs:
        t = encode(words, p, rng, logo)
        if len(t) >= 2:
            X.append(bigrams(t)); y.append(fam)
    acc = cv(X, y, random.Random(7))
    sr = random.Random(8); nulls = []
    for _ in range(N_SHUFFLE):
        ys = y[:]; sr.shuffle(ys); nulls.append(cv(X, ys, random.Random(sr.random())))
    res[p] = dict(n=len(y), majority=round(max(y.count('tamil'), y.count('prakrit'))/len(y), 3),
                  accuracy=round(acc, 3), null_mean=round(sum(nulls)/len(nulls), 3),
                  p_one_sided=round(sum(v >= acc for v in nulls)/len(nulls), 4))
print(json.dumps(res, indent=2))
