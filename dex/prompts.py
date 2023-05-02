import os

import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt

from dex.client import MangaDexClient
from dex.utils import _open_chapter

console = Console()
err_console = Console(stderr=True)


def line_break_console() -> None:
    console.print(f"\n{os.get_terminal_size().columns * '+'}\n")


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
        Prompt.ask(
            "Which one would you like to explore?",
            choices=choice_map.keys(),
            show_choices=False,
        )
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

        volume = result["attributes"]["volume"]
        chapter = result["attributes"]["chapter"]

        choice_map[str(choice)] = result

        console.print(f"({choice}) {title} - {volume}/{chapter} - Pages: {page_count}")

    chapter_obj = choice_map[
        Prompt.ask(
            "Which chapter you want to download?",
            choices=choice_map.keys(),
            show_choices=False,
        )
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


def ls_manga_prompt(manga_ls: list) -> dict:
    choice_map = {}

    for choice, result in enumerate(manga_ls, 1):
        title = result["title"]

        choice_map[str(choice)] = result

        console.print(f"({choice}) {title}")

    manga_obj = choice_map[
        Prompt.ask(
            "Which one would you like to explore?",
            choices=choice_map.keys(),
            show_choices=False,
        )
    ]

    return manga_obj


def ls_chapter_prompt(chapter_ls: list) -> dict:
    choice_map = {}

    for choice, result in enumerate(chapter_ls, 1):
        title = result["title"]

        choice_map[str(choice)] = result

        console.print(f"({choice}) {title}")

    chapter_obj = choice_map[
        Prompt.ask(
            "Which one would you like to read?",
            choices=choice_map.keys(),
            show_choices=False,
        )
    ]

    return chapter_obj


def confirm_read_prompt(
    manga_title: str, chapter_title: str, chapter_path: str
) -> bool:
    if Confirm.ask(f"Do you want to read {manga_title} - {chapter_title}?"):
        _open_chapter(chapter_path)

        return True

    return False
