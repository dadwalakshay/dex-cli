import os
import uuid

import requests
from rich.progress import track

from config import BASE_URL, DEFAULT_STORAGE_PATH


class MangaDexClient:
    def __init__(self):
        os.makedirs(DEFAULT_STORAGE_PATH, exist_ok=True)

    @staticmethod
    def _parse_title(title: str) -> str:
        return "_".join(title.strip().split())

    @staticmethod
    def _parse_error_resp(resp) -> str:
        if resp.status_code >= 500:
            return f"{BASE_URL} service(s) are down."

        error_resp = resp.json()

        return " |".join(map(lambda err: err["title"], error_resp["errors"]))

    @classmethod
    def handler(cls, url: str, params: dict = {}, json: dict = {}) -> tuple[bool, dict]:
        response = requests.get(url, params)

        if response.status_code >= 400:
            return False, {"errors": cls._parse_error_resp(response)}

        return True, response.json()

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
        for page_link in track(links, description="Downloading chapter..."):
            filename = page_link.split("/")[-1]
            ext = page_link.split(".")[-1]

            file_path = f"{path}/{filename}.{ext}"

            if not os.path.exists(file_path):
                with requests.get(page_link, stream=True) as r_ctx:
                    r_ctx.raise_for_status()

                    with open(file_path, "wb") as page:
                        for chunk in r_ctx.iter_content(chunk_size=8192):
                            page.write(chunk)

        return True

    def search(self, title: str) -> tuple[bool, dict]:
        URL = f"{BASE_URL}/manga"

        PARAMS = {"title": title}

        return self.handler(URL, PARAMS)

    def list_chapters(self, manga_id: str, language: str = "en") -> tuple[bool, dict]:
        URL = f"{BASE_URL}/manga/{manga_id}/feed"

        PARAMS = {"translatedLanguage[]": language}

        return self.handler(URL, PARAMS)

    def download_chapter(
        self, chapter_id: str, manga_title: str, chapter_title: str
    ) -> tuple[bool, str]:
        URL = f"{BASE_URL}/at-home/server/{chapter_id}"

        _status, response = self.handler(URL)

        if not _status:
            return _status, response

        host_base_url = response["baseUrl"]

        chapter_hash = response["chapter"]["hash"]

        dl_links = [
            self.dl_link_builder(host_base_url, chapter_hash, page)
            for page in response["chapter"]["data"]
        ]

        dl_path = (
            f"{DEFAULT_STORAGE_PATH}/{self._parse_title(manga_title)}"
            f"/{self._parse_title(chapter_title)}"
        )

        os.makedirs(dl_path, exist_ok=True)

        try:
            self.dl_threaded(dl_links, dl_path)
        except Exception as e:
            return False, str(e)

        return True, ""
