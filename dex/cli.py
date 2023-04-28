import typer
from dotenv import load_dotenv

from dex.client import MangaDexClient
from dex.db import get_chapters, get_mangas, get_page_meta
from dex.prompts import (
    choose_chapter_prompt,
    choose_manga_prompt,
    confirm_download_prompt,
    err_console,
    ls_chapter_prompt,
    ls_manga_prompt,
    page_meta_console,
)
from dex.utils import _meta_parser

load_dotenv()

app = typer.Typer()


@app.command()
def download(title: str):
    client_obj = MangaDexClient()

    _status, manga_results = client_obj.search(title)

    if not _status:
        err_console.print(manga_results["errors"])

        raise typer.Exit(code=1)

    manga_id, manga_title = choose_manga_prompt(manga_results)

    _status, chapter_results = client_obj.list_chapters(manga_id)

    if not _status:
        err_console.print(chapter_results["errors"])

        raise typer.Exit(code=1)

    chapter_id, chapter_title = choose_chapter_prompt(chapter_results)

    confirm_download_prompt(client_obj, chapter_id, manga_title, chapter_title)


@app.command()
def explore():
    manga_ls = get_mangas(_meta_parser())

    manga_obj = ls_manga_prompt(manga_ls)

    chapter_ls = get_chapters(_meta_parser(manga_obj["path"]))

    chapter_obj = ls_chapter_prompt(chapter_ls)

    page_meta = get_page_meta(_meta_parser(chapter_obj["path"]))

    page_meta_console(page_meta, chapter_obj["path"])
