import typer
from dotenv import load_dotenv

from client import MangaDexClient
from prompts import (
    choose_chapter_prompt,
    choose_manga_prompt,
    confirm_download_prompt,
    err_console,
)

load_dotenv()

app = typer.Typer()


@app.command()
def search(title: str):
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
def main():
    return


if __name__ == "__main__":
    app()
