import os
from multiprocessing.pool import ThreadPool

import requests


class BulkDownloader:
    def __init__(self, links: list[str], path: str) -> None:
        self.links = links
        self.path = path

    def download(self, mode: str = "th") -> list[str]:
        match mode:
            case "seq":
                _filenames = self.seq_download()
            case "th":
                _filenames = self.th_download()
            case _:
                raise NotImplementedError("Un-supported download mode.")

        return _filenames

    @staticmethod
    def _save_link(page_args: tuple[int, str, str]) -> str:
        count = page_args[0]
        link = page_args[1]
        path = page_args[2]

        raw_filename = link.split("/")[-1]

        ordered_filename = f"{str(count).zfill(3)}-{raw_filename}"

        file_path = f"{path}/{ordered_filename}"

        if not os.path.exists(file_path):
            with requests.get(link, stream=True) as r_ctx:
                r_ctx.raise_for_status()

                with open(file_path, "wb") as page:
                    for chunk in r_ctx.iter_content(chunk_size=8192):
                        page.write(chunk)

        return ordered_filename

    def seq_download(self) -> list[str]:
        _filenames = []

        for page_count, page_link in enumerate(self.links, start=1):
            _filenames.append(self._save_link((page_count, page_link, self.path)))

        return _filenames

    def th_download(self) -> list[str]:
        _fieldnames = []

        pages = (
            (page_count, page_link, self.path)
            for page_count, page_link in enumerate(self.links, start=1)
        )

        with ThreadPool() as th_pool:
            for result in th_pool.map(self._save_link, pages):
                _fieldnames.append(result)

        return _fieldnames
