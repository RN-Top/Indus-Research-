"""Genre scouting (EXPLORATION only): can the object type (seal / tablet / other) be predicted from the inscription,
and from position-only features? 5-fold cross-validation within the exploration split, grouped by exact text so
identical texts never sit on both sides. Baseline: always predict the majority class; and labels shuffled."""
import json, sys
from collections import Counter
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
from indus_workbench import data  # noqa: E402
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.metrics import balanced_accuracy_score

H = json.load(open(ROOT / "hypotheses/H-2026-10-16-51b7445b.json"))["params"]
O, C, N = set(H["openers"]), set(H["closers"]), set(H["numerals"])

def pos_feats(s):
    f = {"len": min(len(s), 8), "first_opener": s[0] in O, "last_closer": s[-1] in C, "has_numeral": any(x in N for x in s),
         "first_numeral": s[0] in N, "last_numeral": s[-1] in N}
    f["last=" + (s[-1] if s[-1] in C else "other")] = 1
    return f

def sign_feats(s):
    f = pos_feats(s)
    for x in set(s): f["has_" + x] = 1
    f["first=" + s[0]] = 1; f["last=" + s[-1]] = 1
    return f

def main():
    raw, _ = data.load_raw("indus_website")
    c = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"), drop_damaged=True, dedupe=False, drop_unidentified=True)
    e = data.explore_only(c).df
    e = e[e.signs.map(len) >= 1].copy()
    e["y"] = e.object_type.map(lambda t: t if t in ("seal", "tablet") else "other")
    y = e.y.values; groups = e.signs.map(" ".join).values
    print("classes:", dict(Counter(y)), "majority baseline", f"{Counter(y).most_common(1)[0][1]/len(y):.1%}")
    rng = np.random.default_rng(1); out = {}
    for name, fn in [("position-only features", pos_feats), ("position + which signs", sign_feats)]:
        X = DictVectorizer().fit_transform([fn(list(s)) for s in e.signs])
        def cv(labels):
            pred = np.empty(len(labels), dtype=object)
            for tr, te in GroupKFold(5).split(X, labels, groups):
                m = LogisticRegression(max_iter=2000, class_weight="balanced").fit(X[tr], labels[tr])
                pred[te] = m.predict(X[te])
            return balanced_accuracy_score(labels, pred)
        acc = cv(y); shuf = [cv(rng.permutation(y)) for _ in range(20)]
        print(f"  {name}: balanced accuracy {acc:.1%} (chance 33.3%); labels shuffled {np.mean(shuf):.1%} (max {max(shuf):.1%})")
        out[name] = dict(acc=acc, shuffled=float(np.mean(shuf)))
    (ROOT / "results" / "genre_scouting.json").write_text(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
