from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

    from plextraktsync.trakt.types import TraktMedia


@dataclass
class PartialTraktMedia:
    ids: Any
    media_type: str

    @classmethod
    def create(cls, m: TraktMedia):
        return cls(**{
            "ids": m.ids,
            "media_type": m.media_type,
        })
