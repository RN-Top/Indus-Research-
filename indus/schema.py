"""Data model for the Indus corpus.

Every record carries a `source` so that any text, sign or statistic shown in
the app can be traced back to a publication or photograph.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field, field_validator

UNREADABLE = "?"


class ObjectType(str, Enum):
    seal = "seal"
    sealing = "sealing"
    tablet = "tablet"
    pottery = "pottery"
    signboard = "signboard"
    other = "other"


class Direction(str, Enum):
    rtl = "rtl"
    ltr = "ltr"
    unknown = "unknown"


class Confidence(str, Enum):
    certain = "certain"
    probable = "probable"
    uncertain = "uncertain"
    unverified = "unverified"


class Site(BaseModel):
    site_id: str
    name: str
    country: str = ""
    lat: float | None = None
    lon: float | None = None
    source: str


class InscribedObject(BaseModel):
    object_id: str
    site_id: str
    object_type: ObjectType
    material: str = ""
    iconography: str = ""
    period: str = ""
    cisi_id: str = ""
    mahadevan_id: str = ""
    icit_id: str = ""
    image_url: str = ""
    image_licence: str = ""
    synthetic: bool = False
    source: str
    notes: str = ""


class Text(BaseModel):
    """One line of signs on one side of an object, in reading order."""

    text_id: str
    object_id: str
    side: str = "a"
    direction: Direction = Direction.rtl
    signs: list[str] = Field(default_factory=list)
    sign_list: str
    confidence: Confidence = Confidence.unverified
    synthetic: bool = False
    source: str
    notes: str = ""

    @field_validator("signs", mode="before")
    @classmethod
    def split_signs(cls, v):
        if isinstance(v, str):
            return v.split()
        return v


class Sign(BaseModel):
    sign_id: str
    sign_list: str
    label: str
    graphic_class: str = ""
    description: str = ""
    source: str


class Crosswalk(BaseModel):
    """Maps an internal sign ID to its number in published sign lists."""

    sign_id: str
    mahadevan: str = ""
    parpola: str = ""
    wells: str = ""
    source: str = ""
