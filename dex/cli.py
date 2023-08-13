import typer

from dex.integrations import ClientFactory
from dex.prompts import (
    choose_chapter_prompt,
    choose_manga_prompt,
    confirm_download_prompt,
    ls_dir,
)

app = typer.Typer()


@app.command()
def download(title: str, code: str = "mangadex") -> None:
    client_obj = ClientFactory.get_client(code)

    manga_obj = choose_manga_prompt(client_obj, title)

    chapter_objs = choose_chapter_prompt(client_obj, manga_obj)

    confirm_download_prompt(client_obj, manga_obj, chapter_objs)


@app.command()
def explore() -> None:
    ls_dir()
