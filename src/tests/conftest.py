# tests/conftest.py
import pytest
from pytest import MonkeyPatch


@pytest.fixture(autouse=True)
def fake_subprocess_run(monkeypatch: MonkeyPatch):
    def fake_run(*args, **kwargs):
        class Result:
            stdout = "ok"
            stderr = ""

        return Result()

    monkeypatch.setattr("subprocess.run", fake_run)
    return fake_run


class FakeConsole:
    def warning(self, *a, **kw):
        pass

    def info(self, *a, **kw):
        pass

    def box(self, *a, **kw):
        pass

    def success(self, *a, **kw):
        pass


def make_fake_confirm(response=True):
    return lambda prompt=None: response


@pytest.fixture(autouse=True)
def patch_tui(monkeypatch: MonkeyPatch):
    """
    Automatically patches src.lib.tui for every test.
    """

    monkeypatch.setattr("lib.bash.console", FakeConsole())
    monkeypatch.setattr("lib.bash.confirm", make_fake_confirm(True))
    monkeypatch.setattr("lib.dmg.console", FakeConsole())
    monkeypatch.setattr("lib.dmg.confirm", make_fake_confirm(True))

    yield


@pytest.fixture(autouse=True)
def patch_urllib(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(
        "lib.dmg.urllib.request.urlretrieve", lambda url, dest, reporthook=None: None
    )


@pytest.fixture(autouse=True)
def patch_tempfile(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(
        "lib.dmg.tempfile.mkdtemp", lambda prefix=None: "/tmp/dmgdl_test"
    )


@pytest.fixture(autouse=True)
def patch_os_shutil(monkeypatch: MonkeyPatch):
    monkeypatch.setattr("lib.dmg.os.listdir", lambda path: ["test.app"])
    monkeypatch.setattr("lib.dmg.os.path.exists", lambda p: False)
    monkeypatch.setattr("lib.dmg.shutil.copytree", lambda *a, **kw: None)
    monkeypatch.setattr("lib.dmg.shutil.rmtree", lambda *a, **kw: None)
