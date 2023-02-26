from dataclasses import dataclass, field
from typing import List


@dataclass
class Song:
    title: str


@dataclass
class Album:
    band: str
    album: str
    year: int
    songs: List[Song] = field(default_factory=list)
