import typer

from dex.integrations import ClientFactory
from dex.prompts import (
    banner,
    choose_chapter_prompt,
    choose_manga_prompt,
    confirm_download_prompt,
    err_console,
    ls_dir,
)

app = typer.Typer()

banner()


@app.command()
def download(title: str, code: str = "mangadex") -> None:
    client_obj = ClientFactory.get_client(code)

    try:
        manga_obj = choose_manga_prompt(client_obj, title)

        chapter_objs = choose_chapter_prompt(client_obj, manga_obj)

        confirm_download_prompt(client_obj, manga_obj, chapter_objs)
    except (KeyboardInterrupt, IndexError):
        err_console.print("Bye Bye!")


@app.command()
def explore() -> None:
    try:
        ls_dir()
    except (KeyboardInterrupt, IndexError):
        err_console.print("Bye Bye!")
