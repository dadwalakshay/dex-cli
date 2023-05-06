import os

DEFAULT_STORAGE_PATH = os.environ.get("DEFAULT_STORAGE_PATH", "manga_dl")

DEFAULT_PDF_NAME = os.environ.get("DEFAULT_PDF_NAME", "dl.pdf")

DEFAULT_MANGA_CLIENT_CODE = os.environ.get("DEFAULT_MANGA_CLIENT_CODE", "mangadex")

_META_STORE = os.environ.get("DEFAULT_META_STORE", "_meta.json")
