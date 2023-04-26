import uuid

from .config import BASE_URL, DEFAULT_STORAGE_PATH


class MangaDexClient:
    @staticmethod
    def _parsed_title(title: str) -> str:
        return title.strip()

    @staticmethod
    def handler(url: str, params: dict = {}, json: dict = {}) -> tuple[bool, dict]:
        return True, {}

    @staticmethod
    def is_valid_uuid(value: str) -> bool:
        try:
            uuid.UUID(value)
        except (TypeError, ValueError):
            return False

        return True

    @staticmethod
    def dl_link_builder(host_url: str, chapter_hash: str, page: str):
        return f"{host_url}/data/{chapter_hash}/{page}"

    @staticmethod
    def dl_threaded(links: list, path: str) -> bool:
        return True

    def search(self, title: str) -> list:
        URL = f"{BASE_URL}/manga"

        PARAMS = {"title": self._parsed_title(title)}

        _status, response = self.handler(URL, PARAMS)

        return response["data"] if _status else response["errors"]

    def list_chapters(self, manga_id: str, language: str = "en") -> list:
        URL = f"{BASE_URL}/manga/{manga_id}/feed"

        PARAMS = {"translatedLanguage[]": language}

        _status, response = self.handler(URL, PARAMS)

        return response["data"] if _status else response["errors"]

    def download_chapter(self, chapter_id: str, title: str) -> bool:
        URL = f"{BASE_URL}/at-home/server/{chapter_id}"

        _status, response = self.handler(URL)

        if _status:
            return response["errors"]

        host_base_url = response["baseUrl"]

        chapter_hash = response["chapter"]["hash"]

        dl_links = [
            self.dl_link_builder(host_base_url, chapter_hash, page)
            for page in response["chapter"]["data"]
        ]

        dl_path = f"{DEFAULT_STORAGE_PATH}/{self._parsed_title(title)}"

        try:
            self.dl_threaded(dl_links, dl_path)
        except Exception:
            return False

        return True
