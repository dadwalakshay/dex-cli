import typer
from dotenv import load_dotenv

from dex.client import MangaDexClient
from dex.prompts import (
    choose_chapter_prompt,
    choose_manga_prompt,
    confirm_download_prompt,
    err_console,
    line_break_console,
    ls_dir,
)

load_dotenv()

app = typer.Typer()


@app.command()
def download(title: str):
    line_break_console()

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

    chapter_id, chapter_attr = choose_chapter_prompt(chapter_results)

    confirm_download_prompt(client_obj, chapter_id, manga_title, chapter_attr)


@app.command()
def explore():
    line_break_console()

    ls_dir()
