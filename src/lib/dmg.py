import subprocess
import re
import tempfile
import os
import urllib.request
import shutil
import time
import sys

from lib.tui import confirm, console
from utils.errors import UserCancelled


class DmgManagement:
    def __init__(self, url: str, show_dialog: bool = False) -> None:
        self.url = url
        self.show_dialog = show_dialog
        self.tmpdir: str | None = None
        self.dmg_path: str | None = None
        self.dmg_name: str = os.path.basename(self.url)
        self.disk_id: str | None = None
        self.mount_point: str | None = None

    def run(self):
        console.box(f"Download and install {self.dmg_name}", color="bright_blue")
        self.download_dmg()
        self.mount_dmg()
        self.copy_to_applications()
        self.detach()
        self.cleanup()
        console.success("Installation finished successfully!")

    def _confirm(self, msg: str, result=False):
        """Ask user for confirmation before continuing"""
        if not self.show_dialog:
            return

        ans = confirm(prompt=msg)
        if result:
            return ans
        if not ans:
            raise UserCancelled(f"User cancelled: {msg}")

    def _progress_hook(self, block_num, block_size, total_size):
        downloaded = block_num * block_size
        percent = min(downloaded / total_size * 100, 100)
        # Carriage return '\r' keeps it on the same line
        # sys.stdout.write(f"\rDownloading: {percent:.2f}%")
        console.progress(percent, 100, color="bright_green")
        sys.stdout.flush()

    def download_dmg(self):
        # 1. Confirm download
        console.warning(f"Download DMG from: \n{self.url}")
        self._confirm("Proceed to download DMG? ")

        self.tmpdir = tempfile.mkdtemp(prefix="dmgdl_")
        self.dmg_path = os.path.join(self.tmpdir, self.dmg_name)
        console.info(f"Downloading {self.url} -> {self.dmg_path}")
        urllib.request.urlretrieve(
            self.url, self.dmg_path, reporthook=self._progress_hook
        )
        console.success("Download complete.\n")

    def mount_dmg(self):
        if not self.dmg_path:
            raise Exception("DMG does not exists, please download dmg file first")

        ans = self._confirm(f"Mount DMG: {self.dmg_name}?", result=True)
        if not ans:
            self.cleanup()
            raise UserCancelled("User cancelled at mount dmg")
        console.info("Mounting DMG...")
        result = subprocess.run(
            ["hdiutil", "attach", self.dmg_path],
            capture_output=True,
            text=True,
            check=True,
        )
        console.info(result.stdout)

        # Extract disk and mount point
        disk_match = re.search(r"(/dev/disk\d+)", result.stdout)
        mount_match = re.search(r"(/Volumes/.*)", result.stdout)

        if not disk_match or not mount_match:
            raise RuntimeError("Could not determine disk or mount point.")

        self.disk_id = disk_match.group(1)
        self.mount_point = mount_match.group(1).strip()
        console.success(f"Mounted at: {self.mount_point}\n")

    def copy_to_applications(self):
        if not self.mount_point:
            raise Exception(
                "Mount point does not exist, make sure mount the image first"
            )
        apps = [f for f in os.listdir(self.mount_point) if f.endswith(".app")]
        if not apps:
            raise RuntimeError("No .app found inside the DMG.")

        app_name = apps[0]
        src_app_path = os.path.join(self.mount_point, app_name)
        dest_app_path = f"/Applications/{app_name}"

        console.info(f"Found app: {src_app_path}")
        console.warning(f"Copy {app_name} to Destination: {dest_app_path}")
        ans = self._confirm("Continue?", result=True)
        if not ans:
            self.detach()
            self.cleanup()
            raise UserCancelled("User cancelled at copy to Applications")

        # Remove old version if exists
        if os.path.exists(dest_app_path):
            ans = self._confirm(
                "App already exists in /Applications. Replace it?", result=True
            )
            if not ans:
                self.detach()
                self.cleanup()
                raise UserCancelled("User cancelled at replace existing Applications")
            shutil.rmtree(dest_app_path)

        shutil.copytree(src_app_path, dest_app_path)
        console.success("Copied successfully.\n")

    def _force_detach(self):
        console.info("Detaching …")
        proc = subprocess.run(["hdiutil", "detach", self.mount_point])
        if proc.returncode == 0:
            console.success("Detached cleanly.\n")
            return

        console.warning("Normal detach failed, forcing detach …")
        time.sleep(1)
        subprocess.run(["hdiutil", "detach", self.mount_point, "-force"])
        console.success("Force-detached.\n")

    def detach(self):
        self._confirm("Ready to unmount the DMG?")
        self._force_detach()

    def cleanup(self):
        self._confirm("Delete temporary download files?")
        shutil.rmtree(self.tmpdir)
        console.success("Cleanup complete.\n")


if __name__ == "__main__":
    url = "https://github.com/alacritty/alacritty/releases/download/v0.16.1/Alacritty-v0.16.1.dmg"
    dmg = DmgManagement(url=url, show_dialog=True)
    dmg.run()
