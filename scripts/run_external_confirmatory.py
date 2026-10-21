"""Confirmatory tests on the comparison scripts' locked holdouts (Proto-Elamite, Mesopotamian seals).

Registered hypotheses with "type": "external" (hypotheses/H-*.json) are run here,
once each; scripts/run_confirmatory.py skips them. The p-values join the same
Benjamini-Hochberg correction across every confirmatory test ever run, and the
results are written as results/confirmatory_<date>[_k].json in the same format,
so later runs of either script include them.

The source corpora are not in this repository (CDLI terms): pass their folders.

    python scripts/run_external_confirmatory.py --pe /path/to/pe-headers/corpus --cdli /path/to/cdli_data
"""

import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from indus_workbench import data, hypotheses as hy  # noqa: E402
from run_confirmatory import already_tested  # noqa: E402


def sha_files(paths):
    h = hashlib.sha256()
    for p in sorted(paths):
        h.update(Path(p).read_bytes())
    return h.hexdigest()


# --------------------------------------------------------------------------- tests

def pe_header_openers(h, args):
    """Share of blind-opener tokens inside the expert-marked header, vs within-tablet shuffles."""
    import proto_elamite_skeleton as pe
    p = h["params"]
    files = sorted(Path(args.pe).glob("*.atf"))
    tabs = [pe.parse(f) for f in files]
    hold = [t for t in tabs if pe.split_of(t["pnum"]) == "holdout"]
    use = [t for t in hold if not t["damaged"] and len(t["toks"]) >= 2 and t["header_upto"]]
    ops = set(p["openers"])
    rng = np.random.default_rng(h["seed"])

    def share(perm):
        inside = tot = 0
        for t in use:
            idx = [k for k, x in enumerate(t["toks"]) if x != "NUM"]
            pos = list(rng.permutation(idx)) if perm else idx
            for k, q in zip(idx, pos):
                if t["toks"][k] in ops:
                    tot += 1
                    inside += q < t["header_upto"]
        return inside / tot if tot else float("nan"), tot

    obs, n = share(False)
    null = np.array([share(True)[0] for _ in range(h["n_perm"])])
    pval = float((1 + (null >= obs).sum()) / (h["n_perm"] + 1))
    return dict(observed=obs, null_mean=float(null.mean()), p=pval, support=n,
                holdout_texts=len(use), extra={"holdout_tablets": len(hold), "headed_undamaged": len(use)},
                data_sha256=sha_files(files), loaded_from=str(args.pe))


def opener_diversity(h, args):
    """Distinct opener forms: Mesopotamian seal legends minus Indus texts, at equal sample size."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import mesopotamian_seals as ms
    import pandas as pd
    p = h["params"]
    # Indus holdout
    raw, origin = data.load_raw(h["source_key"].split("+")[0])
    c = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"), **h["data_settings"])
    ind = data.holdout_only(c).df
    iops = set(p["indus_openers"])
    iu = [" ".join(x for x in s if x in iops) for s in ind["signs"]]
    iu = [u for u in iu if u]
    # Mesopotamian holdout (same selection as scripts/mesopotamian_seals.py)
    folder = Path(args.cdli)
    cat = pd.read_csv(folder / "cdli_cat.csv", usecols=["id_text", "period", "object_type", "provenience"],
                      dtype=str, low_memory=False)
    cat["P"] = "P" + cat["id_text"].str.zfill(6)
    info = cat.set_index("P")[["period", "object_type"]].to_dict("index")
    leg = {}
    for pn, kind, lines in ms.parse(folder / "cdliatf_unblocked.atf"):
        meta = info.get(pn, {})
        period = str(meta.get("period", ""))
        if not period.startswith(ms.PERIODS):
            continue
        if kind == "object" and "seal" not in str(meta.get("object_type", "")):
            continue
        toks = [w for ln in lines for w in ln]
        if len(toks) >= 2:
            leg.setdefault(" ".join(toks), toks)
    mhold = [t for k, t in leg.items()
             if int(hashlib.sha256(f"{ms.SALT}:{k}".encode()).hexdigest(), 16) % 100 < 20]
    mops = set(p["mesopotamian_openers"])
    mu = [" ".join(x for x in s if x in mops) for s in mhold]
    mu = [u for u in mu if u]
    n = min(len(iu), len(mu))
    rng = np.random.default_rng(h["seed"])

    def distinct(u, draws=200):
        return float(np.mean([len(set(rng.choice(u, n, replace=False))) for _ in range(draws)])) \
            if len(u) > n else float(len(set(u)))
    obs = distinct(mu) - distinct(iu)
    pool = iu + mu
    null = np.empty(h["n_perm"])
    for i in range(h["n_perm"]):
        a = rng.choice(len(pool), 2 * n, replace=False)
        null[i] = len({pool[j] for j in a[n:]}) - len({pool[j] for j in a[:n]})
    pval = float((1 + (null >= obs).sum()) / (h["n_perm"] + 1))
    return dict(observed=obs, null_mean=float(null.mean()), p=pval, support=n, holdout_texts=len(ind),
                extra={"indus_opener_texts": len(iu), "mes_holdout_legends": len(mhold), "mes_opener_legends": len(mu),
                       "indus_distinct": len(set(iu)), "mes_distinct_at_n": distinct(mu), "sample_size_n": n},
                data_sha256=c.sha256 + "+" + sha_files([folder / "cdliatf_unblocked.atf"]), loaded_from=origin)


def genre_from_position(h, args):
    """Position-only model trained on exploration predicts object type (seal / tablet / other) on the holdout.
    Statistic: balanced accuracy on holdout texts. Null: holdout labels permuted (model fixed)."""
    from sklearn.feature_extraction import DictVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import balanced_accuracy_score
    p = h["params"]
    O, C, N = set(p["openers"]), set(p["closers"]), set(p["numerals"])

    def feats(s):
        f = {"len": min(len(s), 8), "first_opener": s[0] in O, "last_closer": s[-1] in C,
             "has_numeral": any(x in N for x in s), "first_numeral": s[0] in N, "last_numeral": s[-1] in N}
        f["last=" + (s[-1] if s[-1] in C else "other")] = 1
        return f

    def cls(t):
        return t if t in ("seal", "tablet") else "other"
    raw, origin = data.load_raw(h["source_key"])
    c = data.build_corpus(raw, h["source_key"], metadata=data.load_metadata(h["source_key"]), **h["data_settings"])
    ex = data.explore_only(c).df
    ex = ex[ex.signs.map(len) >= 1]
    ho = data.holdout_only(c).df
    ho = ho[ho.signs.map(len) >= 1]
    seen = {tuple(s) for s in ex.signs}
    ho = ho[[tuple(s) not in seen for s in ho.signs]]               # no text shared with exploration
    ho = ho.assign(y=ho.object_type.map(cls), key=ho.signs.map(tuple))
    ho = ho.drop_duplicates(subset=["key", "y"])                      # one copy per text and class
    vec = DictVectorizer()
    Xe = vec.fit_transform([feats(list(s)) for s in ex.signs])
    model = LogisticRegression(max_iter=2000, class_weight="balanced").fit(Xe, ex.object_type.map(cls).values)
    pred = model.predict(vec.transform([feats(list(s)) for s in ho.signs]))
    y = ho.y.values
    obs = balanced_accuracy_score(y, pred)
    rng = np.random.default_rng(h["seed"])
    null = np.array([balanced_accuracy_score(rng.permutation(y), pred) for _ in range(h["n_perm"])])
    pval = float((1 + (null >= obs).sum()) / (h["n_perm"] + 1))
    from collections import Counter
    return dict(observed=float(obs), null_mean=float(null.mean()), p=pval, support=int(len(ho)), holdout_texts=int(len(ho)),
                extra={"class_counts": dict(Counter(y)), "predicted_counts": dict(Counter(pred))},
                data_sha256=c.sha256, loaded_from=origin)


def _export(args):
    """ICIT export (github.com/yajnadevam/lipi, src/assets/data/inscriptions.csv): find-spot, period, size fields.
    Not in this repository (no licence); its reading/translation columns are never used."""
    import pandas as pd
    path = Path(args.icit_export)
    L = pd.read_csv(path, dtype=str, keep_default_na=False)
    L["icit"] = L.id.str.split(".").str[0]
    return L.drop_duplicates("icit"), path


def _target(c, args):
    """The holdout, except in a dry run (exploration only, used to check the code before freezing)."""
    return data.explore_only(c).df if getattr(args, "dry_explore", False) else data.holdout_only(c).df


def unicorn_w_size(h, args):
    """Holdout unicorn seals (Mohenjo-daro, Harappa) coded Bull1:W are larger than other unicorn seals with the same
    text length (capped at 8) at the same site. Size = sqrt(horizontal mm x vertical mm) from the ICIT export (0 = missing).
    Statistic: within site x length cells, mean log size of W minus others, weighted by cell size (cells with both).
    Null: W labels permuted within cells. One-sided (greater)."""
    import pandas as pd
    L, path = _export(args)
    raw, origin = data.load_raw(h["source_key"])
    c = data.build_corpus(raw, h["source_key"], metadata=data.load_metadata(h["source_key"]), **h["data_settings"])
    d = _target(c, args).copy()
    d["icit"] = d.text_id.str.lstrip("S")
    d = d.merge(L[["icit", "horizontal(mm)", "vertical(mm)"]], on="icit", how="left")
    d = d[(d.object_type == "seal") & d.site.isin(["Mohenjo-daro", "Harappa"]) & d.motif.str.startswith("Bull1")].copy()
    w = pd.to_numeric(d["horizontal(mm)"], errors="coerce").replace(0, np.nan)
    v = pd.to_numeric(d["vertical(mm)"], errors="coerce").replace(0, np.nan)
    d["ls"] = np.log(np.sqrt(w * v))
    d = d.dropna(subset=["ls"])
    d["W"] = d.motif.eq("Bull1:W")
    d["cell"] = d.site + "_" + d.signs.map(len).clip(upper=8).astype(str)
    d = d[d.groupby("cell").W.transform(lambda s: s.any() and not s.all())]

    def stat(g):
        num = den = 0.0
        for _, x in d.assign(g=g).groupby("cell"):
            n = len(x); num += n * (x.ls[x.g].mean() - x.ls[~x.g].mean()); den += n
        return num / den
    obs = stat(d.W.values)
    rng = np.random.default_rng(h["seed"])
    null = np.array([stat(d.groupby("cell").W.transform(lambda s: pd.Series(rng.permutation(s.values), index=s.index)).values)
                     for _ in range(h["n_perm"])])
    pval = float((1 + (null >= obs).sum()) / (h["n_perm"] + 1))
    return dict(observed=float(obs), null_mean=float(null.mean()), p=pval, support=int(d.W.sum()), holdout_texts=int(len(d)),
                extra={"W_minus_other_percent": round(100 * (np.exp(obs) - 1), 1), "n_W": int(d.W.sum()), "n_other": int((~d.W).sum()),
                       "icit_export_sha256": sha_files([path])},
                data_sha256=c.sha256, loaded_from=origin)


def emblem_from_seal_text_bounded(h, args):
    """Bounded claim: seal text predicts unicorn vs other identified animal only weakly. A bag-of-signs logistic model
    (binary features, C=0.5, balanced weights) is trained on exploration seals with an identified animal and scored on
    holdout seals with an identified animal whose exact text is not in the exploration split. Statistic: balanced
    accuracy. Claim: it is below the bound (0.60). p = share of bootstrap resamples of the holdout seals (n_perm) whose
    balanced accuracy is at or above the bound (one-sided test of H0: accuracy >= bound). Support = minority class size."""
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import balanced_accuracy_score
    bound = h["params"]["bound"]
    raw, origin = data.load_raw(h["source_key"])
    c = data.build_corpus(raw, h["source_key"], metadata=data.load_metadata(h["source_key"]), **h["data_settings"])
    vague = set(h["params"]["vague_motifs"])

    def prep(df):
        df = df[(df.object_type == "seal") & ~df.motif.isin(vague) & (df.signs.map(len) >= 1)]
        return df.assign(y=np.where(df.motif.str.startswith("Bull1"), "unicorn", "other"), t=df.signs.map(" ".join))
    ex = prep(data.explore_only(c).df)
    if getattr(args, "dry_explore", False):          # dry run: split exploration in two by text id parity
        ids = ex.text_id.str.lstrip("S").astype(int)
        ho, ex = ex[ids % 5 == 0], ex[ids % 5 != 0]
    else:
        ho = prep(data.holdout_only(c).df)
    ho = ho[~ho.t.isin(set(ex.t))]
    vec = CountVectorizer(token_pattern=r"\S+", binary=True)
    model = LogisticRegression(max_iter=3000, class_weight="balanced", C=0.5).fit(vec.fit_transform(ex.t), ex.y)
    pred = model.predict(vec.transform(ho.t)); y = ho.y.values
    obs = balanced_accuracy_score(y, pred)
    rng = np.random.default_rng(h["seed"]); n = len(y); boots = []
    for _ in range(h["n_perm"]):
        i = rng.integers(0, n, n)
        if len(set(y[i])) < 2:
            continue
        boots.append(balanced_accuracy_score(y[i], pred[i]))
    boots = np.array(boots)
    pval = float((1 + (boots >= bound).sum()) / (len(boots) + 1))
    from collections import Counter
    cc = Counter(y)
    return dict(observed=float(obs), null_mean=float(bound), p=pval, support=int(min(cc.values())) if cc else 0,
                holdout_texts=int(n), extra={"class_counts": dict(cc), "bootstrap_95pct_upper": float(np.quantile(boots, 0.95)),
                                             "bound": bound},
                data_sha256=c.sha256, loaded_from=origin)


def restorer_calibration(h, args):
    """Frozen restorer (indus_workbench/restore.py; k and weights in params) trained on the exploration split.
    Each sign of each holdout text (2+ signs, exact text not in exploration) is hidden in turn. Among gaps where the
    top guess has confidence >= threshold, the share guessed exactly right must exceed the bound.
    p = one-sided exact binomial test of H0: accuracy <= bound. Support = number of such confident gaps.
    Descriptive (not tested): overall top-1/top-5 of the structured model and of the sign-pair (n-gram) model."""
    from scipy.stats import binomtest
    from indus_workbench.restore import Restorer
    p = h["params"]
    raw, origin = data.load_raw(h["source_key"])
    c = data.build_corpus(raw, h["source_key"], metadata=data.load_metadata(h["source_key"]), **h["data_settings"])
    ex = data.explore_only(c).df
    ex = ex[ex.signs.map(len) >= 2]
    if getattr(args, "dry_explore", False):          # dry run: hold out every fifth exploration text
        ids = ex.text_id.str.lstrip("S").astype(int)
        ho, ex = ex[ids % 5 == 0], ex[ids % 5 != 0]
    else:
        ho = data.holdout_only(c).df
        ho = ho[ho.signs.map(len) >= 2]
    seen = {tuple(s) for s in ex.signs}
    ho = ho[[tuple(s) not in seen for s in ho.signs]]
    R = Restorer(k=p["k"], weights=p["weights"]).fit(list(ex.signs), list(ex.object_type))
    conf_right, top1 = [], {"structured": [], "ngram": []}
    for s, o in zip(ho.signs, ho.object_type):
        s = list(s)
        for i in range(len(s)):
            for m in top1:
                rk = R.rank_of(s, i, o, m); top1[m].append(rk if rk else 10**6)
            g, pr = R.top(s, i, o, "structured", n=1)[0]
            if pr >= p["threshold"]:
                conf_right.append(g == s[i])
    k, n = int(sum(conf_right)), len(conf_right)
    obs = k / n if n else float("nan")
    pval = float(binomtest(k, n, p["bound"], alternative="greater").pvalue) if n else float("nan")
    extra = {"confident_gaps": n, "confident_right": k, "all_gaps": len(top1["ngram"])}
    for m, r in top1.items():
        r = np.array(r); extra[f"{m}_top1"] = round(float((r <= 1).mean()), 4); extra[f"{m}_top5"] = round(float((r <= 5).mean()), 4)
    return dict(observed=float(obs), null_mean=float(p["bound"]), p=pval, support=n, holdout_texts=int(len(ho)),
                extra=extra, data_sha256=c.sha256, loaded_from=origin)


TESTS = {"pe_header_openers": pe_header_openers, "opener_diversity_vs_mesopotamia": opener_diversity,
         "genre_from_position": genre_from_position,
         "unicorn_w_size": unicorn_w_size, "emblem_from_seal_text_bounded": emblem_from_seal_text_bounded,
         "restorer_calibration": restorer_calibration}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pe", default="")
    ap.add_argument("--cdli", default="")
    ap.add_argument("--icit-export", default="")
    ap.add_argument("--dry-explore", nargs="*", default=None,
                    help="kinds to run on exploration only (code check before freezing); nothing is written")
    args = ap.parse_args()
    if args.dry_explore is not None:
        args.dry_explore = True
        import types
        for kind, extra in [("restorer_calibration", {"k": 0.01, "weights": {"bi": 1.0, "tri": 0.15, "slot": 0.25, "obj": 0.25}, "threshold": 0.8, "bound": 0.70}), ("unicorn_w_size", {}), ("emblem_from_seal_text_bounded", {"bound": 0.60, "vague_motifs": ["unknown", "", "None", "Othr", "Comp", "Mult", "Misc"]})]:
            h = {"kind": kind, "params": extra, "source_key": "indus_website", "seed": 1, "n_perm": 500,
                 "data_settings": {"drop_damaged": True, "dedupe": True, "drop_unidentified": True}}
            r = TESTS[kind](h, args)
            print("DRY (exploration only)", kind, {k: r[k] for k in ("observed", "null_mean", "p", "support")}, r["extra"])
        return
    done = already_tested()
    results = []
    for path in sorted((ROOT / "hypotheses").glob("H-*.json")):
        h = json.loads(path.read_text())
        if h.get("type") != "external":
            continue
        if h["id"] in done:
            print(f"skip {path.name} (already tested)")
            continue
        if not hy.verify(h):
            print(f"skip {path.name} (edited after freezing)")
            continue
        r = TESTS[h["kind"]](h, args)
        results.append({"id": h["id"], "file": path.name, "kind": h["kind"], "params": h["params"],
                        "statement": h["statement"], "alpha": h["alpha"], "observed": r["observed"],
                        "null_mean": r["null_mean"],
                        "effect_ratio": r["observed"] / r["null_mean"] if r["null_mean"] else float("inf"),
                        "p": r["p"], "support": r["support"], "n_perm": h["n_perm"],
                        "holdout_texts": r["holdout_texts"], "data_sha256": r["data_sha256"],
                        "loaded_from": r["loaded_from"], "settings": h["data_settings"], "details": r["extra"]})
    if not results:
        print("nothing new to test")
        return
    previous = []
    for f in sorted((ROOT / "results").glob("confirmatory_*.json")):
        previous += [x for x in json.loads(f.read_text()) if isinstance(x, dict) and "id" in x and "p" in x and x["p"] == x["p"]]
    qs = hy.benjamini_hochberg([x["p"] for x in previous] + [x["p"] for x in results])
    for x, q in zip(results, qs[len(previous):]):
        x["q_BH"] = q
        x["q_BH_scope"] = f"all {len(previous) + len(results)} confirmatory tests to date"
        x["verdict"] = hy.verdict(q, x["alpha"], x["support"])
    stamp = date.today().isoformat()
    out = ROOT / "results" / f"confirmatory_{stamp}.json"
    k = 2
    while out.exists():
        out = ROOT / "results" / f"confirmatory_{stamp}_{k}.json"
        k += 1
    out.write_text(json.dumps(results, indent=2, default=str))
    for x in results:
        print(f"{x['id']}  {x['kind']:32s} obs {x['observed']:.3f} null {x['null_mean']:.3f} p {x['p']:.4f} "
              f"q {x['q_BH']:.4f} n {x['support']}  -> {x['verdict']}  {x['details']}")
    print("written", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
