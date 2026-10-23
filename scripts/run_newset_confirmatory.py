"""Run the locked new-set batch ONCE (protocol: predictions/newset_protocol_2026-10-23.md).

Data: the held-out-from-export set (source key icit_new_to_export): ICIT objects missing from this project's export,
never used in any analysis here. The whole set is test data (no exploration split).

Batch:
  A. Replications: every registered hypothesis on the indus_website source (not external, fingerprint intact),
     run unchanged on the new set with its own frozen settings and parameters.
  B. New hypotheses registered for this set (source_key icit_new_to_export).
Benjamini-Hochberg is applied within this batch (A + B). Results: results/newset_2026-10-23.json.
Refuses to run if that file exists.

    python scripts/run_newset_confirmatory.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from indus_workbench import data, hypotheses as hy  # noqa: E402

OUT = ROOT / "results" / "newset_2026-10-23.json"
SRC = "icit_new_to_export"


def main() -> None:
    if OUT.exists():
        sys.exit(f"{OUT.name} exists: the batch has already been run once.")
    raw, origin = data.load_raw(SRC)
    md = data.load_metadata(SRC)
    batch = []
    for path in sorted((ROOT / "hypotheses").glob("H-*.json")):
        h = json.loads(path.read_text())
        if h.get("type") in ("external", "reading") or not hy.verify(h):
            continue
        if h["source_key"] == "indus_website":
            batch.append(("replication", path, h))
        elif h["source_key"] == SRC:
            batch.append(("new", path, h))
    results = []
    for role, path, h in batch:
        c = data.build_corpus(raw, SRC, **h["data_settings"], metadata=md)
        r = hy.run_test(h, c.df)
        results.append({"id": h["id"], "role": role, "file": path.name, "kind": h["kind"], "statement": h["statement"],
                        "alpha": h["alpha"], "observed": r.observed, "null_mean": r.null_mean,
                        "effect_ratio": r.effect_ratio, "p": r.p_value, "support": r.n_support, "n_perm": r.n_perm,
                        "texts": c.n_texts, "note": r.note, "data_sha256": c.sha256, "loaded_from": origin,
                        "settings": c.settings})
        print(f"{role:11} {h['id']}  {h['kind']:24} obs {r.observed:.3f} p {r.p_value:.4f} n {r.n_support}", flush=True)
    valid = [x for x in results if x["p"] == x["p"]]
    for x, q in zip(valid, hy.benjamini_hochberg([x["p"] for x in valid])):
        x["q_BH"] = q
        x["q_BH_scope"] = f"within the new-set batch ({len(valid)} tests with a p-value)"
    for x in results:
        x.setdefault("q_BH", float("nan"))
        x["verdict"] = hy.verdict(x["q_BH"], x["alpha"], x["support"])
    OUT.write_text(json.dumps(results, indent=2, default=str))
    print("written", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
