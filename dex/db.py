import json

from dex.config import _META_STORE


def read_chapter_meta(chapter_path: str) -> dict:
    _meta_path = f"{chapter_path}/{_META_STORE}"

    try:
        with open(_meta_path, "r") as _meta_json_r:
            _meta_json_obj = json.loads(_meta_json_r.read())

            return _meta_json_obj
    except FileNotFoundError:
        return {}


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
