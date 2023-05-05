import json
import os
from datetime import datetime

import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt

from dex.client import MangaDexClient
from dex.config import _META_STORE, DEFAULT_STORAGE_PATH
from dex.utils import _get_dirs, _open_chapter

console = Console()
err_console = Console(stderr=True)


def line_break_console() -> None:
    console.print(f"\n{os.get_terminal_size().columns * '+'}\n")


def choose_manga_prompt(results: dict) -> dict:
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

    return manga_obj


def choose_chapter_prompt(results: dict) -> dict:
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

    return chapter_obj


def confirm_download_prompt(
    client_obj: MangaDexClient, manga_obj: dict, chapter_obj: dict
) -> None:
    if Confirm.ask(
        f"Do you want to download {manga_obj['attributes']['title']['en']} -"
        f" {chapter_obj['attributes']['title']}?"
    ):
        _status, error = client_obj.download_chapter(manga_obj, chapter_obj)

        if not _status:
            console.print(error)

            raise typer.Exit(1)

    console.print("Arigato!")

    raise typer.Exit(code=0)


def confirm_read_prompt(chapter_path: str) -> bool:
    is_read = False

    _meta_path = f"{chapter_path}/{_META_STORE}"

    with open(_meta_path, "r") as _meta_json_r:
        _meta_json_obj = json.loads(_meta_json_r.read())

        if Confirm.ask(
            "Do you want to read"
            f" {_meta_json_obj['manga']['attributes']['title']['en']} -"
            f" {_meta_json_obj['chapter']['attributes']['title']}? - Last read at"
            f" {_meta_json_obj['last_read_at']}"
        ):
            _open_chapter(chapter_path)

            is_read = True

    if is_read:
        with open(_meta_path, "w") as _meta_json_w:
            _meta_json_obj["last_read_at"] = str(datetime.now().date())

            _meta_json_w.write(json.dumps(_meta_json_obj))

    return is_read


def ls_dir(path: str = "") -> None:
    curr_path = path or DEFAULT_STORAGE_PATH

    paths = os.listdir(curr_path)

    if _META_STORE in paths:
        if confirm_read_prompt(curr_path):
            raise typer.Exit(code=0)

    _dirs = _get_dirs(curr_path, paths)

    choice_map = {
        "0": "../",
    }

    console.print("(0) <back>")

    for choice, _dir in enumerate(_dirs, 1):
        choice_map[str(choice)] = _dir

        console.print(f"({choice}) {_dir}")

    _selected_dir = choice_map[
        Prompt.ask(
            "Please choose directory",
            choices=choice_map.keys(),
            show_choices=False,
        )
    ]

    ls_dir(f"{curr_path}/{_selected_dir}")
