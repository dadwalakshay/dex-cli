import json
import subprocess

from dex.config import _META_STORE, DEFAULT_STORAGE_PATH


def _meta_parser(path: str = "") -> dict:
    with open(
        f"{DEFAULT_STORAGE_PATH}{('/' + path) or ''}/{_META_STORE}", "rb"
    ) as _meta:
        _meta_json = json.load(_meta)

        return _meta_json


def _open_chapter(path: str) -> None:
    subprocess.Popen(["xdg-open", f"{DEFAULT_STORAGE_PATH}/{path}"])
