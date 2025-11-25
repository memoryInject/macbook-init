import subprocess
from typing import Union, List

from lib.tui import console, confirm
from utils.errors import UserCancelled


def run(cmd: Union[str, List[str]], show_log: bool = True, show_dialog: bool = True):
    if show_log:
        console.warning(f"executing shell command: {cmd}")

    if show_dialog:
        if not confirm(prompt="Continue?"):
            raise UserCancelled("User cancelled command execution")

    return subprocess.run(
        cmd,
        shell=True,
        executable="/bin/bash",
        capture_output=True,
        check=True,
        text=True,
    )
