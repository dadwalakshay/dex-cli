import json
import os
from datetime import datetime

import requests
import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt

from dex.config import (
    _META_STORE,
    DEFAULT_PDF_NAME,
    DEFAULT_STORAGE_PATH,
    IS_DISCORD_ENABLED,
)
from dex.db import read_chapter_meta
from dex.discord import DiscordClient
from dex.integrations.base import BaseClient
from dex.utils import _get_dirs, _open_file

console = Console()
err_console = Console(stderr=True)


def choose_manga_prompt(client: BaseClient, results: dict) -> dict:
    choice_map = client.get_manga_choices(results, console)

    if not choice_map:
        err_console.print("No Mangas found.")

        raise typer.Exit(code=1)

    manga_obj = choice_map[
        Prompt.ask(
            "Which one would you like to explore?",
            choices=list(choice_map.keys()),
            show_choices=False,
        )
    ]

    return manga_obj


def choose_chapter_prompt(client: BaseClient, results: dict) -> dict:
    choice_map = client.get_chapter_choices(results, console)

    if not choice_map:
        err_console.print("No Chapters found.")

        raise typer.Exit(code=1)

    chapter_obj = choice_map[
        Prompt.ask(
            "Which chapter you want to download?",
            choices=list(choice_map.keys()),
            show_choices=False,
        )
    ]

    return chapter_obj


def confirm_download_prompt(
    client_obj: BaseClient, manga_obj: dict, chapter_obj: dict
) -> None:
    manga_title, chapter_title = client_obj.get_titles(manga_obj, chapter_obj)

    if Confirm.ask(f"Do you want to download {manga_title} - {chapter_title}?"):
        _status, result = client_obj.download_chapter(manga_obj, chapter_obj)

        if not _status:
            console.print(result)

            raise typer.Exit(1)

        if IS_DISCORD_ENABLED:
            discord_client_obj = DiscordClient(result)

            try:
                discord_client_obj.send_file_webhook()
            except (requests.HTTPError, requests.ConnectionError, requests.ReadTimeout):
                err_console.print("Download completed, but Discord webhook failed.")

    console.print("Arigato!")

    raise typer.Exit(code=0)


def confirm_read_prompt(chapter_path: str) -> bool:
    is_read = False

    _meta_path = f"{chapter_path}/{_META_STORE}"

    with open(_meta_path, "r") as _meta_json_r:
        _meta_json_obj = json.loads(_meta_json_r.read())

        last_read_at = _meta_json_obj.get("last_read_at", "")

        if Confirm.ask(
            "Do you want to read"
            f" {_meta_json_obj['manga_title']} -"
            f" {_meta_json_obj['chapter_title']}?"
            f" {('- Last read at ' + last_read_at) if last_read_at else ''}"
        ):
            _open_file(f"{chapter_path}/{DEFAULT_PDF_NAME}")

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
        confirm_read_prompt(curr_path)

        ls_dir(f"{curr_path}/../")

    _dirs = sorted(_get_dirs(curr_path, paths))

    choice_map = {
        "0": "../",
    }

    console.print("(0) <back>")

    for choice, _dir in enumerate(_dirs, 1):
        choice_map[str(choice)] = _dir

        chapter_meta = read_chapter_meta(f"{curr_path}/{_dir}")

        last_read_at = chapter_meta.get("last_read_at", "")

        console.print(
            f"({choice})"
            f" {_dir} {('- Last read at ' + last_read_at) if last_read_at else ''}"
        )

    _selected_dir = choice_map[
        Prompt.ask(
            "Please choose directory",
            choices=list(choice_map.keys()),
            show_choices=False,
        )
    ]

    ls_dir(f"{curr_path}/{_selected_dir}")
