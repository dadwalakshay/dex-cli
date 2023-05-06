import os
from abc import ABC, abstractmethod

import requests
from PIL import Image
from rich.progress import track

from dex.config import DEFAULT_PDF_NAME, DEFAULT_STORAGE_PATH


class BaseClient(ABC):
    def __init__(self, *args, **kwargs):
        os.makedirs(DEFAULT_STORAGE_PATH, exist_ok=True)

    @staticmethod
    @abstractmethod
    def _ordered_filename(*args, **kwargs):
        return

    @classmethod
    @abstractmethod
    def _parse_error_resp(*args, **kwargs):
        return

    @classmethod
    @abstractmethod
    def handler(cls, *args, **kwargs):
        return

    @abstractmethod
    def list_mangas(self, *args, **kwargs):
        return

    @abstractmethod
    def list_chapters(self, *args, **kwargs):
        return

    @abstractmethod
    def download_chapter(self, *args, **kwargs):
        return

    @staticmethod
    def _parse_title(title: str) -> str:
        return "_".join(title.strip().split())

    @staticmethod
    def _pdf_builder(path: str) -> None:
        filename_ls = os.listdir(path)

        sorted_filename_iter = filter(
            lambda filename: (".json" not in filename) and (".pdf" not in filename),
            sorted(filename_ls),
        )

        pil_image_ls = list(
            map(
                lambda filename: Image.open(f"{path}/{filename}").convert("RGB"),
                sorted_filename_iter,
            )
        )

        if pil_image_ls:
            pil_image_ls[0].save(
                f"{path}/{DEFAULT_PDF_NAME}",
                save_all=True,
                append_images=pil_image_ls[1:],
            )

            # Uncomment this if you want to enable auto-clean-up of downloaded images
            # os.system(f"rm -r {path}/*.{ext}")

    @staticmethod
    def dl_link_builder(host_url: str, chapter_hash: str, page: str):
        return f"{host_url}/data/{chapter_hash}/{page}"

    @classmethod
    def dl_threaded(cls, links: list, path: str) -> bool:
        for page_link in track(links, description="Downloading chapter..."):
            raw_filename = page_link.split("/")[-1]

            ordered_filename = cls._ordered_filename(raw_filename)

            file_path = f"{path}/{ordered_filename}"

            if not os.path.exists(file_path):
                with requests.get(page_link, stream=True) as r_ctx:
                    r_ctx.raise_for_status()

                    with open(file_path, "wb") as page:
                        for chunk in r_ctx.iter_content(chunk_size=8192):
                            page.write(chunk)

        cls._pdf_builder(path)

        return True
