import json

from dex.config import _META_STORE


def create_chapter_meta(_meta_path: str, manga_title: str, chapter_title: str):
    with open(f"{_meta_path}/{_META_STORE}", "w") as _meta_json:
        _meta_json.write(
            json.dumps(
                {"manga": manga_title, "chapter": chapter_title, "last_read_at": ""}
            )
        )
