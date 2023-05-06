import os
import subprocess


def _open_file(path: str) -> None:
    subprocess.Popen(["xdg-open", path])


def _get_dirs(curr_path: str, paths: list[str]) -> list[str]:
    return [_path for _path in paths if os.path.isdir(f"{curr_path}/{_path}")]
