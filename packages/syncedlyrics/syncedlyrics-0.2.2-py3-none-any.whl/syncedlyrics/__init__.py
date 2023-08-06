"""
Search for an LRC format (synchronized lyrics) of a music.

```py
import syncedlyrics
lrc_text = syncedlyrics.search("[TRACK_NAME] [ARTIST_NAME]")
```
"""

from typing import Optional, List
import logging
from .providers import NetEase, Deezer
from .utils import is_lrc_valid, save_lrc_file


def search(
    search_term: str,
    allow_plain_format: bool = False,
    save_path: str = None,
    providers: List[str] = None,
) -> Optional[str]:
    """
    Returns the synced lyrics of the song in [LRC](https://en.wikipedia.org/wiki/LRC_(file_format)) format if found.
    ### Arguments
    - `search_term`: The search term to find the track.
    - `allow_normal_format`: Return a plain text (not synced) lyrics if not LRC was found.
    - `save_path`: Path to save `.lrc` lyrics. No saving if `None`.
    - `providers`: A list of provider names to include in searching. Uses `Deezer` and `NetEase` by default.
    """
    _providers = [
        Deezer(),
        NetEase(),
    ]
    if providers:
        # Filtering the providers
        _providers = [p for p in _providers if p.__class__.__name__ in providers]
    for provider in _providers:
        lrc = provider.get_lrc(search_term)
        if is_lrc_valid(lrc, allow_plain_format):
            break
    if not lrc:
        logging.info(f'No synced-lyrics found for "{search_term}" :(')
        return
    if save_path:
        save_path = save_path.format(search_term=search_term)
        save_lrc_file(save_path, lrc)
    return lrc
