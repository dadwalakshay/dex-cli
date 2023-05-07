import os

DEFAULT_STORAGE_PATH = os.environ.get("DEFAULT_STORAGE_PATH", "manga_dl")

DEFAULT_PDF_NAME = os.environ.get("DEFAULT_PDF_NAME", "dl.pdf")

_META_STORE = os.environ.get("DEFAULT_META_STORE", "_meta.json")

IS_DISCORD_ENABLED = os.environ.get("IS_DISCORD_ENABLED", "False") == "True"

DEFAULT_DISCORD_WEBHOOK_URL = os.environ.get("DEFAULT_DISCORD_WEBHOOK_URL", "")
