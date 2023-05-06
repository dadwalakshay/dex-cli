import os
from abc import ABC, abstractmethod

import requests

from dex.config import DEFAULT_STORAGE_PATH


class BaseClient(ABC):
    def __init__(self) -> None:
        os.makedirs(DEFAULT_STORAGE_PATH, exist_ok=True)

    @classmethod
    @abstractmethod
    def _parse_error_resp(cls, resp: requests.Response) -> str:
        return ""

    @classmethod
    @abstractmethod
    def handler(cls, url: str, params: dict = {}, json: dict = {}) -> tuple[bool, dict]:
        return True, {}

    @abstractmethod
    def list_mangas(self, title: str) -> tuple[bool, dict]:
        return True, {}

    @abstractmethod
    def list_chapters(self, manga_obj: dict, language: str = "en") -> tuple[bool, dict]:
        return True, {}

    @abstractmethod
    def download_chapter(self, manga_obj: dict, chapter_obj: dict) -> tuple[bool, str]:
        return True, ""

    @staticmethod
    def _parse_title(title: str) -> str:
        return "_".join(title.strip().split())

    @staticmethod
    def dl_link_builder(host_url: str, chapter_hash: str, page: str) -> str:
        return f"{host_url}/data/{chapter_hash}/{page}"
