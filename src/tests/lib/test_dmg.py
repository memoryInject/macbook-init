import pytest
from pytest import MonkeyPatch
from lib.dmg import DmgManagement
from utils.errors import UserCancelled


@pytest.fixture
def confirm_no(monkeypatch: MonkeyPatch):
    monkeypatch.setattr("lib.dmg.confirm", lambda prompt=None: False)


def test_download():
    dmg = DmgManagement("http://example.com/test.dmg", show_dialog=True)
    dmg.download_dmg()

    assert dmg.dmg_path == "/tmp/dmgdl_test/test.dmg"


def test_mount(monkeypatch: MonkeyPatch):
    fake_output = """
                /dev/disk4  Apple_HFS
                /Volumes/TestApp
                """

    def fake_run(*a, **k):
        class Result:
            stdout = fake_output

        return Result()

    monkeypatch.setattr("lib.dmg.subprocess.run", fake_run)

    dmg = DmgManagement("url", show_dialog=True)
    dmg.dmg_path = "/tmp/fake.dmg"
    dmg.mount_dmg()

    assert dmg.disk_id == "/dev/disk4"
    assert dmg.mount_point == "/Volumes/TestApp"


def test_copy_app():
    dmg = DmgManagement("x", show_dialog=True)
    dmg.mount_point = "/Volumes/Test"
    dmg.copy_to_applications()


def test_cancel_stops_install(confirm_no):
    dmg = DmgManagement("x", show_dialog=True)

    with pytest.raises(UserCancelled):
        dmg.download_dmg()
