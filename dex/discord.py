import requests

from dex.config import DEFAULT_DISCORD_WEBHOOK_URL


class DiscordClient:
    def __init__(self, path: str) -> None:
        self.path = path

    def send_file_webhook(self) -> None:
        with open(f"{self.path}/dl.pdf", "rb") as _file:
            requests.post(
                DEFAULT_DISCORD_WEBHOOK_URL,
                files={"files": _file},
                data={"content": self.path.split("/")[-1]},
            )

        return
