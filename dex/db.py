import json

from dex.config import _META_STORE


def create_or_update_chapter_meta(
    _meta_path: str, manga_obj: dict, chapter_obj: dict
) -> None:
    with open(f"{_meta_path}/{_META_STORE}", "w") as _meta_json:
        _meta_json.write(
            json.dumps({"manga": manga_obj, "chapter": chapter_obj, "last_read_at": ""})
        )
