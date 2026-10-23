"""Run every registered hypothesis once on the locked holdout.

Same logic as the Hypothesis Lab's confirm step, for use outside the app.
Writes results/confirmatory_<date>.json. Run once per set of hypotheses.
"""

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from indus_workbench import data, hypotheses as hy  # noqa: E402


def already_tested() -> set[str]:
    """IDs with a confirmatory result already on file: each hypothesis is tested once."""
    done = set()
    for f in (ROOT / "results").glob("confirmatory_*.json"):
        done |= {x["id"] for x in json.loads(f.read_text()) if isinstance(x, dict) and "id" in x}
    return done


def main() -> None:
    results = []
    done = already_tested()
    for path in sorted((ROOT / "hypotheses").glob("H-*.json")):
        h = json.loads(path.read_text())
        if h.get("id") in done:
            print(f"skip {path.name} (already tested on the holdout)")
            continue
        if h.get("source_key") == "icit_new_to_export":
            print(f"skip {path.name} (new-set test: run scripts/run_newset_confirmatory.py)")
            continue
        if h.get("type") == "external":
            print(f"skip {path.name} (comparison-script test: run scripts/run_external_confirmatory.py)")
            continue
        if h.get("type") == "reading" or not hy.verify(h):
            print(f"skip {path.name} (reading key or edited after freezing)")
            continue
        raw, origin = data.load_raw(h["source_key"])
        c = data.build_corpus(raw, h["source_key"], **h["data_settings"],
                              collapse_variants=data.SOURCES[h["source_key"]].get("collapse_variants", False),
                              metadata=data.load_metadata(h["source_key"]))
        hold = data.holdout_only(c)
        r = hy.run_test(h, hold.df)
        results.append({"id": h["id"], "file": path.name, "kind": h["kind"], "params": h["params"],
                        "statement": h["statement"], "alpha": h["alpha"], "observed": r.observed,
                        "null_mean": r.null_mean, "effect_ratio": r.effect_ratio, "p": r.p_value,
                        "support": r.n_support, "n_perm": r.n_perm, "holdout_texts": hold.n_texts,
                        "data_sha256": c.sha256, "loaded_from": origin, "settings": c.settings})
    # Correct across every confirmatory test ever run, not just this batch, so
    # running hypotheses in small batches cannot dodge the correction.
    previous = []
    for f in sorted((ROOT / "results").glob("confirmatory_*.json")):
        previous += [x for x in json.loads(f.read_text())
                     if isinstance(x, dict) and "id" in x and "p" in x and x["p"] == x["p"]]
    valid = [x for x in results if x["p"] == x["p"]]
    qs = hy.benjamini_hochberg([x["p"] for x in previous] + [x["p"] for x in valid])
    for x, q in zip(valid, qs[len(previous):]):
        x["q_BH"] = q
        x["q_BH_scope"] = f"all {len(previous) + len(valid)} confirmatory tests to date"
    for x in results:
        x.setdefault("q_BH", float("nan"))
        x["verdict"] = hy.verdict(x["q_BH"], x["alpha"], x["support"])
    if not results:
        print("nothing new to test")
        return
    stamp = date.today().isoformat()
    out = ROOT / "results" / f"confirmatory_{stamp}.json"
    k = 2
    while out.exists():
        out = ROOT / "results" / f"confirmatory_{stamp}_{k}.json"
        k += 1
    out.write_text(json.dumps(results, indent=2, default=str))
    for x in results:
        print(f"{x['id']}  {x['kind']:18s} obs {x['observed']:.3f} null {x['null_mean']:.3f} "
              f"p {x['p']:.4f} q {x['q_BH']:.4f} n {x['support']}  -> {x['verdict']}")
    print("written", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
