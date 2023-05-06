from dex.integrations.base import BaseClient
from dex.integrations.mangadex import MangaDexClient


class ClientFactory:
    @staticmethod
    def get_client(code: str) -> BaseClient:
        match code:
            case "mangadex":
                klass = MangaDexClient
            case "":
                # default client when no User input is provided
                klass = MangaDexClient
            case _:
                raise NotImplementedError("Un-supported client.")

        return klass()
