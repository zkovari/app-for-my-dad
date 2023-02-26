from dataclasses import dataclass, field
from typing import List


@dataclass
class Song:
    title: str
    full_name: str


@dataclass
class Album:
    band: str
    album: str
    year: int
    genre: str = ''
    songs: List[Song] = field(default_factory=list)
