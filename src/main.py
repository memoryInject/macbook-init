import json
import re
from pathlib import Path
from typing import List

from lib.dmg import DmgManagement
from lib import bash
from lib.tui import console
from utils.errors import UserCancelled

BASE_DIR = Path(__file__).parent.parent
TASKS_FILE = BASE_DIR / "tasks.json"


def parse_prefix(filename: str):
    """Extract numeric prefix from filename for fallback ordering."""
    match = re.match(r"(\d+)_", filename)
    return int(match.group(1)) if match else float("inf")


def run_bash_task(script_path: Path, show_log=True, show_dialog=True):
    """Execute a bash script."""
    cmd = f"bash {script_path}"

    try:
        bash.run(cmd, show_log=show_log, show_dialog=show_dialog)
    except BaseException as e:
        console.error(e)


def run_dmg_tasks(urls: List[str]):
    """Execute DMG installation tasks."""
    for url in urls:
        dmg = DmgManagement(url=url, show_dialog=True)
        try:
            dmg.run()
            print()
        except UserCancelled as e:
            console.warning(str(e))
            console.info(f"Skipping {url}...\n")
            continue


def main():
    # Load tasks
    with open(TASKS_FILE) as f:
        tasks_json = json.load(f)

    bash_tasks = tasks_json.get("bash", [])
    dmg_urls = tasks_json.get("dmg", [])

    # Sort bash tasks by 'order', fallback to filename numeric prefix
    bash_tasks.sort(key=lambda t: t.get("order", parse_prefix(Path(t["script"]).name)))

    # Run bash tasks
    for task in bash_tasks:
        name: str = task["name"]
        script_path: Path = BASE_DIR / task["script"]
        show_log: bool = task.get("show_log", True)
        show_dialog: bool = task.get("show_dialog", True)

        try:
            console.box(name)
            run_bash_task(script_path, show_log=show_log, show_dialog=show_dialog)
        except UserCancelled as e:
            console.warning(str(e))
            console.info(f"Skipping {name}...\n")
            continue

    # Run DMG tasks
    if dmg_urls:
        console.box("Installing DMG applications", color="green")
        run_dmg_tasks(dmg_urls)


if __name__ == "__main__":
    main()
