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


def main() -> None:
    results = []
    for path in sorted((ROOT / "hypotheses").glob("H-*.json")):
        h = json.loads(path.read_text())
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
    valid = [x for x in results if x["p"] == x["p"]]
    for x, q in zip(valid, hy.benjamini_hochberg([x["p"] for x in valid])):
        x["q_BH"] = q
    for x in results:
        x.setdefault("q_BH", float("nan"))
        x["verdict"] = hy.verdict(x["q_BH"], x["alpha"], x["support"])
    out = ROOT / "results" / f"confirmatory_{date.today().isoformat()}.json"
    out.write_text(json.dumps(results, indent=2, default=str))
    for x in results:
        print(f"{x['id']}  {x['kind']:18s} obs {x['observed']:.3f} null {x['null_mean']:.3f} "
              f"p {x['p']:.4f} q {x['q_BH']:.4f} n {x['support']}  -> {x['verdict']}")
    print("written", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
