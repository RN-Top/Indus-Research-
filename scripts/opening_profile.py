"""Opening/closing profile across corpora (F5, F1r, F2 of drafts/dravidian_opening_PREDICTIONS.md).
EXPLORATION only: Indus exploration split, Mesopotamian exploration split.

    python scripts/opening_profile.py [cdli_data_folder]
"""
import json, re, sys, unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if not unicodedata.combining(c)).lower())


def words(fn):
    out = []
    for line in open(fn):
        t = [norm(w.get("stem") or w["form"]) for w in json.loads(line).get("words", [])]
        t = [x for x in t if x]
        if t:
            out.append(t)
    return out


def profile(texts):
    T = [t for t in texts if len(t) >= 2]
    freq = Counter(x for t in texts for x in t)
    first = Counter(t[0] for t in T); last = Counter(t[-1] for t in T)
    f5 = sum(c for _, c in first.most_common(5)) / len(T)
    f2 = sum(c for _, c in last.most_common(5)) / len(T)
    rf = sum(freq[t[0]] <= 5 for t in T) / len(T)
    rest = [x for t in T for x in t[1:]]
    rr = sum(freq[x] <= 5 for x in rest) / len(rest)
    return dict(texts=len(T), F5=f5, F2=f2, rare_first=rf, rare_rest=rr, F1r=rf / rr if rr else float("nan"),
                top_first=first.most_common(5), top_last=last.most_common(5))


def main():
    corpora = {
        "Old Tamil, caves": words(ROOT / "data/tamil_brahmi/corpus_roles.jsonl"),
        "Old Tamil, objects": words(ROOT / "data/tamil_brahmi/objects_roles.jsonl"),
        "Prakrit (EIAD)": words(ROOT / "data/prakrit_eiad/tagged_roles.jsonl"),
    }
    from functional_slots import load
    corpora["Indus (exploration)"] = [list(s) for s in load()["signs"] if len(s)]
    if len(sys.argv) > 1:
        sys.path.insert(0, str(Path(sys.argv[1]).parent))
        import importlib.util
        spec = importlib.util.spec_from_file_location("mes_load", sys.argv[2] if len(sys.argv) > 2 else "mes_load.py")
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        corpora["Mesopotamian seal legends (exploration)"] = [t for t, sp in m.legends(sys.argv[1]) if sp == "explore"]
    out = {}
    for k, T in corpora.items():
        p = profile(T); out[k] = p
        print(f"{k:42} texts {p['texts']:5}  F5 {p['F5']:.0%}  F1r {p['F1r']:.2f} (rare first {p['rare_first']:.0%} vs rest {p['rare_rest']:.0%})  F2 {p['F2']:.0%}")
        print(f"{'':42} first: {p['top_first']}")
    (ROOT / "results" / "opening_profile.json").write_text(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
