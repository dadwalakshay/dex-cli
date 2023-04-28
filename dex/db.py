def get_mangas(_meta: dict) -> list:
    return _meta["mangas"]


def get_chapters(_meta: dict) -> list:
    return _meta["chapters"]


def get_page_meta(_meta: dict) -> dict:
    return _meta["pages"]
