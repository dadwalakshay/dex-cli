import json

from dex.config import _META_STORE


def create_or_update_chapter_meta(
    _meta_path: str, manga_title: str, chapter_title: str, _meta: dict
) -> None:
    with open(f"{_meta_path}/{_META_STORE}", "w") as _meta_json:
        _meta_json.write(
            json.dumps(
                {
                    "manga_title": manga_title,
                    "chapter_title": chapter_title,
                    "last_read_at": "",
                    "_meta": _meta,
                }
            )
        )
