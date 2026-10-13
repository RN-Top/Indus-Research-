"""Load and validate a corpus directory of CSV files."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd
from pydantic import BaseModel, ValidationError

from .schema import UNREADABLE, Crosswalk, InscribedObject, Sign, Site, Text

FILES: dict[str, type[BaseModel]] = {
    "sites": Site,
    "objects": InscribedObject,
    "texts": Text,
    "signs": Sign,
    "crosswalk": Crosswalk,
}


@dataclass
class Corpus:
    name: str
    sites: pd.DataFrame
    objects: pd.DataFrame
    texts: pd.DataFrame
    signs: pd.DataFrame
    crosswalk: pd.DataFrame
    errors: list[str] = field(default_factory=list)

    def synthetic_share(self) -> float:
        """Fraction of texts that are synthetic placeholders, not real inscriptions."""
        return float(self.texts["synthetic"].mean()) if len(self.texts) else 0.0

    def text_table(self) -> pd.DataFrame:
        """Texts joined with their object and site, one row per text."""
        df = self.texts.merge(self.objects, on="object_id", how="left", suffixes=("", "_object"))
        df = df.merge(
            self.sites[["site_id", "name"]].rename(columns={"name": "site"}),
            on="site_id",
            how="left",
        )
        df["length"] = df["signs"].map(len)
        df["sequence"] = df["signs"].map(" ".join)
        return df


def _read(path: Path, model: type[BaseModel], errors: list[str]) -> pd.DataFrame:
    if not path.exists():
        errors.append(f"{path.name}: file missing")
        return pd.DataFrame(columns=list(model.model_fields))
    raw = pd.read_csv(path, dtype=str, keep_default_na=False)
    rows = []
    for i, record in enumerate(raw.to_dict("records"), start=2):
        clean = {k: v for k, v in record.items() if v != ""}
        try:
            rows.append(model.model_validate(clean).model_dump(mode="json"))
        except ValidationError as e:
            for err in e.errors():
                loc = ".".join(str(p) for p in err["loc"])
                errors.append(f"{path.name} line {i}: {loc}: {err['msg']}")
    return pd.DataFrame(rows, columns=list(model.model_fields))


def load_corpus(directory: str | Path, name: str | None = None) -> Corpus:
    directory = Path(directory)
    errors: list[str] = []
    frames = {key: _read(directory / f"{key}.csv", model, errors) for key, model in FILES.items()}
    corpus = Corpus(name=name or directory.name, errors=errors, **frames)
    errors.extend(check_references(corpus))
    return corpus


def check_references(corpus: Corpus) -> list[str]:
    """Cross-file checks: every text points at a known object and known signs."""
    problems = []
    object_ids = set(corpus.objects["object_id"])
    site_ids = set(corpus.sites["site_id"])
    sign_ids = set(corpus.signs["sign_id"]) | {UNREADABLE}
    for row in corpus.objects.itertuples():
        if row.site_id not in site_ids:
            problems.append(f"object {row.object_id}: unknown site {row.site_id}")
    for row in corpus.texts.itertuples():
        if row.object_id not in object_ids:
            problems.append(f"text {row.text_id}: unknown object {row.object_id}")
        unknown = sorted(set(row.signs) - sign_ids)
        if unknown:
            problems.append(f"text {row.text_id}: unknown signs {', '.join(unknown)}")
    return problems
