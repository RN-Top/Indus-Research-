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


TESTS = {"pe_header_openers": pe_header_openers, "opener_diversity_vs_mesopotamia": opener_diversity}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pe", required=True)
    ap.add_argument("--cdli", required=True)
    args = ap.parse_args()
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
