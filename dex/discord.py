import requests

from dex.config import DEFAULT_DISCORD_WEBHOOK_URL, DEFAULT_PDF_NAME


class DiscordClient:
    def __init__(self, path: str) -> None:
        self.path = path

    def send_file_webhook(self) -> None:
        with open(f"{self.path}/{DEFAULT_PDF_NAME}", "rb") as _file:
            requests.post(
                DEFAULT_DISCORD_WEBHOOK_URL,
                files={"files": _file},
                data={"content": self.path.split("/")[-1]},
            )

        return
