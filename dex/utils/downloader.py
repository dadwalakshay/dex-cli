import os

import requests
from rich.progress import track


class BulkDownloader:
    def __init__(
        self, links: list[str], path: str, pool_size: int = 5, batch_size: int = 10
    ) -> None:
        self.links = links
        self.path = path

        self.pool_size = pool_size
        self.batch_size = batch_size

    def download(self, mode: str = "seq") -> list[str]:
        match mode:
            case "seq":
                _filenames = self.seq_download(self.links, self.path)
            case _:
                raise NotImplementedError("Un-supported download mode.")

        return _filenames

    @classmethod
    def seq_download(cls, links: list[str], path: str) -> list[str]:
        _filenames = []

        for page_count, page_link in track(
            enumerate(links, start=1), description="Downloading chapter..."
        ):
            raw_filename = page_link.split("/")[-1]

            ordered_filename = f"{str(page_count).zfill(3)}-{raw_filename}"

            file_path = f"{path}/{ordered_filename}"

            if not os.path.exists(file_path):
                with requests.get(page_link, stream=True) as r_ctx:
                    r_ctx.raise_for_status()

                    with open(file_path, "wb") as page:
                        for chunk in r_ctx.iter_content(chunk_size=8192):
                            page.write(chunk)

            _filenames.append(ordered_filename)

        return _filenames

    @classmethod
    def th_download(cls, pool_size: int, batch_size: int) -> list[str]:
        return []

    @classmethod
    def mp_download(cls, pool_size: int, batch_size: int) -> list[str]:
        return []
