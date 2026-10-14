"""Render the session log as a Markdown methods report."""

from __future__ import annotations

import platform
from datetime import datetime, timezone

from . import __version__, data


def _fmt(x, nd=4):
    try:
        return f"{float(x):.{nd}g}"
    except (TypeError, ValueError):
        return str(x)


def render(log: dict) -> str:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    out = [
        "# Indus Script Workbench: methods report",
        "",
        f"Generated {now} · Workbench v{__version__} · Python {platform.python_version()}",
        "",
        "The Indus script is undeciphered. These results describe statistical patterns in "
        "transcribed sign sequences, each compared against explicit controls.",
        "",
    ]
    d = log.get("data")
    if d:
        out += [
            "## Data",
            f"- Corpus: `{d['source_key']}` — {data.SOURCES[d['source_key']]['origin']}",
            f"- URL (pinned): {d['url']}",
            f"- SHA-256: `{d['sha256']}`",
            f"- Settings: {d['settings']}",
            f"- Texts used: {d['n_texts']:,}; sign tokens: {d['n_tokens']:,}; distinct signs: {d['n_signs']:,}",
            f"- Texts excluded: {d['n_excluded']:,} (reasons listed in the app)",
            f"- Split: {d['explore']:,} exploration / {d['holdout']:,} holdout "
            f"(salt `{data.HOLDOUT_SALT}`, fraction {data.HOLDOUT_FRACTION})",
            "",
        ]
    e = log.get("entropy")
    if e:
        out += ["## Block entropy (replication of Rao 2010)",
                f"Texts: {e['texts']:,}; alphabet size: {e['alphabet']}; Miller-Madow: {e['miller_madow']}; "
                f"seeds per control: {e['seeds']}.", "",
                "| Series | " + " | ".join(f"N={i}" for i in range(1, e['max_n'] + 1)) + " |",
                "|---|" + "---|" * e["max_n"]]
        for name, vals in e["curves"].items():
            out.append(f"| {name} | " + " | ".join(_fmt(v, 3) for v in vals) + " |")
        out.append("")
    s = log.get("sequence_model")
    if s:
        out += ["## Sequence model (5-fold cross-validation, exploration split)",
                f"λ = {s['lambda']}.",
                f"- Indus: gain from sign order {_fmt(s['real']['mean_gain_bits'])} bits/sign; "
                f"bigram better in {s['real']['folds_bigram_better']}/5 folds.",
                f"- Negative control (shuffled within texts): gain {_fmt(s['shuffled_control']['mean_gain_bits'])} "
                f"bits/sign; bigram better in {s['shuffled_control']['folds_bigram_better']}/5 folds.", ""]
    r = log.get("robustness")
    if r:
        out += ["## Robustness grid (exploration split)", f"Hypothesis: {r['hypothesis']}", "",
                "| Corpus | Damaged excluded | Duplicates removed | Observed | Null mean | p | Support |",
                "|---|---|---|---|---|---|---|"]
        for row in r["rows"]:
            out.append(f"| {row['corpus']} | {row['damaged excluded']} | {row['duplicates removed']} | "
                       f"{_fmt(row['observed'])} | {_fmt(row['null mean'])} | {_fmt(row['p'])} | {row['support']} |")
        out.append("")
    c = log.get("confirmatory")
    if c:
        out += ["## Confirmatory tests on the locked holdout",
                "Benjamini-Hochberg correction across all registered hypotheses.", "",
                "| ID | Kind | Params | Observed | Null mean | p | q (BH) | Support | Verdict |",
                "|---|---|---|---|---|---|---|---|---|"]
        for row in c["results"]:
            out.append(f"| {row['id']} | {row['kind']} | `{row['params']}` | {_fmt(row['observed'])} | "
                       f"{_fmt(row['null_mean'])} | {_fmt(row['p'])} | {_fmt(row['q_BH'])} | "
                       f"{row['support']} | {row['verdict']} |")
        out.append("")
    out += ["## References",
            "- Rao, R. P. N. 2010. Probabilistic analysis of an ancient undeciphered script. *IEEE Computer* 43(4).",
            "- Rao, R. P. N. et al. 2009. Entropic evidence for linguistic structure in the Indus script. *Science* 324.",
            "- Rao, R. P. N. 2017. The Indus script and economics. In *Walking with the Unicorn*, Archaeopress.",
            "- Sproat, R. 2014. A statistical comparison of written language and nonlinguistic symbol systems. *Language* 90(2).",
            "- Benjamini, Y. and Hochberg, Y. 1995. Controlling the false discovery rate. *JRSS B* 57(1)."]
    return "\n".join(out)
