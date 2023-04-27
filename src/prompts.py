import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt

from client import MangaDexClient

console = Console()
err_console = Console(stderr=True)


def choose_manga_prompt(results: dict) -> tuple[str, str]:
    if not results["data"]:
        err_console.print("No results found.")

        raise typer.Exit(code=1)

    choice_map = {}

    for choice, result in enumerate(results["data"], 1):
        title = result["attributes"]["title"]["en"]

        choice_map[str(choice)] = result

        console.print(f"({choice}) {title}")

    manga_obj = choice_map[
        Prompt.ask("Which one would you like to explore?", choices=choice_map.keys())
    ]

    return manga_obj["id"], manga_obj["attributes"]["title"]["en"]


def choose_chapter_prompt(results: dict) -> tuple[str, str]:
    if not results["data"]:
        err_console.print("No results found.")

        raise typer.Exit(code=1)

    choice_map = {}

    for choice, result in enumerate(results["data"], 1):
        title = result["attributes"]["title"]

        page_count = result["attributes"]["pages"]

        choice_map[str(choice)] = result

        console.print(f"({choice}) {title} - Pages: {page_count}")

    chapter_obj = choice_map[
        Prompt.ask("Which chapter you want to download?", choices=choice_map.keys())
    ]

    return chapter_obj["id"], chapter_obj["attributes"]["title"]


def confirm_download_prompt(
    client_obj: MangaDexClient, chapter_id: str, manga_title: str, chapter_title: str
) -> None:
    if Confirm.ask(f"Do you want to download {manga_title} - {chapter_title}?"):
        _status, error = client_obj.download_chapter(
            chapter_id, manga_title, chapter_title
        )

        if not _status:
            console.print(error)

            raise typer.Exit(1)

    console.print("Arigato!")

    raise typer.Exit(code=0)
