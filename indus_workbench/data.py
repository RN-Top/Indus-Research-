"""Corpus loading, normalisation, provenance and the locked holdout split.

Every analysis in the app starts from `Corpus`, so the rules that a reviewer
will check first (where the data came from, which version, what was excluded
and why, how texts were oriented, which texts are held out) all live here.
"""

from __future__ import annotations

import hashlib
import io
from dataclasses import dataclass, field

import pandas as pd

# ---------------------------------------------------------------------------
# Sources. URLs are pinned to a specific commit of the dataset repository so
# that results can be reproduced exactly. Change the revision deliberately,
# never silently, and record the change in CHANGELOG.md.
# ---------------------------------------------------------------------------

HF_REPO = "joyboseroy/indus_decipher"
HF_REVISION = "47e8616dff4d1ff62343bd74f3eeefc4afbfd4d8"


def _hf_url(filename: str) -> str:
    return f"https://huggingface.co/datasets/{HF_REPO}/resolve/{HF_REVISION}/{filename}"


DATA_DIR = __import__("pathlib").Path(__file__).resolve().parent.parent / "data"

_CISI_ORIGIN = "Hand transcription of Parpola's CISI (mayig/indus-valley-script-corpus)"

# `file` + `sha256`: a copy bundled in data/, used first so the app works
# offline and every user analyses byte-identical data. `url`: the pinned
# public copy, used when no bundled file exists. `collapse_variants`: build
# this source by reducing each sign ID to its base sign.
SOURCES: dict[str, dict] = {
    "indus_website": {
        "label": "Full corpus: 2,543 inscriptions, 52 sites (G-numbered signs)",
        "file": "indus_website_real_corpus.csv",
        "sha256": "7258075509684e008aea3d9726417de86a135c1a4325e2e633e0cb98598392c8",
        "url": _hf_url("indus_website_real_corpus.csv"),
        "sign_scheme": "G-numbers (sign list not named by the dataset card)",
        "origin": "MySQL dump from yajnadevam/indus-website on GitHub, converted to CSV by joyboseroy",
        "licence": "Derived CSV: MIT. Underlying transcription: the source repository's terms apply.",
    },
    "cisi_allograph": {
        "label": "CISI: 179 Mohenjo-daro unicorn seals, every sign variant separate",
        "file": "cisi_real_corpus_allograph.csv",
        "sha256": "2b464963848d8046b635266e4706baf98495f78fecea0ab131cfa4bc32eb4048",
        "url": _hf_url("cisi_real_corpus_allograph.csv"),
        "sign_scheme": "P-numbers with variant codes (e.g. P324_1-0-0-1-0)",
        "origin": _CISI_ORIGIN,
        "licence": "MIT",
    },
    "cisi_base": {
        "label": "CISI: same seals, variants merged into base signs",
        "file": "cisi_real_corpus_allograph.csv",
        "sha256": "2b464963848d8046b635266e4706baf98495f78fecea0ab131cfa4bc32eb4048",
        "url": _hf_url("cisi_real_corpus_allograph.csv"),
        "collapse_variants": True,
        "sign_scheme": "P-numbers, variant codes removed (P324_1-0-0-1-0 becomes P324)",
        "origin": _CISI_ORIGIN + "; variants merged by this app",
        "licence": "MIT",
    },
    "cisi_hierarchical": {
        "label": "CISI: same seals, variants split only when seen 3+ times (downloads)",
        "url": _hf_url("cisi_real_corpus_hierarchical.csv"),
        "sign_scheme": "P-numbers, partial variant split",
        "origin": _CISI_ORIGIN,
        "licence": "MIT",
    },
}

SOURCES["icit_new_to_export"] = {
    "label": "Held out from the export: 1,788 ICIT objects missing from indus_website (paragorth merged Wells/ICIT copy)",
    "file": "icit_merged_paragorth/new_to_export_corpus.csv",
    "sha256": "47667e3d8be6be56680395e58119ccdff157e9d0a6d8296b8beeeba8192ddde9",
    "url": "",
    "sign_scheme": "G-numbers (Wells/ICIT), reading order",
    "origin": "github.com/paragorth/Indus- data/derived/merged-corpus-canonical.json (MIT), filtered by scripts/build_new_to_export.py",
    "licence": "MIT (derived table); underlying ICIT transcription by Wells and Fuls",
}

CISI_FAMILY = ["cisi_base", "cisi_hierarchical", "cisi_allograph"]


def load_metadata(source_key: str) -> pd.DataFrame | None:
    """Extra per-text details (object type, material) where available."""
    if source_key == "icit_new_to_export":
        return pd.read_csv(DATA_DIR / "icit_merged_paragorth/new_to_export_metadata.csv", dtype=str, keep_default_na=False)
    path = DATA_DIR / "text_metadata.csv"
    if source_key == "indus_website" and path.exists():
        return pd.read_csv(path, dtype=str, keep_default_na=False)
    return None


def load_raw(source_key: str) -> tuple[bytes, str]:
    """Return the raw bytes for a source and where they came from.

    Uses the bundled copy when present and checks it against the recorded
    SHA-256; a mismatch is raised, never silently accepted."""
    src = SOURCES[source_key]
    if "file" in src and (DATA_DIR / src["file"]).exists():
        raw = (DATA_DIR / src["file"]).read_bytes()
        if sha256_bytes(raw) != src["sha256"]:
            raise ValueError(f"Bundled file {src['file']} does not match its recorded SHA-256. "
                             "The data has changed; restore the original or record the new "
                             "version in CHANGELOG.md.")
        return raw, f"bundled copy data/{src['file']}"
    return fetch(src["url"]), src["url"]


# Column names the rest of the code relies on.
STANDARD_COLUMNS = [
    "text_id", "signs", "site", "object_type", "motif",
    "reading_direction", "damaged", "source_ref",
]

HOLDOUT_FRACTION = 0.20
# The salt is part of the pre-registered protocol. Changing it changes which
# texts are held out, which would let someone pick a favourable split.
HOLDOUT_SALT = "indus-workbench-holdout-v1"


@dataclass
class Exclusion:
    text_id: str
    reason: str


@dataclass
class Corpus:
    """A cleaned corpus plus everything needed to audit how it was made."""

    df: pd.DataFrame
    source_key: str
    sha256: str
    exclusions: list[Exclusion] = field(default_factory=list)
    settings: dict = field(default_factory=dict)

    @property
    def sequences(self) -> list[list[str]]:
        return list(self.df["signs"])

    @property
    def n_texts(self) -> int:
        return len(self.df)

    @property
    def n_tokens(self) -> int:
        return int(self.df["signs"].map(len).sum())

    @property
    def sign_inventory(self) -> list[str]:
        return sorted({s for seq in self.sequences for s in seq})

    def subset(self, mask: pd.Series, note: str) -> "Corpus":
        settings = dict(self.settings)
        settings.setdefault("subsets", []).append(note)
        return Corpus(self.df[mask].reset_index(drop=True), self.source_key,
                      self.sha256, list(self.exclusions), settings)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def parse_csv(raw: bytes) -> pd.DataFrame:
    """Read the raw CSV and map it to the standard columns."""
    df = pd.read_csv(io.BytesIO(raw), dtype=str, keep_default_na=False)
    cols = {c.lower().strip(): c for c in df.columns}

    def pick(*names, default=""):
        for n in names:
            if n in cols:
                return df[cols[n]]
        return pd.Series([default] * len(df), index=df.index)

    out = pd.DataFrame({
        "text_id": pick("inscription_id", "text_id", "id"),
        "raw_sequence": pick("sign_sequence", "signs", "sequence"),
        "site": pick("site", default="unknown"),
        "object_type": pick("object_type", "type", default="unknown"),
        "motif": pick("motif", default="unknown"),
        "reading_direction": pick("reading_direction", default="R-L"),
        "damaged": pick("damaged", default="False"),
        "source_ref": pick("cisi_number", "inscription_id", default=""),
    })
    for c in ["site", "object_type", "motif", "source_ref"]:
        out[c] = out[c].replace("", "unknown")
    out["damaged"] = out["damaged"].str.strip().str.lower().isin(["true", "1", "yes"])
    out["motif_group"] = out["motif"].map(motif_group)
    out["is_unicorn"] = out["motif_group"].map(lambda m: "yes" if m == "unicorn" else "no")
    out["reading_direction"] = out["reading_direction"].str.strip().str.upper()
    return out


def motif_group(motif: str) -> str:
    """Collapse the source's motif codes to the animal: 'Bull1:W' -> 'unicorn'.

    Bull1 is the one-horned bull ('unicorn') in the source's own label list."""
    m = str(motif).strip()
    if m.startswith("Bull1"):
        return "unicorn"
    if m in ("", "unknown", "None", "nan"):
        return "none"
    return m.split(":")[0]


def orient(tokens: list[str], direction: str) -> list[str]:
    """Return signs in reading order.

    The dataset card defines the convention: R-L rows are used as stored and
    L-R rows are reversed. This is a storage convention, not a claim about
    how the script was read.
    """
    return list(reversed(tokens)) if direction == "L-R" else list(tokens)


# Sign IDs the source uses without documenting them. In the CISI files, P000
# appears where other IDs carry a catalogue number, so it most likely marks a
# sign the transcriber could not assign. Texts containing one are excluded by
# default because an unknown sign breaks every adjacency it touches.
UNIDENTIFIED_PREFIXES = ("P000",)
# In the full corpus's source database these G-numbers are drawn with the
# "double question mark" placeholder (U+2047) rather than a sign: they mark
# signs that could not be identified.
UNIDENTIFIED_G = {"G12", "G25", "G106", "G316", "G376", "G445", "G515", "G516", "G546", "G547", "G606"}
# G0 is a line break in the source database (its glyph is "<br>"), not a sign.
LINE_BREAK = "G0"


def base_sign(sign: str) -> str:
    """CISI IDs encode variants after an underscore (P324_1-0-0-1-0).
    The base sign is the part before it (P324)."""
    return sign.split("_", 1)[0]


def is_unidentified(sign: str) -> bool:
    return base_sign(sign) in UNIDENTIFIED_PREFIXES or sign in UNIDENTIFIED_G


def build_corpus(raw: bytes, source_key: str, *, drop_damaged: bool = True,
                 dedupe: bool = False, min_length: int = 1,
                 collapse_variants: bool = False, drop_unidentified: bool = True,
                 metadata: pd.DataFrame | None = None) -> Corpus:
    """Clean a raw CSV into a Corpus, logging every excluded text and why."""
    df = parse_csv(raw)
    exclusions: list[Exclusion] = []

    df["signs"] = [orient(str(s).split(), d)
                   for s, d in zip(df["raw_sequence"], df["reading_direction"])]
    line_breaks = int(sum(s.count(LINE_BREAK) for s in df["signs"]))
    df["signs"] = [[x for x in s if x != LINE_BREAK] for s in df["signs"]]
    if collapse_variants:
        df["signs"] = [[base_sign(x) for x in s] for s in df["signs"]]
    if metadata is not None:
        md = metadata.set_index("text_id")
        for col in ("object_type", "material"):
            if col in md:
                filled = df["text_id"].map(md[col]).fillna("")
                df[col] = filled.where(filled != "", df.get(col, "unknown"))

    keep = []
    seen: set[tuple] = set()
    for row in df.itertuples():
        if drop_unidentified and any(is_unidentified(x) for x in row.signs):
            exclusions.append(Exclusion(row.text_id, "contains an unidentified sign"))
            keep.append(False)
            continue
        if len(row.signs) < min_length:
            exclusions.append(Exclusion(row.text_id, f"shorter than {min_length} sign(s)"))
            keep.append(False)
            continue
        if drop_damaged and row.damaged:
            exclusions.append(Exclusion(row.text_id, "marked damaged in source"))
            keep.append(False)
            continue
        key = tuple(row.signs)
        if dedupe and key in seen:
            exclusions.append(Exclusion(row.text_id, "duplicate of an earlier identical text"))
            keep.append(False)
            continue
        seen.add(key)
        keep.append(True)

    df = df[keep].reset_index(drop=True)
    df["length"] = df["signs"].map(len)
    df["split"] = [holdout_split(t) for t in df["text_id"]]
    settings = {"drop_damaged": drop_damaged, "dedupe": dedupe, "min_length": min_length,
                "collapse_variants": collapse_variants, "drop_unidentified": drop_unidentified,
                "line_breaks_removed": line_breaks, "metadata_attached": metadata is not None}
    return Corpus(df, source_key, sha256_bytes(raw), exclusions, settings)


def holdout_split(text_id: str) -> str:
    """Deterministically assign a text to 'explore' or 'holdout'.

    The split depends only on the text ID and a fixed salt, so it is the same
    for everyone, cannot be tuned, and does not change when other texts are
    added or removed.
    """
    h = hashlib.sha256(f"{HOLDOUT_SALT}:{text_id}".encode()).digest()
    frac = int.from_bytes(h[:8], "big") / 2**64
    return "holdout" if frac < HOLDOUT_FRACTION else "explore"


def explore_only(corpus: Corpus) -> Corpus:
    return corpus.subset(corpus.df["split"] == "explore", "exploration split only")


def holdout_only(corpus: Corpus) -> Corpus:
    return corpus.subset(corpus.df["split"] == "holdout", "HOLDOUT split")


def fetch(url: str, timeout: int = 60) -> bytes:
    """Download a source file. Kept separate so the app can cache it."""
    import urllib.request
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read()
