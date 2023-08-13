import os
from abc import ABC, abstractmethod

import requests

from dex.config import DEFAULT_STORAGE_PATH


class BaseClient(ABC):
    def __init__(self) -> None:
        os.makedirs(DEFAULT_STORAGE_PATH, exist_ok=True)

    @staticmethod
    def _parse_title(title: str) -> str:
        return "_".join(title.strip().split())

    @staticmethod
    @abstractmethod
    def get_manga_title(manga: dict) -> str:
        return ""

    @staticmethod
    @abstractmethod
    def get_chapter_title(chapter: dict) -> str:
        return ""

    @staticmethod
    @abstractmethod
    def get_chapter_volume_num(chapter: dict) -> int:
        return 0

    @staticmethod
    @abstractmethod
    def get_chapter_num(chapter: dict) -> int:
        return 0

    @staticmethod
    @abstractmethod
    def get_chapter_page_count(chapter: dict) -> int:
        return 0

    @staticmethod
    @abstractmethod
    def dl_link_builder(*args, **kwargs) -> str:
        return ""

    @classmethod
    @abstractmethod
    def _parse_error_resp(cls, resp: requests.Response) -> str:
        return ""

    @classmethod
    @abstractmethod
    def handler(cls, url: str, params: dict = {}, json: dict = {}) -> tuple[bool, dict]:
        return False, {}

    @classmethod
    @abstractmethod
    def list_mangas(self, title: str) -> tuple[bool, dict]:
        return True, {}

    @classmethod
    @abstractmethod
    def list_chapters(self, manga_obj: dict, language: str = "en") -> tuple[bool, dict]:
        return True, {}

    @classmethod
    @abstractmethod
    def download_chapter(self, manga_obj: dict, chapter_obj: dict) -> tuple[bool, str]:
        return True, ""

    @abstractmethod
    def get_manga_choices(title: str) -> tuple[bool, list | str]:
        return False, {}

    @abstractmethod
    def get_chapter_choices(manga: dict) -> tuple[bool, list | str]:
        return False, {}
