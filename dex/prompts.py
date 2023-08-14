import json
import os
from datetime import datetime

import typer
from beaupy import Config, confirm, select, select_multiple
from rich.console import Console
from rich.progress import track

from dex.config import _META_STORE, DEFAULT_PDF_NAME, DEFAULT_STORAGE_PATH
from dex.db import read_chapter_meta
from dex.integrations.base import BaseClient
from dex.utils import _get_dirs, _open_file

console = Console(style="#00c38b")
err_console = Console(stderr=True, style="bold red")


Config.raise_on_escape = True
Config.raise_on_interrupt = True


def banner():
    banner = """
        ██████╗ ███████╗██╗  ██╗      ██████╗██╗     ██╗
        ██╔══██╗██╔════╝╚██╗██╔╝     ██╔════╝██║     ██║
        ██║  ██║█████╗   ╚███╔╝█████╗██║     ██║     ██║
        ██║  ██║██╔══╝   ██╔██╗╚════╝██║     ██║     ██║
        ██████╔╝███████╗██╔╝ ██╗     ╚██████╗███████╗██║
        ╚═════╝ ╚══════╝╚═╝  ╚═╝      ╚═════╝╚══════╝╚═╝

        Made by Akshay Dadwal | https://github.com/dadwalakshay | Press "ctrl + c" to quit.
    """  # noqa: E501

    console.print(banner)


def choose_manga_prompt(client: BaseClient, title: str) -> dict:
    _status, resp = client.get_manga_choices(title)

    if not _status:
        err_console.print(resp)

        raise typer.Exit(code=1)

    console.print("Which Manga would you like to download?")

    manga_obj = resp[
        select(
            options=[client.get_manga_title(manga) for manga in resp]
            + [
                "Quit",
            ],
            cursor_style="#00c38b",
            return_index=True,
            pagination=True,
            page_size=10,
        )
    ]

    return manga_obj


def choose_chapter_prompt(client: BaseClient, manga: dict) -> dict:
    _status, resp = client.get_chapter_choices(manga)

    if not _status:
        err_console.print(resp)

        raise typer.Exit(code=1)

    console.print("Which Manga chapter would you like to download?")

    non_empty_chapters = list(
        filter(lambda chapter: client.get_chapter_page_count(chapter) > 0, resp)
    )

    selected_chapter_idx = select_multiple(
        options=[
            f"Title: {client.get_chapter_title(chapter)} - "
            f"Volume: {client.get_chapter_volume_num(chapter)} - "
            f"Chapter: {client.get_chapter_num(chapter)} - "
            f"Pages: {client.get_chapter_page_count(chapter)}"
            for chapter in non_empty_chapters
        ],
        cursor_style="#00c38b",
        tick_character="x",
        tick_style="#00c38b",
        return_indices=True,
        pagination=True,
        page_size=10,
    )

    selected_chapters = list(map(non_empty_chapters.__getitem__, selected_chapter_idx))

    return selected_chapters


def confirm_download_prompt(
    client_obj: BaseClient, manga_obj: dict, chapter_objs: list
) -> None:
    if confirm(
        question="Do you want to download selected chapter(s)?",
        cursor_style="#00c38b",
        default_is_yes=False,
    ):
        for chapter_obj in track(
            chapter_objs, description="Downloading selected chapter(s)..."
        ):
            _status, result = client_obj.download_chapter(manga_obj, chapter_obj)

            if not _status:
                console.print(result)

                raise typer.Exit(1)

            console.print(f"{client_obj.get_chapter_title(chapter_obj)}, downloaded.")

    console.print("Arigato!")

    raise typer.Exit(code=0)


def confirm_read_prompt(chapter_path: str) -> bool:
    is_read = False

    _meta_path = f"{chapter_path}/{_META_STORE}"

    with open(_meta_path, "r") as _meta_json_r:
        _meta_json_obj = json.loads(_meta_json_r.read())

        last_read_at = _meta_json_obj.get("last_read_at", "")

        if confirm(
            question=(
                "Do you want to read"
                f" {_meta_json_obj['manga_title']} -"
                f" {_meta_json_obj['chapter_title']}?"
                f" {('- Last read at ' + last_read_at) if last_read_at else 'N/A'}"
            ),
            cursor_style="#00c38b",
            default_is_yes=True,
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

    _dirs.insert(0, "../")

    _selected_dir = _dirs[
        select(
            options=[
                f" {_dir} {('- Last read at ' + (read_chapter_meta(f'{curr_path}/{_dir}').get('last_read_at') or 'N/A'))}"  # noqa: E501
                for _dir in _dirs
            ]
            + [
                "Quit",
            ],
            cursor_style="#00c38b",
            return_index=True,
            pagination=True,
            page_size=10,
        )
    ]

    ls_dir(f"{curr_path}/{_selected_dir}")
