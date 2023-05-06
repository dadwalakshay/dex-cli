import os

import requests

from dex.config import DEFAULT_STORAGE_PATH
from dex.db import create_or_update_chapter_meta
from dex.integrations.base import BaseClient
from dex.utils import BulkDownloader, PDFGenerator


class MangaDexClient(BaseClient):
    BASE_URL = "https://api.mangadex.org"

    @classmethod
    def _parse_error_resp(cls, resp: requests.Response) -> str:
        if resp.status_code >= 500:
            return f"{cls.BASE_URL} service(s) are down."

        error_resp = resp.json()

        return " |".join(map(lambda err: err["title"], error_resp["errors"]))

    @classmethod
    def handler(cls, url: str, params: dict = {}, json: dict = {}) -> tuple[bool, dict]:
        response = requests.get(url, params)

        if response.status_code >= 400:
            return False, {"errors": cls._parse_error_resp(response)}

        return True, response.json()

    def list_mangas(self, title: str) -> tuple[bool, dict]:
        URL = f"{self.BASE_URL}/manga"

        PARAMS = {"title": title}

        return self.handler(URL, PARAMS)

    def list_chapters(self, manga_obj: dict, language: str = "en") -> tuple[bool, dict]:
        URL = f"{self.BASE_URL}/manga/{manga_obj['id']}/feed"

        PARAMS = {
            "translatedLanguage[]": language,
            "order[volume]": "asc",
            "order[chapter]": "asc",
        }

        return self.handler(URL, PARAMS)

    def download_chapter(self, manga_obj: dict, chapter_obj: dict) -> tuple[bool, str]:
        URL = f"{self.BASE_URL}/at-home/server/{chapter_obj['id']}"

        _status, response = self.handler(URL)

        if not _status:
            return _status, response["errors"]

        host_base_url = response["baseUrl"]

        chapter_hash = response["chapter"]["hash"]
        chapter_attr = chapter_obj["attributes"]

        dl_links = [
            self.dl_link_builder(host_base_url, chapter_hash, page)
            for page in response["chapter"]["data"]
        ]

        dl_path = (
            f"{DEFAULT_STORAGE_PATH}"
            f"/{self._parse_title(manga_obj['attributes']['title']['en'])}"
            f"/{self._parse_title(chapter_attr['title'])}"
        )

        manga_volume = chapter_attr["volume"]

        if manga_volume:
            dl_path += f"_{manga_volume}"

        manga_chapter = chapter_attr["chapter"]

        if manga_chapter:
            dl_path += f"_{manga_chapter}"

        os.makedirs(dl_path, exist_ok=True)

        bulk_downloader = BulkDownloader(dl_links, dl_path)

        if dl_filenames := bulk_downloader.download():
            pdf_generator = PDFGenerator(dl_filenames, dl_path)

            pdf_generator.generate()

            create_or_update_chapter_meta(dl_path, manga_obj, chapter_obj)

            return True, ""

        return False, "Download failed."
