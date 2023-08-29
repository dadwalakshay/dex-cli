import os
import subprocess
import sys


def _open_file(path: str) -> None:
    match sys.platform:
        case "darwin":
            subprocess.Popen(["open", path])
        case "linux":
            subprocess.Popen(["xdg-open", path])
        case _:
            raise OSError(
                "dex-cli currently does not support reading manga on this OS."
            )


def _get_dirs(curr_path: str, paths: list[str]) -> list[str]:
    return [_path for _path in paths if os.path.isdir(f"{curr_path}/{_path}")]
