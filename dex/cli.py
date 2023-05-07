import typer

from dex.integrations import ClientFactory
from dex.prompts import (
    choose_chapter_prompt,
    choose_manga_prompt,
    confirm_download_prompt,
    err_console,
    ls_dir,
)

app = typer.Typer()


@app.command()
def download(title: str, code: str = "") -> None:
    client_obj = ClientFactory.get_client(code)

    _status, manga_results = client_obj.list_mangas(title)

    if not _status:
        err_console.print(manga_results["errors"])

        raise typer.Exit(code=1)

    manga_obj = choose_manga_prompt(client_obj, manga_results)

    _status, chapter_results = client_obj.list_chapters(manga_obj)

    if not _status:
        err_console.print(chapter_results["errors"])

        raise typer.Exit(code=1)

    chapter_obj = choose_chapter_prompt(client_obj, chapter_results)

    confirm_download_prompt(client_obj, manga_obj, chapter_obj)


@app.command()
def explore() -> None:
    ls_dir()
