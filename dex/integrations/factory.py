from dex.config import DEFAULT_MANGA_CLIENT_CODE
from dex.integrations.base import BaseClient
from dex.integrations.mangadex import MangaDexClient

CLIENT_KLASS_MAP = {
    "mangadex": MangaDexClient,
}


class ClientFactory:
    def __new__(cls, code: str = "", *args, **kwargs):
        code = code or DEFAULT_MANGA_CLIENT_CODE

        klass = CLIENT_KLASS_MAP.get(code, None)

        if not issubclass(klass, BaseClient):
            raise NotImplementedError(
                f"Sorry, We do not support {code} integration yet."
            )

        return klass(*args, **kwargs)
