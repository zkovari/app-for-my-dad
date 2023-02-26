import os
from pathlib import Path
from typing import List

from atomicwrites import atomic_write
from qthandy import ask_confirmation

from vakhangya.view.domain import Album, Song


def retrieve_album(path: Path) -> Album:
    parts = path.name.split(' - ')
    if len(parts) < 2:
        raise ValueError(f'Could not parse album name from folder: {path.name}')

    return Album(parts[0][0:-4].strip(), album=parts[1].strip(), year=int(parts[0][-4:]))


def collect_songs(path: Path) -> List[Song]:
    songs = []
    for file in os.listdir(path):
        if file.endswith('.mp3') or file.endswith('.flac'):
            song_path = path.joinpath(file)
            songs.append(Song(song_path.stem, full_name=song_path.name))
    return songs


def generate_cue_file(album: Album, path: Path) -> bool:
    content: str = f'''REM GENRE "{album.genre}"
REM DATE {album.year}
PERFORMER "{album.band}"
TITLE "{album.album}"
'''

    for i, song in enumerate(album.songs):
        content += f'''FILE "{song.full_name}" WAVE
  TRACK {i + 1} AUDIO
    TITLE "{song.title}"
    INDEX 01 00:00:00\n'''

    target = path.joinpath(f'{album.band} - {album.album}.cue')
    if target.exists():
        if not ask_confirmation('CUE file already exists. Override?'):
            return False
    with atomic_write(target, overwrite=True) as f:
        f.write(content)

    return True
