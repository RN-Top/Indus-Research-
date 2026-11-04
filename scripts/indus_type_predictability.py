"""Where does sign-sequence structure carry information on Indus objects?
Target: object family (SEAL, TAB:B, TAB:I, POT, other). Features: sign bigrams + first/last sign.
Same naive Bayes, 5-fold CV, 200 label shuffles. Uses seq_strong (strong-merge reading).
"""
import json, random, ast, collections, math, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
rows = json.load(open(ROOT / "data/icit_merged_paragorth/merged-corpus-canonical.json"))
def fam(t):
    if t.startswith("SEAL"): return "SEAL"
    if t in ("TAB:B", "TAB:I"): return t
    if t.startswith("POT"): return "POT"
    return None
docs = []
for r in rows:
    f = fam(r["type"])
    s = r["seq_strong"]
    if isinstance(s, str):
        try: s = ast.literal_eval(s)
        except Exception: continue
    s = [str(x) for x in s]
    if f and len(s) >= 2:
        docs.append((f, s))
def feats(s):
    return [f"{a}|{b}" for a, b in zip(s, s[1:])] + [f"^{s[0]}", f"${s[-1]}"]
def train(X, y):
    cnt = {c: collections.Counter() for c in set(y)}; pri = collections.Counter(y); V = set()
    for f, c in zip(X, y): cnt[c].update(f); V.update(f)
    tot = {c: sum(cnt[c].values()) for c in cnt}
    return cnt, pri, V, tot
def pred(m, f):
    cnt, pri, V, tot = m; n = sum(pri.values()); best = None; bl = -1e18
    for c in cnt:
        lp = math.log(pri[c] / n) + sum(math.log((cnt[c][x] + 1) / (tot[c] + len(V) + 1)) for x in f)
        if lp > bl: best, bl = c, lp
    return best
def cv(X, y, seed, k=5):
    idx = list(range(len(y))); random.Random(seed).shuffle(idx)
    ok = 0
    for i in range(k):
        te = set(idx[i::k]); m = train([X[j] for j in idx if j not in te], [y[j] for j in idx if j not in te])
        ok += sum(pred(m, X[j]) == y[j] for j in te)
    return ok / len(y)
X = [feats(s) for _, s in docs]; y = [f for f, _ in docs]
maj = collections.Counter(y).most_common(1)[0][1] / len(y)
acc = cv(X, y, 7)
sr = random.Random(8); nulls = []
for _ in range(200):
    ys = y[:]; sr.shuffle(ys); nulls.append(cv(X, ys, 9))
print(json.dumps({"n": len(y), "counts": dict(collections.Counter(y)), "majority": round(maj, 3),
    "accuracy": round(acc, 3), "null_mean": round(sum(nulls) / len(nulls), 3),
    "p_one_sided": round(sum(v >= acc for v in nulls) / len(nulls), 4)}, indent=2))
